---
title: "Проєкт: 3G — QR-оплата окремого квитка у кабінеті водія"
date: 2026-06-25
tags: [3g, work, session, portmone, qr, driver, payments]
category: session
project: 3g
status: completed
aliases: ["QR оплата квитка 3G", "per-ticket QR payment"]
pinecone_indexed: false
---

# QR-оплата окремого квитка у кабінеті водія

**Гілка:** `qr_driver_ticket` (відгалужена від `driver`). Усі зміни **незакомічені**.

## Мета сесії
Додати у кабінет водія можливість оплатити через QR **окремий квиток**, а не лише все замовлення цілком (як було). Зробити так, щоб старий потік оплати всього ордера не зламався, і коректно працювало повернення коштів.

## Контекст наявного потоку (досліджено)
- Оплата через **Portmone**. QR генерується у `WidgetsController::getPortmoneUrl()` — `billNumber = {order_id}_{uuid}`, `amount = order->amount`, ставить `is_qr_sale=true` на всі квитки ордера.
- Callback успіху: `OrderController::confirmPayedPortmone()` (роут `POST /api/confirm/payed/portmone`, name `general.portmone.callback`). Парсив `SHOPORDERNUMBER` через `explode('_')`, ставив `SOLD` усім квиткам ордера.
- Рефанд: `ReturnTicket` job б'є Portmone REFUND, `shopOrderNumber = {order_id}_{uuid}`, результат у `ticket_retuned.paid_result`.
- **Ключове відкриття:** transaction id Portmone **ніде не зберігався** — Portmone ідентифікує платіж лише за `shopOrderNumber`. Сира відповідь callback не зберігалась; підпис callback **не перевіряється** (на відміну від LiqPay).

## Виконано

### Backend — поквиткова оплата
- Нове поле `tickets.payment_bill_number` (nullable string) — міграція `2026_06_25_120000_*`. Фіксує фактичний номер платежу.
- `WidgetsController::getTicketPortmoneUrl($id, $ticketId)` — QR на один квиток: `billNumber = {order_id}_{uuid}_t{ticket_id}`, `amount = ticket->price`, `is_qr_sale` + `payment_bill_number` тільки на цей квиток.
- Старий `getPortmoneUrl` тепер теж пише `payment_bill_number = {order_id}_{uuid}` на всі квитки ордера.
- `confirmPayedPortmone` — зворотньо-сумісний парсинг: `preg_match('/_t(\d+)$/')` + `explode('_', $raw, 2)`. Гілка квитка: `SOLD` лише цьому квитку, без `TicketSoldJob` (email у кабінеті водія не шлемо), parent/child не чіпає. Без суфікса `_t` — стара логіка ордера без змін.
- `ReturnTicket` — `shopOrderNumber = ticket->payment_bill_number ?: ({order_id}_{uuid})` (fallback для старих квитків).
- Роут `POST short-trip-management/{id}/get-ticket-portmone-url/{ticket}`.

### Фіксація типу оплати при «явився»
- Нове поле `tickets.payment_type` (nullable string) — міграція `2026_06_25_130000_*`. Значення з `config/types.php` payment_types: `not_paid_yet/cash/card/qr_code`.
- `TripManagementOperation::toggleTicketCheck()` приймає `payment` (fallback `type_payment`), валідує проти config, фіксує `payment_type`.
- Полагоджено фронтовий ланцюг подій: розбіжність `@toggleTicket` vs `@toggle-ticket` у `TicketsManager.vue`; `TripManagement.vue` тепер передає `payment` у тіло POST.

### QR-модалка: таби + сума
- `PaymentQrCode.vue` — два таби: **«Квиток»** (дефолт) і **«Все замовлення»**, різні QR (getTicketPortmoneUrl / getPortmoneUrl), сума над QR (`ticket.price` / `order_amount`). QR кешується по табу.
- **Умова одного квитка:** якщо `order_tickets_count <= 1` — таби сховані, лише режим «Все замовлення».
- Resource `TripManagementTicket` — додано `order_amount`, `order_tickets_count`. Eager-load `order` (з `withCount tickets` без TicketScope) + `parentTicket.order` у `TripStation::getTicketsFrom()` (анти-N+1) і у `WidgetsController::shortTripManagementWidget` (драйверський шлях).
- Трансферна узгодженість: `order_id`/`order_amount`/`order_tickets_count` беруться від одного й того самого order (`$orderTicket = parentTicket для non-transfer child`).

### Переклади
- `fields.*` для Vue беруться з **`lang/uk/fields.php`** (через `TranslationServiceProvider` → `window._translations`), а **НЕ** з `lang/php_uk.json` (json фронтом не використовується). Ключі `payment-qr-tab-ticket/order/amount` додано в `lang/uk/fields.php` (+ `lang/en/fields.php`).

## Проблеми й як вирішили

| Проблема | Рішення |
|---|---|
| Callback зав'язаний на `order_id` — оплата квитка закрила б весь ордер | Протягнули `ticket_id` через `billNumber` суфіксом `_t{id}` + гілка в callback |
| Рефанд шукав платіж за `{order_id}_{uuid}`, а поквитковий платіж має інший номер | Зберігаємо фактичний номер у `payment_bill_number`, рефанд бере його з fallback |
| `order_tickets_count = null` → таби не показувались (квиток 148331) | Драйверський `shortTripManagementWidget` обходив `getTicketsFrom()` → додали той самий `withCount` у `loadMissing` + фолбек у Resource |
| Переклади не резолвились | Лежали в `php_uk.json`; перенесли в `lang/uk/fields.php` |
| Локально не генерувався QR (`imagick not installed`) | Поставили PHP-розширення imagick через `pecl install imagick` (ImageMagick через brew вже був) |

## Ручна перевірка (без реального Portmone)
- `curl` ззовні на callback **впав 500** на `AuthCheck` middleware (`oauth/token` → `invalid_grant`) — роут callback стоїть за `auth.client`. Обійшли, викликавши `confirmPayedPortmone` напряму через `tinker`.
- **Сценарій A (квиток 148331, ордер 113101 на 2 квитки):** `SHOPORDERNUMBER=...._t148331` → `148331 SOLD`, `148332` лишився `booked`. ✅ Поквиткова оплата підтверджена.
- Сценарій B (весь ордер) — заплановано, ще не прогнано.

## Важливі рішення (ADR-замітки)
- **billNumber-формат `{order_id}_{uuid}_t{ticket_id}`** — обрано замість окремого callback-роуту чи `attribute4`, бо зворотньо сумісний (старий формат без `_t` → стара гілка).
- **Зберігати фактичний `payment_bill_number`**, а не реконструювати по `is_qr_sale` — бо `is_qr_sale` ставиться і при ордерній QR-оплаті, тож не розрізняє «оплачений окремо».
- Трансфери (parent/child): при поквитковій оплаті оплачується **рівно один запис** (рішення власника).
- У кабінеті водія QR-оплата **не шле email** (рішення власника).

## Відкриті питання / ризики
- **Безпека callback:** Portmone callback не перевіряє підпис (LiqPay — перевіряє). Варто додати перевірку автентичності.
- **AuthCheck на callback-роуті:** переконатись, що на проді Portmone реально проходить `auth.client`, інакше справжні callback-и відхиляються.
- Передіснуючий баг (не наш): `$ticket->code` у payload Portmone — колонки `code` на `tickets` немає, йде `null`.
- SMS у callback — на захардкоджений номер `380955784907`.
- `Order->amount` — збережена колонка, може бути застарілою без `calculateAmount()`.

## Артефакти
- Міграції: `2026_06_25_120000_add_payment_bill_number_to_tickets_table.php`, `2026_06_25_130000_add_payment_type_to_tickets_table.php` — **НЕ запущені** (потрібен `php artisan migrate`).
- Debug-нотатка: `.planning/debug/qr-tabs-single-ticket.md`.
- Ключові файли: `WidgetsController.php`, `OrderController.php`, `ReturnTicket.php`, `TripManagementOperation.php`, `TripManagementTicket.php`, `TripStation.php`, `Ticket.php`, `PaymentQrCode.vue`, `TripTickets.vue`, `TripManagement.vue`, `TicketsManager.vue`, `api-bridge.js`, `lang/uk/fields.php`.

## Ручні кроки (лишились користувачу)
1. `php artisan migrate` — застосувати `payment_bill_number` + `payment_type`.
2. `npm run build` — зібрати Vue.
3. Прогнати Сценарій B (оплата всього ордера + ідемпотентність).
4. Розглянути перевірку підпису Portmone callback.

## Пов'язані нотатки
- [[project-overview]]
