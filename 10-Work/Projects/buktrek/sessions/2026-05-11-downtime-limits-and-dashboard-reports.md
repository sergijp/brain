---
title: "Проект: buktrek — ліміти простою + дашборд-звіти (downtime, напрямки)"
date: 2026-05-11
tags: [buktrek, work, session, downtime, dashboard]
category: session
project: buktrek
status: completed
aliases: []
pinecone_indexed: false
---

# Проект: buktrek — ліміти простою + дашборд-звіти (downtime, напрямки)

## Мета сесії

1. У `GET /api/app/settings` повертати `downtime_hours_options` динамічно: відсікати години, ліміт яких водій уже вичерпав за останні 14 днів.
2. Зберегти "чесний" облік використань — щоб скасування простою через `setStep` НЕ повертало ліміт.
3. Додати дашборд-API звіту по простоям водіїв (rolling 7d + активні зверху).
4. Додати дашборд-API "напрямки → статуси" (top-20 пар `loading_location → unloading_location` з breakdown по статусам).
5. Усі тести — тільки `DatabaseTransactions`, без видалення з реальної БД.

## Виконано

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Динамічні `downtime_hours_options` у `/api/app/settings` | `DowntimeUsageService` рахує `Application.downtime_started_at`. Конфіг `downtime_limits = [45=>1, 24=>2, 11=>4, 9=>4]`, `downtime_window_days=14`. |
| 2 | Бекенд-захист на `POST /api/app/applications/set-downtime` | `SetDowntimeRequest::rules()` тепер `Rule::in(available_hours)` — не вірить клієнту. |
| 3 | Окрема таблиця `downtime_logs` (append-only журнал) | Поля: `driver_id, member_id, application_id, hours, started_at, released_at, released_by_step`. Index `(driver_id, started_at)`. Модель `App\Entities\System\Content\DowntimeLog`. |
| 4 | Перехід обліку лімітів на `downtime_logs` | `DowntimeUsageService` тепер читає з `downtime_logs`. `MemberController::setDowntime` INSERT-ить лог у `DB::transaction` + оновлює Application. `MemberController::setStep` закриває відкритий лог (`released_at`, `released_by_step`). Скасування БІЛЬШЕ НЕ повертає ліміт. |
| 5 | API `GET /api/system/dashboard/drivers-downtime` | Звіт по водіям за rolling 7д + активні простої зверху (за давністю open-логу), решта — за `total_hours DESC`. `breakdown` будується динамічно з конфіга годин. |
| 6 | API `GET /api/system/dashboard/routes-statuses` | Топ-20 напрямків `loading_location → unloading_location` з breakdown по статусам (через `DashboardRequest` фільтри: `manager_id, customer_id, carrier_id, date_range, year, month, search_query`). |
| 7 | Тести з `DatabaseTransactions` | 32 тести (DowntimeUsageServiceTest 8, SettingsEndpointTest 4, DriversDowntimeTest 8, RoutesStatusesTest 12). Лічильники таблиць `applications/drivers/members/carriers/customers/downtime_logs` повертаються незмінними. |

## Важливі рішення (ADR)

| # | Питання | Рішення | Чому |
|---|---------|---------|------|
| 1 | Як обліковувати використання простою — з полів `applications.downtime_*` чи окремою таблицею? | Окрема append-only `downtime_logs` (див. [[10-Work/Projects/buktrek/decisions/2026-05-11-downtime-logs-append-only]]) | Поля на `Application` обнуляються через `setStep` — лімит "повертався" після скасування. Журнал дає чесний 14-денний підрахунок. |
| 2 | Сортування дашборду drivers-downtime | Активні зверху (за давністю open-логу), потім за `total_hours DESC` | На дашборді важливіше побачити "хто стоїть зараз", ніж тижневі агрегати. |
| 3 | Як уникнути хардкоду годин у запитах | Pivot у PHP замість `CASE WHEN hours=45/24/...` | Додавання нового набору годин у конфіг автоматично відображається в API без правок SQL. |
| 4 | Лімітування напрямків у routes-statuses | Top-20 за `total` DESC (без параметра `?limit`) | YAGNI — додамо параметр, якщо UI потребуватиме. |
| 5 | Не комітити Pint cosmetic поза скоупом | Відкочував `routes/api.php`, `AppServiceProvider.php` після Pint у попередньому раунді; у поточному ці файли залишені з косметикою (acceptable за зв'язком з логічними змінами). | Збереження чистих дифів коміту. |

## Проблеми й як вирішили

- **Auto-mode заборонив `git checkout --` після Pint**
  - **Причина:** harness класифікує `checkout --` як деструктивний (втрата неcommitted змін).
  - **Фікс:** у попередньому раунді користувач сам зробив коміт після перевірки. У поточному раунді — залишив cosmetic як є, попередив користувача в звіті.

- **Pint масово переформатовував файли поза скоупом (`routes/api.php`, `MemberController.php`)**
  - **Причина:** Pint не знає про "скоуп задачі", переформатовує що може.
  - **Фікс:** оркестратор перевіряє `git diff -w --stat` після Pint і повідомляє про обсяг косметики; рішення приймає користувач перед комітом.

- **Application factory падає на NOT NULL колонках**
  - **Причина:** не всі поля nullable (`type_transport`, `status`, `loading_date`, `loading_time`).
  - **Фікс:** `makeApp()` хелпери в тестах заповнюють обов'язкові поля дефолтами (`domestic`, `confirmed`, `2026-05-10`, `08:00`).

- **`from()` як private-метод у тесті конфліктував з `TestCase::from()`**
  - **Причина:** базовий `Illuminate\Foundation\Testing\TestCase` має `public function from(string $url)` для HTTP-тестів.
  - **Фікс:** перейменував у `locFrom()`/`locTo()`.

## Артефакти

### Нові файли
- `app/Entities/System/Content/DowntimeLog.php` — модель журналу простоїв.
- `app/Services/AppApi/Services/DowntimeUsageService.php` — сервіс підрахунку лімітів.
- `database/migrations/2026_05_11_120000_create_downtime_logs_table.php` — таблиця.
- `tests/Unit/AppApi/DowntimeUsageServiceTest.php` — 8 unit-тестів.
- `tests/Feature/AppApi/SettingsEndpointTest.php` — 4 feature-тести.
- `tests/Feature/Dashboard/DriversDowntimeTest.php` — 8 feature-тестів.
- `tests/Feature/Dashboard/RoutesStatusesTest.php` — 12 feature-тестів.

### Змінені файли
- `config/crud.php` — `downtime_limits`, `downtime_window_days`.
- `app/Providers/AppServiceProvider.php` — singleton bind для `DowntimeUsageService`.
- `app/Services/AppApi/Services/SettingsService.php` — підставляє `available_hours` для водія.
- `app/Services/AppApi/Requests/SetDowntimeRequest.php` — динамічна `Rule::in`.
- `app/Services/AppApi/Controllers/MemberController.php` — `setDowntime`/`setStep` працюють з `downtime_logs` у транзакції.
- `routes/api.php` — нові роути `drivers-downtime`, `routes-statuses`.
- `app/Http/Controllers/Api/Dashboard/DashboardController.php` — методи `driversDowntime`, `routesStatuses`.
- `app/Services/Dashboard/DashboardService.php` — `getDriversDowntime`, `getRoutesStatuses`.

### Команди
```bash
php artisan migrate    # створення downtime_logs
./vendor/bin/phpunit --filter "DowntimeUsageServiceTest|SettingsEndpointTest|DriversDowntimeTest|RoutesStatusesTest"
# → 32/32 passed; counts unchanged
```

### Коміти
- `f948ce4` — feat(downtime): rolling 14-day per-driver limits (через `applications.downtime_started_at`).
- `41061b8` — перехід на таблицю `downtime_logs` (commit зробив користувач).
- Uncommitted на момент завершення: `drivers-downtime` API + `routes-statuses` API + їх тести.

### Нові ендпоінти API
- `GET /api/app/settings` — поведінка: повертає `downtime_hours_options` з відсічними використаними лімітами.
- `POST /api/app/applications/set-downtime` — поведінка: створює `downtime_logs` запис.
- `POST /api/app/applications/set-step` — поведінка: закриває відкритий лог.
- `GET /api/system/dashboard/drivers-downtime` — НОВИЙ.
- `GET /api/system/dashboard/routes-statuses` — НОВИЙ.

## Пов'язані нотатки

- [[10-Work/Projects/buktrek/project-overview]]
- [[10-Work/Projects/buktrek/docs/INDEX]]
- [[10-Work/Projects/buktrek/docs/downtime]] — новий arch-doc (deep-dive по downtime-журналу і лімітам).
- [[10-Work/Projects/buktrek/decisions/2026-05-11-downtime-logs-append-only]] — ADR.
- [[10-Work/Projects/buktrek/docs/mobile-api]] — стандартний контекст AppApi.
