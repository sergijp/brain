---
title: "Проект: 3g — Echeck при закритті станції: дослідження + баг booked/seat_payment"
date: 2026-06-30
tags: [3g, work, session, echeck, bug, fiscal]
category: session
project: 3g
status: in-progress
aliases: []
pinecone_indexed: false
---

# Echeck при закритті станції — дослідження + знайдений баг

## Мета сесії
1. Дослідити, яким квиткам відправляється/створюється echeck (фіскальний чек) при закритті станції.
2. Перевірити повідомлений користувачем баг: echeck НЕ створюється, якщо квиток має статус `booked`.

## Виконано

### 1. Ланцюжок створення echeck при закритті станції
```
POST /crud/trip/{id}/station/{station_id}/arrived
  → TripManagementOperation::arrived()            app/Crud/Operations/TripManagementOperation.php:105-178
  → SendEcheckSmsJob::dispatch($ticket, false, isCash:true)   :153
  → SendEcheckSmsJob::handle()                    app/Jobs/Echeck/SendEcheckSmsJob.php
  → EcheckService::createEcheck()                 app/Services/EcheckService.php
```

### 2. Відбір квитків-тригерів (TripManagementOperation.php:138-147)
```php
Ticket::query()
    ->withoutGlobalScope(TicketScope::class)
    ->where('trip_id', $id)                  // квитки рейсу
    ->where('from_id', $station->station_id) // ПОСАДКА саме на цій станції
    ->pendingEcheck()                         // scope-тригер
    ->whereHas('order.member', fn($q) => $q->where('echeck_enabled', true))
    ->whereHas('order', fn($q) => $q->whereNull('echeck_id')) // без дублів
    ->with('order')->get()->groupBy('order_id'); // 1 чек на ордер
```

### 3. Два scope з різними ролями (Ticket.php)
- **`scopePendingEcheck()` (358-366)** — ТРИГЕР: чи запускати job для ордера.
  `(seat_payment=true OR status IN (booked,prebooked)) AND status!=sold AND checked=true`
- **`scopeIncludedInEcheck()` (368-382)** — НАПОВНЕННЯ: які квитки ордера друкуються в чек (включає `sold`).
  `status=sold OR (prebooked AND checked) OR (booked AND seat_payment=true AND checked)`

## Знайдений баг (ПІДТВЕРДЖЕНО)

**Розбіжність між двома scope для статусу `booked`:**

| Статус | seat_payment | checked | pendingEcheck (тригер) | includedInEcheck (чек) | Наслідок |
|--------|--------------|---------|------------------------|------------------------|----------|
| booked | **false**    | true    | ✓ проходить            | ✗ НЕ проходить         | **БАГ** |
| booked | true         | true    | ✓                      | ✓                      | OK |
| prebooked | true      | true    | ✓                      | ✓                      | OK |
| sold   | -            | -       | ✗                      | ✓                      | OK |

**Сценарій збою:** `booked` + `seat_payment=false` (це дефолт для booked, `Order.php:96` + міграція `default(false)`) + `checked=true`:
- проходить `pendingEcheck()` → job запускається;
- `includedInEcheck()` відкидає (бо вимагає `seat_payment=true`);
- колекція порожня → `Log::warning('echeck_no_included_tickets')` + тихий `return`;
- **чек не створюється**.

**Root cause:** `app/Entities/Tenant/Ticket.php:377-379` — зайва/неузгоджена умова `->where('seat_payment', true)` для `booked` у `scopeIncludedInEcheck()`.

## Важливі рішення (ADR)

| Питання | Рішення |
|---------|---------|
| Чи має `booked` з `seat_payment=false` отримувати чек при закритті станції? | **НІ, не має** (рішення користувача). |
| Напрям фіксу | Узгодити `pendingEcheck()` з `includedInEcheck()`: додати вимогу `seat_payment=true` для `booked` у **тригер** (`pendingEcheck`), щоб такі квитки взагалі не запускали job. НЕ прибирати умову з `includedInEcheck`. |

## Артефакти / локації
- `app/Crud/Operations/TripManagementOperation.php:105-178, 138-147`
- `app/Jobs/Echeck/SendEcheckSmsJob.php` (handle, dispatch :153, isCash логіка, `echeck_no_included_tickets`)
- `app/Entities/Tenant/Ticket.php:358-366` (pendingEcheck), `:368-382` (includedInEcheck — root cause :377-379)
- `app/Entities/Tenant/Order.php:96` (виставлення seat_payment)
- міграція `2024_04_26_104959` — `seat_payment` default(false)

## Наступні кроки (НЕ зроблено)
- [ ] Фікс `scopePendingEcheck()`: вимагати `seat_payment=true` для `booked` (узгодити з рішенням «booked без оплати при посадці чек не отримує»).
- [ ] Тест-репро на сценарій booked/seat_payment=false/checked=true.
- [ ] Перевірити, чи інші виклики `pendingEcheck()` не покладаються на старий критерій.

## Пов'язані нотатки
- [[2026-06-25-qr-oplata-okremogo-kvytka]]
- [[2026-06-26-driver-cash-and-ticket-colors]]
