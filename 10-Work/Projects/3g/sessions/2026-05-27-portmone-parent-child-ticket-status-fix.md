---
title: "Проект: 3g — Фікс синхронізації статусу parent/child квитків у Portmone/LiqPay callback"
date: 2026-05-27
tags: [3g, work, session, bugfix, payments, portmone, liqpay, eloquent-scope]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

# Фікс: статус parent/child квитків не оновлювався при підтвердженні платежу

## Мета сесії

Користувач повідомив про баг у `confirmPayedPortmone`: на сервері в основному квитку статус міняється, а в `parentTicket` / `childTicket` (трансферні квитки) — ні.

## Виконано

| Задача | Результат |
|--------|-----------|
| Діагностика root cause | Знайдено: `TicketScope` (global scope) фільтрує по `member_id`, lazy-load relationships тягне його повторно і повертає `null` для не-власника ордера |
| Виявлено симетричний баг у LiqPay-методі | `confirmPayed` мав той самий + **ширший** баг (взагалі без `withoutGlobalScope` на головному запиті) |
| Точковий фікс через eager-load | `with(['parentTicket' => fn($q) => $q->withoutGlobalScope(TicketScope::class), ...])` |
| `./vendor/bin/pint` | passed (1 stylistic fix) |

## Важливі рішення (ADR)

| Рішення | Альтернатива | Чому обрано |
|---------|--------------|-------------|
| Eager-load з `withoutGlobalScope` у запиті | `->withoutGlobalScope()->first()` на кожному lazy access | Менше SQL-запитів, мінімум змін у логіці, існуючі `if ($ticket->parentTicket)` запрацювали без переписування |
| Фікс тільки в `OrderController.php` | Винести логіку в `BookingService::markOrderAsPaid()` | Користувач явно обмежив scope одним файлом — точкове виправлення без рефакторингу |
| Не чіпати `TicketScope` сам по собі | Зняти глобальний скоуп або переробити | Поза scope задачі, ризик регресії в інших місцях коду |
| Не запускати `tester` автоматично | Запустити з RefreshDatabase | `feedback_test_database.md` — ризик знищення БД без `.env.testing`, перевірка вручну на сервері |

## Проблеми й як вирішили

### Bug 1: lazy-load relationship тягне global scope
**Симптом:** `if ($ticket->parentTicket) { ... }` ніколи не виконується для не-власника ордера.
**Причина:** `$order->tickets()->withoutGlobalScope(TicketScope::class)->get()` знімає скоуп лише з прямого запиту. Звертання до `$ticket->parentTicket` — це окремий SQL із активним скоупом → `null`.
**Фікс:** eager-load з вкладеним `withoutGlobalScope`.

### Bug 2 (виявлений в процесі): LiqPay варіант ще гірший
**Симптом:** `confirmPayed` міг не оновлювати навіть основний квиток для не-власника.
**Причина:** там використовувався `$order->tickets->whereIn(...)` (collection filter), без жодного `withoutGlobalScope`.
**Фікс:** перевів на query builder з `withoutGlobalScope` + eager-load (симетрично Portmone-варіанту).

### Контекст роуту
Користувач підсвітив `routes/api.php:57` — `/confirm/payed/portmone` оголошений **поза будь-якою middleware group** (unauthenticated). Тобто callback від Portmone (server-to-server) приходить без user'а, і `TicketScope::apply()` має ранній `return` для `!$user`. Тоді чому баг проявляється? Гіпотеза: на production шлях колись пройшов через автентифікований клієнтський redirect, або існує інший callback-шлях через сесію — в цих випадках user активний, але не власник ордера → relationship падає в null.

## Артефакти

### Файли змінено
- `app/Http/Controllers/Api/OrderController.php`
  - `confirmPayedPortmone` (рядки ~392–456) — додано eager-load з `withoutGlobalScope`
  - `confirmPayed` LiqPay (рядки ~280–353) — переведено з collection filter на query builder + eager-load з `withoutGlobalScope`

### Файли НЕ чіпали (свідомо)
- `app/Scopes/TicketScope.php`
- `app/Services/BookingService.php`
- `routes/api.php`

### Команди
```bash
./vendor/bin/pint app/Http/Controllers/Api/OrderController.php
```

### Pattern для подальших фіксів подібного типу
```php
$ticket = $order->tickets()
    ->withoutGlobalScope(TicketScope::class)
    ->with([
        'parentTicket' => fn ($q) => $q->withoutGlobalScope(TicketScope::class),
        'childTicket'  => fn ($q) => $q->withoutGlobalScope(TicketScope::class),
    ])
    ->whereIn('status', [...])
    ->get();
```

## Залишкові задачі / технічний борг

- IDE diagnostics показав ~50 pre-existing warnings у `OrderController.php` (magic property access, missing return types, `Order::find()` не розпізнається, unused vars). Не виправлено — поза scope. Кандидат для окремого `laravel-refactoring-expert` прогону.
- `TicketScope` як глобальний скоуп — потенційне джерело подібних багів у інших операціях з related tickets. Потрібен окремий аудит usage.
- У `confirmPayedPortmone` після оновлення статусів є інші читання `$order->tickets` (для SMS-нотифікацій), теж без `withoutGlobalScope` — поки не критично, але теоретично могли б дати неповний список номерів у SMS.
- Verification на сервері: відтворити сценарій трансферного квитка + платіж Portmone → перевірити що child/parent ticket перейшли у `STATUS_PAYED`.

## Пов'язані нотатки

- [[2026-05-19-busfor-api-transfer-fixes]] — інші баги трансферних квитків
- [[project_infobus_sync]] (auto-memory) — синхронізація трансферів, CreateTicketJob fixes
- Сусідні роботи з payments: жодних інших активних