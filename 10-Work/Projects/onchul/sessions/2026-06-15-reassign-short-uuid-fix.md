---
title: "Проект: onchul (VTS) — фікс короткого UUID при реасайні квитка"
date: 2026-06-15
tags: [onchul, work, session, bugfix, booking]
category: session
project: onchul
status: completed
aliases: [onchul-reassign-short-uuid-fix]
pinecone_indexed: false
---

# Проект: onchul (VTS) — фікс короткого UUID при реасайні квитка

## Мета сесії

Користувач запитав, чому при реасайні (reassign) квитка `Order` отримує короткий UUID замість повноцінного згенерованого. Потрібно знайти корінь і поправити, не змінюючи решту робочої поведінки.

## Виконано

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Діагностика (debugger) | Корінь знайдено: `ReassignTicketOperation.php` передавав числовий PK `$ticket->order_id` у `BookingService::book()`, де він трактувався як `uuid` через `Order::firstOrNew(['uuid' => $orderId])` (≈ `BookingService.php:177` у старій нумерації). Як наслідок — створювався **новий** `Order` з `uuid="<id>"`, а повний генератор uuid пропускався через guard `if (! $orderId)`. |
| 2 | Реалізація (developer, Варіант B) | Додано параметр `?int $reuseOrderId = null` у `book()` та `bookOriginal()`. Нова гілка: `if ($reuseOrderId) { $order = Order::query()->findOrFail($reuseOrderId); } else { ... }`. Uuid-генератори тепер під guard `if (! $reuseOrderId && ! $orderId)` → uuid існуючого `Order` зберігається. Call site: `ReassignTicketOperation.php:128` → `$service->book($trip, $tickets, null, false, $ticket->order_id)`. Pint прибрав невикористані імпорти і додав дужки в `if (empty($tickets))`. |
| 3 | Рев'ю (reviewer) | Підняв 2 концерни: (1) дужки в `if (empty($tickets))`; (2) перезапис `trip_id`/`member_id`/`currency_id` у reuse-гілці. |
| 4 | Розбір концернів | Дужки **не** змінювали потік: без дужок до `if` прив'язувався лише перший `return`, тож `book()` і так виконувався коректно — Pint лише косметика. `associate(trip/member/currency)` лишили як є, бо старий шлях робив те саме на новому `Order`; `member` фактично той самий (`api_user = order->member_id`). Рішення користувача: «ціль — поправити тільки `order_id` (uuid), все інше працювало» → мінімальний фікс, нічого зайвого. |

## Важливі рішення (ADR)

| # | Питання | Рішення | Чому |
|---|---------|---------|------|
| 1 | Як переюзати існуючий Order при реасайні | Варіант B: пошук Order по PK `id` (`findOrFail`) без перезапису `uuid` | Чистіше розділення id-каналу від uuid-каналу, ніж у Варіанті A (передавати `$ticket->order->uuid`) |
| 2 | Чи прибирати `associate(trip/currency/member)` у reuse-гілці | Залишити навмисно | Відповідає робочій поведінці до фіксу; `member` той самий, тож семантика не змінюється |

## Проблеми й як вирішили

- **Bug / blocker:** При реасайні квитка `Order` отримує короткий UUID (`uuid = "<order_id>"`).
  - **Причина:** числовий PK `$ticket->order_id` передавався як `$orderId` і трактувався у `Order::firstOrNew(['uuid' => $orderId])`; повний генератор uuid пропускався через `if (! $orderId)`.
  - **Фікс:** окремий канал `?int $reuseOrderId` → `Order::findOrFail($reuseOrderId)`; uuid-генерація лише коли `! $reuseOrderId && ! $orderId`.
- **Хибне зауваження reviewer** про «мертвий код» у `book()` — спростовано аналізом семантики `if` без дужок (до `if` прив'язувався лише `return`, далі код виконувався нормально).

## Артефакти

- **Файли:**
  - `app/Services/BookingService.php` — `book()`, `bookOriginal()` (+ параметр `?int $reuseOrderId`)
  - `app/Crud/Operations/ReassignTicketOperation.php` — call site (`:128`) + Pint formatting
- **Стан:** незакомічено (working tree, гілка `migrate_refact`). Коміт/пуш **не** робились.
- **Edge cases для тестів** (tester ще не запускався):
  - uuid існуючого `Order` не змінюється до/після реасайну (головний регрес)
  - reassign на неіснуючий `order_id` → `findOrFail` кидає `ModelNotFoundException`
  - reassign з transfer — дочірнє transfer-замовлення отримує нормальний uuid, батьківське переюзається
  - звичайне нове бронювання — uuid генерується як раніше

## Пов'язані нотатки

- [[10-Work/Projects/onchul/project-overview]]
- [[BookingService]]
- [[Order]]
- [[ReassignTicketOperation]]
