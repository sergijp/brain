---
title: "Проект: 3g — EcheckService: готівкова оплата при закритті станції"
date: 2026-05-14
tags: [3g, work, session, echeck, fiscal]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Доопрацювати систему фіскальних чеків (EcheckService): при закритті станції (посадка пасажирів) вказувати в чеку тип оплати "готівка" (`paymentTypeId: 1`) і суму готівки в копійках.

## Виконано

| Задача | Результат |
|--------|-----------|
| Дослідити всі місця виклику EcheckService | Знайдено 7 call sites; виявлено що `TripManagementOperation::arrived()` — головне місце для готівки |
| Дослідити статуси квитків та поле `seat_payment` | `pendingEcheck()` scope ловить тільки готівкові квитки (seat_payment або booked/prebooked) |
| Перевірити чи є перевірки на `echeck_id` | `SendEcheckSmsJob` має подвійний захист (lockForUpdate); в `arrived()` — немає |
| Реалізувати зміни в 3 файлах | ✅ |

## Важливі рішення

| Рішення | Обґрунтування |
|---------|---------------|
| Логіку визначення типу оплати — у `SendEcheckSmsJob` (через `$isCash`) | Job вже знає всі квитки ордеру, має доступ до суми |
| `whereNull('echeck_id')` в `arrived()` — як оптимізація | Job сам ідемпотентний (lockForUpdate), але зайві dispatch-и усунуто |
| Статус `sold` не чіпаємо | Потребує окремого аналізу — може бути і онлайн і готівка |

## Артефакти (змінені файли)

### `app/Services/EcheckService.php` (рядок 86)
```php
public function createEcheck(string $orderId, array $products, int $paymentTypeId = 7, int $cash = 0): array
```
- Додано параметри `$paymentTypeId` і `$cash` з дефолтами (зворотна сумісність збережена)

### `app/Jobs/Echeck/SendEcheckSmsJob.php`
- Конструктор: додано `public bool $isCash = false`
- В `handle()`: перед `createEcheck()` визначається тип оплати:
  - `$isCash = true` → `paymentTypeId = 1`, `cash = sum(price)` (в копійках)
  - `$isCash = false` → дефолти (paymentTypeId = 7, cash = 0)

### `app/Crud/Operations/TripManagementOperation.php` (метод `arrived()`)
- Додано `->whereHas('order', fn($q) => $q->whereNull('echeck_id'))` в Ticket query
- Dispatch змінено: `SendEcheckSmsJob::dispatch($orderTickets->first(), false, true)` (isCash = true)

## Контекст — типи оплати квитків

| Стан | `status` | `seat_payment` | Тип оплати |
|------|----------|----------------|------------|
| Оплата при посадці | `booked` | `true` | Готівка (paymentTypeId: 1) |
| Попереднє бронювання | `prebooked` | `true` | Готівка (paymentTypeId: 1) |
| Бронювання → оплачено | `sold` | `false` | Уточнити окремо |

## Що залишилось на потім

- Статус `sold` — визначити чи завжди онлайн/картка або може бути готівка
- `OrderController::paymentCallback()` — там `createEcheck()` викликається напряму, без Job; поки не чіпаємо
- `TicketsController::sendEcheckSmsByStation()` — ручний виклик; `isCash` не передається

## Пов'язані нотатки

- [[project_echeck_fiscal]] — повна реалізація системи фіскальних чеків (T0-T10)
