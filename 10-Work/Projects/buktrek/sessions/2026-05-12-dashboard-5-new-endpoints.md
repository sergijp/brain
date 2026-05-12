---
title: "Проект: buktrek — 5 нових дашборд-ендпойнтів за специфікаціями data/*.json"
date: 2026-05-12
tags: [buktrek, work, session, dashboard, api]
category: session
project: buktrek
status: completed
aliases: []
pinecone_indexed: false
---

# Проект: buktrek — 5 нових дашборд-ендпойнтів за специфікаціями data/*.json

## Мета сесії

У папці `data/` лежать 5 JSON-специфікацій того, що має повертати фронтенд-дашборд
(`kpi.json`, `directions.json`, `drivers.json`, `finance.json`, `fleet.json`).
Імплементувати відповідні Laravel-ендпойнти, прийнявши рішення по кожному полю,
яке не мапиться 1:1 на наявну схему.

## Виконано

| # | Задача | Результат |
|---|--------|-----------|
| 1 | `kpi.json` → `/dashboard/kpi` | `getKpi()` — fleet (in_transit/total/idle/problems по distinct transport_id) + finance (earned/expected по amount); фільтри period/carrier_id/customer_id |
| 2 | `directions.json` → `/dashboard/directions` | `getDirections()` — group by (from, to, carrier_id) з revenue, has_problem, статусами (тільки ненульові); `carriers[]` для селекта |
| 3 | `drivers.json` → `/dashboard/drivers` | `getDrivers()` — status (problem/in_transit/idle), label з driver_status активної заявки, trips/mileage/work_days/problems, idle_days з `downtime_logs` |
| 4 | `finance.json` → `/dashboard/finance` | `getFinance()` — `summary.received/expected` + `clients[]` (id/name/trips/freight); поля без даних (paid/overdue/total/plan/currency) свідомо опущено |
| 5 | `fleet.json` → `/dashboard/fleet` | `getFleet()` — Gantt-сегменти per-transport: trip_done/trip_active/problem/planned/idle; `status_label` з кількістю днів; mileage_km = SUM completed |
| 6 | Vault arch-doc | `docs/dashboard-api.md` + рядок у `docs/INDEX.md` |

## Важливі рішення (ADR)

| # | Питання | Рішення | Чому |
|---|---------|---------|------|
| 1 | Currency у finance/kpi/directions | Відкладено — не фільтруємо по `amount_currency_id`, сума всіх валют | Немає `Setting::get('dashboard_currency')`; коли з'явиться — додамо |
| 2 | `Application.amount` vs `freight` | `amount` = revenue замовнику (kpi.earned/expected, summary.received/expected, directions.revenue); `freight` = фрахт перевізника (clients[].freight, fleet segment.freight) | Узгоджено напряму з користувачем |
| 3 | `fleet.in_transit` рахуємо distinct transport_id, виключаючи is_problem | `idle = total - in_transit - problems` без перекриттів | Авто не може одночасно бути і "в дорозі" і "в проблемі" — інакше дублюється |
| 4 | `drivers.problems` рахуємо поточний `is_problem=1`, не journal | `is_problem` НЕ логується в `Application::logOnly()` — повного журналу нема | Compromise; для повного journal треба додати поле до logOnly |
| 5 | `fleet.segments[].idle` — тільки з `downtime_logs`, без gap-заповнення | Прагматичне спрощення | Розрахунок gaps між заявками — складна логіка; downtime_logs покривають реальні простої водіїв |
| 6 | `fleet` period filter — strict (`whereYear+whereMonth`), не overlap | Включаємо тільки заявки де `loading_date` у period | За домовленістю з користувачем |
| 7 | `fleet.vehicles[].driver/trailer` — з найсвіжішої заявки за period | `sortByDesc('loading_date')->first()` | Простіше і прозоріше за priority-логіку (problem→inprog→sched→completed) |
| 8 | `fleet.vehicles[].status_label` з днями ("Простій 7 дн.") | sum (end_day - start_day) сегментів цього типу | За домовленістю |
| 9 | `finance` — недоступні поля не повертаємо взагалі | overdue/total/plan/currency/paid просто відсутні в JSON | За домовленістю з користувачем |
| 10 | `fleet.model`, `fleet.mileage_km` (загальний одометр) — не повертаємо | Немає поля у `transports` | За домовленістю |
| 11 | `carriers[]` "all" elem — `{id:0, label:"Всі перевізники"}` | Літерал замість lang ключа | `crud.all` = "Загальна сума" (не "Всі"); окремого ключа `all_carriers` не існує |
| 12 | Всі нові endpoints **НЕ використовують** `baseQuery()` | Пишуть фільтр самостійно | `baseQuery` додає `active=true+archive=false`, а у kpi `earned` треба і архівні |

> Детальніші контракти й callsite-и — у [[dashboard-api]].

## Проблеми й як вирішили

- **Прогалини в БД для `finance.json`** — у нас немає `paid_amount`, `due_date`,
  таблиці планів, окремих платежів. **Рішення:** не повертати ці поля взагалі
  (а не нулі/null'и) — user explicit. Якщо знадобиться повна спека — окрема
  міграція + UI для введення.
- **`is_problem` = toggle, не журнал** — `ApplicationService::94` ставить `true`,
  `ApplicationsCrudController::removeProblem` (2113) знімає. `Application::logOnly()`
  (167-189) не містить `is_problem` → activity_log не зберігає історію. **Рішення:**
  `drivers.problems` = поточний прапор; TODO у коментарі для майбутнього розширення.
- **`Application` має і `amount` (для замовника), і `freight` (фрахт перевізника)** —
  легко переплутати. Зафіксовано у docs контракт 6.
- **Linter shows hundreds of "Unknown column" warnings** — IDE не резолвить колонки
  з міграцій (це норма для цього проекту, не блокери). Reading через `php -l` усе чисто.

## Артефакти

**Нові файли:**
- `app/Http/Requests/Dashboard/KpiRequest.php`
- `app/Http/Requests/Dashboard/DirectionsRequest.php`
- `app/Http/Requests/Dashboard/DriversReportRequest.php`
- `app/Http/Requests/Dashboard/FinanceRequest.php`
- `app/Http/Requests/Dashboard/FleetRequest.php`

**Змінені файли:**
- `app/Services/Dashboard/DashboardService.php` — додано 5 публічних методів + хелпери
  (`resolveKpiPeriod`, `buildCarriersFilter`, `resolveVehicleStatus`, `buildAppSegment`,
  `buildDowntimeSegment`, `clampDay`); імпорти Transport, Carrier
- `app/Http/Controllers/Api/Dashboard/DashboardController.php` — 5 нових `kpi/directions/drivers/finance/fleet` методів + імпорти Request-класів
- `routes/api.php` — 5 нових роутів під `/api/system/dashboard/*`

**Команди:**
```bash
php -l app/Services/Dashboard/DashboardService.php
php artisan route:list --path=dashboard
```

## Пов'язані нотатки

- [[10-Work/Projects/buktrek/project-overview]]
- [[10-Work/Projects/buktrek/docs/INDEX]]
- [[10-Work/Projects/buktrek/docs/dashboard-api]] — повна arch-документація (контракти + callsite-и + gotchas)
- [[10-Work/Projects/buktrek/docs/downtime]] — пов'язано через idle сегменти у fleet і `drivers-downtime`
- [[10-Work/Projects/buktrek/sessions/2026-05-11-downtime-limits-and-dashboard-reports]] — попередня дашборд-сесія