---
title: "Проект: buktrek — Dashboard: дефолтний перевізник, валютне групування KPI/directions, drill-down напрямків, problems в одиницях заявок"
date: 2026-06-22
tags: [buktrek, work, session, dashboard, kpi, directions, currency]
category: session
project: buktrek
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Доробити логіку дашборду: дефолтний перевізник по замовчуванню, валютне групування фінансів у KPI та directions, drill-down з картки напрямку у спільну панель заявок, і узгодити лічильник `problems`.

## Контекст

- Сервіс: `app/Services/Dashboard/DashboardService.php` (вся логіка)
- Фронт: `resources/js/components/dashboard/` (KpiBar, TimelineView, timeline/DirectionsStats, timeline/TicketsListPanel) + `views/base/Dashboard.vue` + `api-bridge.js`
- Спільна панель заявок (Row 4 у TimelineView) перевикористовується для статус-кліків і тепер для drill-down напрямків.

## Виконано

### 1. Дефолтний перевізник (`default` flag на Carrier)

- Міграція `2026_06_18_000000_add_default_to_carriers_table` — `boolean default` після `active`.
- `Carrier`: `$fillable`/`$casts`/`logOnly` + `boot::saved()` тримає **єдиний** default (демоутить інших) + `scopeDefault()`. Дзеркалить наявний патерн Currency.
- CRUD: toggle-колонка + чекбокс у create/update, метод `toggleDefault()`, роут `carriers.toggle-default` (guard `carriers-edit`), правила у Create/UpdateCarrierRequest.
- `DashboardService::resolveDefaultCarrierId()` — fallback коли `carrier_id` не переданий (KPI і directions відкриваються pre-scoped).

### 2. Валютне групування KPI (earned/expected)

- `sumAmountByCurrency(Builder, fallbackCode)`: `leftJoin('currencies')`, group по `amount_currency_id`/`code`, повертає `list<{code, amount}>` (sort desc). Заявки без валюти → дефолтна валюта (`resolveDefaultCurrencyCode()`, fallback EUR).
- `in_transit` і `problems` — додано фільтр періоду по `loading_date` (whereYear+whereMonth).
- Фронт `KpiBar.vue` — earned/expected рендеряться кількома рядками по валютах; `CURRENCY_SYMBOLS`.

### 3. directions — валюта + перевізник (getDirections)

- `revenue` і `avg_freight` тепер **по валютах** (масив `{code, amount}`), симетрично з KPI. У pivot — `revenueByCode => [total, count]`; `avg = total/count` на валюту.
- Додано `leftJoin('carriers')` → у відповідь кожного напрямку `carrier_name`.
  - **Gotcha:** alias мусить бути `carrier_legal_name`, бо `Application::getCarrierNameAttribute()` перехоплює поле `carrier_name` і повертає CRUD-структуру `{value,label,...}`.
- Fallback на дефолтного перевізника + у відповідь `carrier_id`.
- Нульові валютні бакети (`total <= 0`) відфільтровуються на бекенді.
- Фронт DirectionsStats: рядки валют (фільтр `amount>0`), назва перевізника на картці + бейдж активного перевізника в шапці; селектор синхронізується з `selectedCarrierId`. Очищення селектора → `carrier_id = 0` («всі»), а не null (інакше бекенд знову застосує default). У Dashboard.vue `carrier_id ?? null` замість `|| null`.

### 4. Drill-down напрямку → панель заявок

- `TicketsRequest` + `loading_location`/`unloading_location` (nullable|string|max:255).
- `getTickets()`: `when()` фільтри локацій; при наявності фільтра напрямку **виключає cancelled** (щоб число збігалось з `dir.total` картки).
- `api-bridge`: `getDirectionTickets({month, year, carrier_id, loading_location, unloading_location})`.
- DirectionsStats: картка клікабельна → `direction-click` з `{from, to, carrier_id, carrier_name}`.
- TimelineView `onDirectionClick`: синтетичний `selectedStatus.label = "from → to · CarrierName"`, заповнює спільну панель, скрол до неї.
- **Carrier scoping:** передається `carrier_id` **самої картки** (важливо в режимі «всі перевізники» — один маршрут = кілька карток по перевізниках). Перевірено: маршрут на 3 перевізники → 18/3/2, кожен клік дає свій набір.

### 5. Фікс періоду drill-down

- Баг: картка рахується за період, який directions резолвить сам (default = поточний місяць), а клік передавав `chartMonth/chartYear` = null → `getTickets` без фільтра періоду → 21 замість 7.
- Фікс: зберігаємо `data.period` directions-відповіді у `timelineData.directionPeriod`; `onDirectionClick` парсить `YYYY-MM` → year/month.

### 6. KPI problems — узгодження одиниць (варіант: заявки)

- Розбіжність: KPI `problems`=1 (distinct transport), drivers-timeline node=2 (COUNT заявок). Причина: 2 проблемні заявки (#952, #1021) на **одному транспорті №5**.
- Рішення (вибір користувача): `problems` на екран = **count заявок** (= 2, як у timeline).
- `idle` і далі рахує **транспорти**: `problemTransports = distinct count(transport_id)` (=1), `idle = total − in_transit − problemTransports`. Інакше idle занижується.

### 7. Default carrier — поширення на ВСІ 6 табів

Дефолтного перевізника докотили до всіх вкладок дашборду: кожен ендпойнт без явного `carrier_id` робить fallback на `resolveDefaultCarrierId()` і повертає резолвлений `carrier_id` + `carriers`; селектор на фронті показує дефолтного вибраним.

| Таб | Метод | Що було | Що зроблено |
|---|---|---|---|
| KPI | `getKpi` | — | fallback (п.1) |
| Напрямки | `getDirections` | — | fallback + селектор (п.3) |
| Канбан | `getKanban` | **не фільтрував взагалі** | + `->when(carrier)`, +carrier_id/carriers, новий селектор у KanbanView |
| Гантт | `getGantt` | **не фільтрував взагалі** | + `->when(carrier)`, +carrier_id/carriers, новий селектор у GanttView |
| Автопарк | `getFleet` | `?? null` | дефолт + carrier_id/carriers у 3 return-и; FleetGanttView брав `routeCarriers` (формат `name`) → перейшов на власні `fleetData.carriers` |
| Водії | `getDrivers` | `?? null`, фільтр **клієнтський** | дефолт + carrier_id у 3 return-и; DriversView переведено на **серверний** фільтр (re-fetch) |

**Об'єктний біндинг селекторів (важливо).** vue-select з `:reduce="c => c.id"` при програмному проставленні моделі показував **сирий id замість назви**. Фікс: прибрати `:reduce`, біндити `v-model` на повний об'єкт `{id,label}`, синхронізувати через watch на `selectedCarrierId`+`carriers` (+ `resolveCarrierOption(id)`). Застосовано в DirectionsStats, KanbanView, GanttView, FleetGanttView, DriversView.

**Конвенція carrier_id:** `0` = «всі» (явний вибір/очищення), `null`/відсутній = застосувати default. Фронт шле `0`, не `null`, інакше бекенд знову застосує дефолт.

### 8. Finance — розділення сум по валютах (як KPI)

Таб «Фінанси» (`getFinance` / `FinanceView`) переведено на валютне групування:

- Узагальнив хелпер: `sumAmountByCurrency` → wrapper над новим `sumColumnByCurrency($q, $column, $currencyFk, $fallback)` (працює і для `amount`/`amount_currency_id`, і для `freight`/`freight_currency_id`). Нульові бакети фільтруються (там же підтягнув і KPI до фільтрації нулів).
- **summary.received/expected** — `list<{code, amount}>` по `amount_currency_id` + окремий `*_trips` count (бо breakdown тепер per-currency).
- **clients[].freight** — `list<{code, amount}>` по `freight_currency_id` (pivot по клієнту в PHP); клієнти сортуються за сумарним freight усіх валют.
- Фронт: картки received/expected/**total** (total = merge received+expected по коду) рендерять рядки по валютах; колонка freight у таблиці — рядки по валютах, `—` якщо порожньо. `currencySymbol`, прибрано хардкод `€` і клієнтський sort по числу.
- **Default carrier у finance НЕ додавав** — таб не має селектора перевізника, тихий scope був би некоректним (`?? null` = всі).

Перевірка (2026-06): received UAH=461480/EUR=81066 (46 trips), expected UAH=198826/EUR=73486 (131), КОКА-КОЛА freight UAH=200300/EUR=117030.

## Важливі рішення (ADR)

| Рішення | Чому |
|---|---|
| `default` boolean flag на Carrier (а не хардкод) | Дзеркалить патерн Currency; редагується в CRUD; one-default enforced у `boot::saved()` |
| earned/expected/revenue/avg_freight групуються по валютах | Раніше валюта ігнорувалась (складались різні валюти); тепер коректно. Знімає старий TODO "currency deferred" для kpi/directions |
| Заявки без валюти → дефолтна валюта | Уникнути втрати сум; UAH/EUR як fallback |
| KPI `problems` = заявки, але `idle` = транспорти | Збіг з drivers-timeline на екрані, але без поломки формули idle (різні одиниці навмисно) |
| drill-down використовує спільну `TicketsListPanel` | Узгоджено зі статус-кліками, мінімум коду |
| Default carrier на всіх 6 табах + об'єктний біндинг селекторів | Єдина поведінка дашборду; `:reduce` показував id замість назви |
| Drivers carrier-фільтр: клієнтський → серверний | Бекенд тепер скоупить по дефолту, тож клієнтський «всі» показував би лише дефолтного |
| Finance: summary по `amount_currency_id`, clients.freight по `freight_currency_id` | `amount` і `freight` мають РІЗНІ валютні FK — не плутати |
| Finance без default carrier | Таб не має селектора перевізника — тихий scope був би некоректним |

## Проблеми й як вирішили

- **carrier_name приходив як CRUD-об'єкт** → accessor `getCarrierNameAttribute` перехоплював alias; перейменував alias на `carrier_legal_name`.
- **drill-down видавав 21 замість 7** → відсутній фільтр періоду; пробросив `directionPeriod` з відповіді.
- **очищення селектора повертало default** → `0` як «всі», `?? null` замість `|| null`.
- **у селекті kanban відображався id замість назви** → vue-select `:reduce` + програмна модель; фікс — об'єктний біндинг (поширено на всі селектори).
- **`resolveCarrierOption` у `data()`** не може юзати computed `carrierOptions` (computed ще не готовий при init) → будувати опцію з prop `carriers` напряму.
- **temp-FS tasks переповнився (ENOSPC)** під час сесії → Bash-команди падали; обхід через `dangerouslyDisableSandbox`. Треба чистити `/private/tmp/claude-*`.

## Артефакти

- Міграція: `database/migrations/2026_06_18_000000_add_default_to_carriers_table.php`
- Бекенд: `DashboardService.php` (getKpi, getDirections, getTickets, getKanban, getGantt, getFleet, getDrivers, getFinance, `sumColumnByCurrency`, + helpers), `DashboardController.php` (kanban), `TicketsRequest.php`, `Carrier.php`, `CarriersCrudController.php`, `Create/UpdateCarrierRequest.php`, `routes/api.php`
- Фронт: `KpiBar.vue`, `DirectionsStats.vue`, `TimelineView.vue`, `KanbanView.vue`, `GanttView.vue`, `FleetGanttView.vue`, `DriversView.vue`, `FinanceView.vue`, `Dashboard.vue`, `api-bridge.js`

## Пов'язані нотатки

- [[dashboard-api]] — оновлено інваріанти (currency, default carrier, problems-units)
- [[2026-05-12-dashboard-5-new-endpoints]] — створення kpi/directions/drivers/finance/fleet
