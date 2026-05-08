---
title: "Echeck — фіскальні чеки"
date: 2026-05-08
tags: [3g, architecture, fiscal, echeck, sms]
category: docs
project: 3g
status: active
aliases: ["3g-echeck", "3g-fiscal"]
pinecone_indexed: false
---

# Echeck — фіскальні чеки

Гілка `echeck` — всі таски T0-T10 виконані. Pending тільки smoke test на staging і вставка SMS-шаблону в БД.

## Компоненти

- `EcheckService` — auth, shift open/close, `createEcheck`, `cancelEcheck`, `infoEcheck`, Z-reports.
- `ShiftOpenJob` / `ShiftCloseJob` — щодня 00:00/23:59 + email, Z-report PDF у `storage/z-reports/`.
- `SendEcheckSmsJob` — повністю реалізований: force flag, retry, DB lock, multi-SMS, dry-run.
- `ReceiptCreateJob` — **видалений** (T10, мертвий код).

## БД

- `orders.echeck_id`
- `orders.echeck_answer`
- `orders.echeck_sms_sent_at`
- `members.echeck_enabled`

## Env

```
ECHECK_ENABLED=true    # kill-switch (false = nothing)
ECHECK_DRY_RUN=false   # true = тільки логи, без реальних API/SMS
```

**Why dry-run:** тестування на лайві без створення реальних чеків.

## SMS-шаблон

- Зберігається у таблиці `settings`, ключ `echeck_sms_template`.
- **Запис ще не існує в БД** — fallback у коді: `'Шановний [client], Ваш фіскальний чек: [link]'`.
- Змінні: `[client]` = `full_name`, `[link]` = URL чеку.
- Редагування через адмінку (`/settings`) **після** вставки рядка:
  ```sql
  INSERT INTO settings (key, value)
  VALUES ('echeck_sms_template', 'Шановний [client], Ваш фіскальний чек: [link]');
  ```

## Архітектурні рішення

1. **Два scope на Ticket:** `pendingEcheck` (кандидати — фронт), `includedInEcheck` (payload чеку: SOLD OR booked/prebooked+seat_payment+checked).
2. **Один чек на ордер** — `createEcheck(orderId, products[])`.
3. **Dedup SMS:** `orders.echeck_sms_sent_at`; авто-dispatch перевіряє і виставляє; `$force=true` ігнорує.
4. **Retry:** `$tries=10`, exp backoff `[30,60,120,240,480,960,1800,3600,3600,3600]`. URL=null → release; shift CLOSED → release до 00:05.
5. **DB lock:** `lockForUpdate` на orders при створенні чеку (паралельні воркери).
6. **Admin override:** `$force=true` — ігнорує `echeck_enabled` і `echeck_sms_sent_at`. SMS тільки на `this->ticket.phone`.
7. **Kill-switch:** `ECHECK_ENABLED` + `config/services.echeck.enabled`.
8. **Dry-run:** `ECHECK_DRY_RUN` + `config/services.echeck.dry_run`. Логи: `echeck_dry_run_mode`, `echeck_products_ready`, `echeck_dry_run_skip_create`, `echeck_dry_run_would_sms`.
9. **Logs:** channel `echeck` → `storage/logs/echeck.log`.
10. **Portmone:** Job dispatch після оплати; email `OrderTicketsSold` з guard `release(60)` поки `echeck_id` не готовий.
11. **LiqPay/QR:** dispatch у `BookingController::confirmPayed`.
12. **Driver booking (готівка):** echeck **не додається** — cash, не потрібно.

## Сценарії

| Актор | Сценарій | Де dispatch |
|---|---|---|
| Пасажир онлайн (Portmone) | оплата картою | `OrderController::confirmPayedPortmone` |
| Пасажир QR (LiqPay) | через QR | `BookingController::confirmPayed` |
| Водій arrived | BOOKED + checked | `TripManagementOperation::arrived` |
| Адмін вручну | "Надіслати чек" | `TicketsController::sendEcheckSms` (force=true) |
| Адмін по станції | "По станції" | `TicketsController::sendEcheckSmsByStation` |
| Водій пряме | готівка | **не додається** |

## Тести (17, всі проходять)

- `tests/Feature/Echeck/SendEcheckSmsJobTest.php` — 12 тестів (`Http::fake`, `dispatchSync`).
- `tests/Feature/Echeck/SendEcheckSmsEndpointTest.php` — 5 тестів (`Queue::fake`, `Passport::actingAs`).

## Pending

- **T9** — ручний smoke test на staging (`queue:work`, сценарії A/B/C, PDF у email).
- Запис `echeck_sms_template` у БД (seeder/міграція).

## Пов'язані

- [[INDEX]]
- [[notifications]] — `SendEcheckSmsJob::sendSms()` через `TicketNotificationService::configure()` + channel routing
