---
title: "dashboard-api — архітектура"
date: 2026-05-12
tags: [buktrek, architecture, dashboard, api]
category: docs
project: buktrek
status: active
aliases: ["buktrek-dashboard-api", "dashboard-endpoints"]
pinecone_indexed: false
last_verified: 2026-06-22
---

# dashboard-api

## Контекст

Дашборд для адміністратора/менеджера, що показує метрики логістичного процесу
(автопарк, водії, замовлення, фінанси). Усі ендпойнти зібрані у єдиний контролер
`DashboardController` з тонкою делегацією у `DashboardService` (single class,
~1500 рядків).

Дашборд читає **тільки systemDB** (Application, Transport, Driver, Carrier,
Customer, DowntimeLog) — не зачіпає tenant-БД.

## Endpoint-и (повна мапа)

| Route | Метод сервісу | Спека `data/` | Призначення |
|---|---|---|---|
| `GET /api/system/dashboard/kpi` | `getKpi` | `kpi.json` | KPI-плитки: fleet (in_transit/total/idle/problems) + finance (earned/expected) |
| `GET /api/system/dashboard/directions` | `getDirections` | `directions.json` | Топ напрямків (from→to×carrier) з revenue, статусами, has_problem |
| `GET /api/system/dashboard/drivers` | `getDrivers` | `drivers.json` | Per-driver: status, trips, mileage, work_days, problems, idle_days |
| `GET /api/system/dashboard/finance` | `getFinance` | `finance.json` | Revenue summary + per-client freight breakdown |
| `GET /api/system/dashboard/fleet` | `getFleet` | `fleet.json` | Per-vehicle Gantt-timeline сегментів за period |
| `GET /api/system/dashboard/filters` | `getFilters` | — | Опції для фільтрів дашборду |
| `GET /api/system/dashboard/monthly-chart` | `getMonthlyChart` | — | Бар-чарт по місяцях року |
| `GET /api/system/dashboard/routes-timeline` | `getRoutesTimeline` | — | Карієр + статус-фуннел |
| `GET /api/system/dashboard/routes-statuses` | `getRoutesStatuses` | — | Топ-20 напрямків (без carrier-розбивки) |
| `GET /api/system/dashboard/drivers-timeline` | `getDriversTimeline` | — | Розбивка по driver_status |
| `GET /api/system/dashboard/drivers-downtime` | `getDriversDowntime` | — | Журнал простоїв (див. [[downtime]]) |
| `GET /api/system/dashboard/donut-statistics` | `getDonutStatistics` | — | Donut по driver_status за місяць |
| `GET /api/system/dashboard/tickets`<br>`/dashboard/tickets/{id}` | `getTickets`/`getTicketDetails` | — | Картки заявок |
| `GET /api/system/dashboard/kanban` | `getKanban` | — | Канбан по application_status |
| `GET /api/system/dashboard/gantt` | `getGantt` | — | Gantt по водіях за місяць |

## Ключові контракти

1. **Period filter** — спільний хелпер `resolveKpiPeriod(filters)` приймає `period=YYYY-MM`
   → потім `year`+`month` → fallback на поточний місяць. Усі нові ендпойнти (kpi,
   directions, drivers, finance, fleet) використовують **strict period**:
   `whereYear+whereMonth` по `loading_date`. **Не overlap.**

2. **Filters спільні** — `period`, `carrier_id`, `customer_id`. Запит-класи
   успадковуються від `DashboardRequest` (там вже `manager_id/customer_id/carrier_id/search_query/year/month/date_range`).
   Нові додають regex для `period`.

3. **Currency — групування по валютах (оновлено 2026-06-22).** `kpi` (earned/expected),
   `directions` (revenue/avg_freight) **і `finance`** (received/expected + clients[].freight)
   групують по валютах через спільний `sumColumnByCurrency(Builder, $column, $currencyFk,
   $fallback)` (leftJoin currencies, group by code) → `list<{code, amount}>`.
   `sumAmountByCurrency` = тонкий wrapper для `amount`/`amount_currency_id`.
   **Важливо:** `amount` → `amount_currency_id` (revenue/received/expected),
   `freight` → `freight_currency_id` (clients[].freight) — РІЗНІ валютні FK.
   Заявки без валюти → дефолтна (`resolveDefaultCurrencyCode()`, fallback `EUR`).
   Нульові бакети фільтруються. На фронті — кілька рядків `{symbol} {amount}` на плитку
   (KpiBar, FinanceView; total = merge received+expected по коду).

4. **`is_problem` — поточний прапор, не журнал.** `applications.is_problem` —
   toggle (ставить `start-trip` коли проблема, `ApplicationsCrudController::removeProblem`
   знімає). У `getDrivers` поле `problems` рахує **заявки де `is_problem=1` зараз**.
   Для повного journal треба додати `is_problem` до `Application::logOnly()`.

5. **Fleet idle сегменти — тільки з `downtime_logs`.** У `getFleet` `segments[].idle`
   беруться з `downtime_logs` де `application_id` належить заявці транспорту.
   **Gaps між заявками не заповнюються** — це свідоме спрощення.

6. **`Application.amount` vs `Application.freight`** — `amount` = сума заявки
   для замовника (revenue/earned/expected у summary), `freight` = фрахт
   перевізника (поле `clients[].freight` у finance, segment.freight у fleet).
   **Не плутати.**

7. **Carriers selector** — спільний хелпер `buildCarriersFilter()` повертає
   `[{id:0, label:"Всі перевізники"}, {id:N, label:legal_name}, ...]`.
   Використовується у `getDirections` і `getDrivers`.

8. **Default carrier — усі 6 табів (2026-06-22).** `carriers.default` (boolean,
   one-default через `Carrier::boot::saved`). **Усі 6 ендпойнтів** — `kpi`,
   `directions`, `kanban`, `gantt`, `fleet`, `drivers` — без явного `carrier_id`
   роблять fallback на `resolveDefaultCarrierId()` → відкриваються pre-scoped, і
   повертають резолвлений `carrier_id` + `carriers` (`buildCarriersFilter`).
   Конвенція: `carrier_id=0` = «всі» (явно), `null`/відсутній = застосувати default.
   На фронті очищення/вибір «всі» шле `0`, не `null`.
   - `getKanban`/`getGantt` раніше **взагалі не фільтрували** по перевізнику (baseQuery
     цього не робить) — тепер додано `->when($carrierId, ...)`.
   - **Drivers**: фільтр перевізника переведено з клієнтського на **серверний**
     (re-fetch), як у решти.
   - **Селектори (фронт):** об'єктний біндинг (`v-model` = повний `{id,label}`,
     без `:reduce`) + watch на `selectedCarrierId`/`carriers` — інакше vue-select
     показував сирий id замість назви. Стосується DirectionsStats/Kanban/Gantt/
     FleetGantt/DriversView.

9. **KPI problems = заявки, idle = транспорти (2026-06-22).** `kpi.fleet.problems` =
   `count()` проблемних **заявок** (збіг з `getDriversTimeline` node `problem`). Але
   `idle = total − in_transit − problemTransports`, де `problemTransports` =
   `distinct count(transport_id)` — інакше кілька проблемних заявок на одному тягачі
   занижують idle. `total`/`in_transit` — теж транспорти.

10. **Directions drill-down (2026-06-22).** Картка напрямку → `getTickets` з
    `loading_location`+`unloading_location`+`carrier_id` картки (+ виключення cancelled,
    щоб збігалось з `dir.total`). Період береться з `directions.period` (НЕ
    chartMonth/chartYear — ті можуть бути null). `carrier_legal_name` alias у
    `getDirections` (бо `Application::getCarrierNameAttribute` перехоплює `carrier_name`).

## Callsite-и

| Файл | Метод/Лінія | Призначення |
|------|-------------|-------------|
| `app/Http/Controllers/Api/Dashboard/DashboardController.php` | `kpi/directions/drivers/finance/fleet` | Тонкі делегати |
| `app/Services/Dashboard/DashboardService.php` | `getKpi` L~780 | KPI tiles |
| `app/Services/Dashboard/DashboardService.php` | `getDirections` L~907 | Directions |
| `app/Services/Dashboard/DashboardService.php` | `getDrivers` L~1010 | Drivers report |
| `app/Services/Dashboard/DashboardService.php` | `getFinance` L~1185 | Finance |
| `app/Services/Dashboard/DashboardService.php` | `getFleet` L~1293 | Fleet timeline |
| `app/Services/Dashboard/DashboardService.php` | `resolveKpiPeriod` | Shared period parser |
| `app/Services/Dashboard/DashboardService.php` | `buildCarriersFilter` | Shared carriers[] |
| `app/Services/Dashboard/DashboardService.php` | `resolveVehicleStatus` | Fleet status+днів |
| `app/Services/Dashboard/DashboardService.php` | `buildAppSegment` / `buildDowntimeSegment` / `clampDay` | Fleet segments |
| `app/Http/Requests/Dashboard/` | `KpiRequest/DirectionsRequest/DriversReportRequest/FinanceRequest/FleetRequest` | Усі від `DashboardRequest` + `period` regex |
| `routes/api.php` | L158-171 | Зареєстровані під `auth:api` |

## Поля яких НЕМАЄ у БД (свідомо не повертаємо)

| Endpoint | Поле | Причина |
|---|---|---|
| `finance` | `summary.overdue`/`overdue_clients` | немає `paid_amount` + `due_date` |
| `finance` | `summary.total`/`plan` | немає partial payments / таблиці планів |
| `finance` | `summary.currency` / `clients[].paid` | те саме + currency setting |
| `fleet` | `vehicles[].model` | немає поля у `transports` |
| `kpi`/`directions`/`fleet` | currency у `revenue`/`amount` | відкладено до setting |

## Gotchas / підводні камені

- **`waitingStatusSql()` (L~608)** — спільний CASE-вираз, що мапить driver_status
  з пріоритетом `is_problem → downtime_started_at → driver_status`. Якщо додаєш
  нові driver-status агрегації — використовуй цей хелпер, не дублюй CASE.
- **`baseQuery(filters)` (L~552)** — додає `active=true` + `archive=false` +
  опц. `manager_id/customer_id/date_range`. Нові endpoint-и (kpi/directions/drivers/finance/fleet)
  **НЕ використовують** `baseQuery` — кожен пише фільтр сам, бо потрібні різні набори
  (наприклад, у kpi `earned` треба включати архівні).
- **`fleet.segments[]` можуть перекриватися** — якщо є 2 in-progress заявки у
  одного транспорту або downtime_log накладається на trip_active. Фронтенд має
  бути готовий до накладень.
- **`work_days_total` у drivers** — поточний місяць → `now.day`, минулий → `daysInMonth`.

## Пов'язані

- [[INDEX]]
- [[downtime]] — `drivers-downtime` + idle сегменти у fleet
- [[multi-tenancy]] — дашборд читає тільки systemDB
- Tier-2 pointer: `~/.claude/projects/-Users-serhiin-Data-Source-buktrek/memory/architecture_dashboard.md`
- Спека-приклади: `data/{kpi,directions,drivers,finance,fleet}.json`
- Сесія: [[2026-05-12-dashboard-5-new-endpoints]]
