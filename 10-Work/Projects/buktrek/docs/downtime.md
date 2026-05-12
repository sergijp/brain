---
title: "downtime — облік простоїв водія, ліміти, дашборд"
date: 2026-05-11
tags: [buktrek, architecture, downtime, dashboard]
category: docs
project: buktrek
status: active
aliases: ["buktrek-downtime"]
pinecone_indexed: false
last_verified: 2026-05-11
---

# downtime

## Контекст

Водій з мобільного застосунку може натиснути "Простій" на активній заявці, обравши тривалість з фіксованого набору `[45, 24, 11, 9]` годин. За **rolling 14 днів** діють ліміти на кожну опцію:

| Години | Дозволено разів за 14d |
|--------|-----------------------|
| 45     | 1                     |
| 24     | 2                     |
| 11     | 4                     |
| 9      | 4                     |

Облік ведеться **append-only** у таблиці `downtime_logs` — щоб скасування простою (через `setStep`) не повертало ліміт назад. Це історичний журнал, не транзакційний стан.

На дашборді є два пов'язані звіти:
1. **drivers-downtime** — водії, які простоюють зараз або простоювали за останній тиждень.
2. **routes-statuses** — *окремий* зріз, не пов'язаний з простоями (топ напрямків по статусах).

## Модель / схема

```
Member ─┐
        ├─ Driver ─┬── Application ──┐
        └──────────┘                 │
                                     ▼
                              downtime_logs
                              (append-only)
```

Таблиця `downtime_logs`:

| Колонка | Тип | Призначення |
|---------|-----|-------------|
| `id` | bigInt PK | |
| `driver_id` | bigInt (FK drivers) | по кому рахуємо ліміт |
| `member_id` | bigInt nullable | автор простою (для аналітики) |
| `application_id` | bigInt nullable | до якої заявки прив'язано |
| `hours` | smallInt | одне зі значень `downtime_limits` |
| `started_at` | timestamp | момент `setDowntime` |
| `released_at` | timestamp nullable | заповнюється при `setStep` (NULL = простій активний) |
| `released_by_step` | string(64) nullable | новий driver_status, на який перейшли |
| `created_at`/`updated_at` | timestamps | |

Індекси:
- `(driver_id, started_at)` — для запиту лімітів і звітів.
- `(application_id)` — для пошуку open-логу при `setStep`.

Поля на `applications.downtime_started_at`, `applications.downtime_hours_proposed` **досі існують** — підтримуються синхронно для існуючого UI (на дашборді показує "поточний простій заявки"). НЕ є source-of-truth для лімітів.

## Ключові контракти

1. **Журнал append-only** — `INSERT` робиться при кожному `setDowntime`. UPDATE — лише `released_at`/`released_by_step` при `setStep`. Жодних DELETE з продакшен-коду.
2. **Скасування ≠ відкат ліміту** — після `released_at = now()` запис далі рахується у вікно 14d. Це і є ціль архітектури.
3. **Активний простій == один open-лог на заявку** — інваріант, який порушується тільки артефактами (race condition, ручні дані). `setStep` закриває "найновіший open-лог цієї заявки" (`orderByDesc('id')->limit(1)`). У звіті drivers-downtime, якщо у водія декілька open — береться найдавніший (`MIN(started_at)`).
4. **Динаміка годин** — список годин зберігається ТІЛЬКИ в `config/crud.php` (`downtime_limits` / `downtime_hours_options`). Сервіс/контролер/звіти не мають хардкоду — `array_keys(config('crud.applications.downtime_limits'))`.
5. **Бекенд завжди перевалідовує** — `SetDowntimeRequest` НЕ довіряє клієнту: повторно викликає `DowntimeUsageService::getAvailableHours($driver->id)` і робить `Rule::in($available)`.

## Callsite-и

| Файл | Метод / лінія | Призначення |
|------|---------------|-------------|
| `app/Services/AppApi/Services/DowntimeUsageService.php` | `getUsageCounts(int $driverId): array` | Group by hours за 14d з `downtime_logs`. |
| `app/Services/AppApi/Services/DowntimeUsageService.php` | `getAvailableHours(int $driverId): array` | Фільтрує конфігурні години по лімітам. |
| `app/Services/AppApi/Services/SettingsService.php` | `getSettings(Member $member)` | Викликає `getAvailableHours($member->driver->id)` для `downtime_hours_options`. |
| `app/Services/AppApi/Requests/SetDowntimeRequest.php` | `rules()` | Бекенд-захист: dynamic `Rule::in`. |
| `app/Services/AppApi/Controllers/MemberController.php` | `setDowntime` | `DB::transaction`: INSERT log + UPDATE application. |
| `app/Services/AppApi/Controllers/MemberController.php` | `setStep` | `DB::transaction`: закриває open-лог (`released_at`, `released_by_step`) + UPDATE application. |
| `app/Services/Dashboard/DashboardService.php` | `getDriversDowntime(int $days = 7)` | Звіт по водіям; active зверху. |
| `app/Services/Dashboard/DashboardService.php` | `getRoutesStatuses(array $filters)` | (НЕ простої) — топ напрямків з breakdown по статусам. |
| `app/Providers/AppServiceProvider.php` | `register()` | Singleton bind `DowntimeUsageService` з конфіг-параметрами. |

## Матриця подій

| Подія користувача | Що з `applications` | Що з `downtime_logs` |
|--------------------|--------------------|-----------------------|
| `POST /set-downtime` | `downtime_started_at = now(); downtime_hours_proposed = $hours` | `INSERT (driver_id, member_id, application_id, hours, started_at = now())` |
| `POST /set-step` (зі статусу простою) | `downtime_started_at = NULL; downtime_hours_proposed = NULL; driver_status = $step` | `UPDATE WHERE application_id = X AND released_at IS NULL ORDER BY id DESC LIMIT 1 SET released_at = now(), released_by_step = $step` |
| Інший `setStep` (не зі стану простою) | `driver_status = $step` (поля downtime_* вже null) | без змін |

## API контракт — звіти

### `GET /api/system/dashboard/drivers-downtime`

```jsonc
{
  "period": { "from": "2026-05-04T...", "to": "2026-05-11T...", "days": 7 },
  "totals": { "drivers_count": N, "active_count": N, "logs_count": N, "total_hours": N },
  "data": [
    {
      "driver_id": N, "driver_name": "...",
      "carrier_id": N|null, "carrier_name": "..."|null,
      "total_hours": N, "logs_count": N,
      "breakdown": { "45": N, "24": N, "11": N, "9": N }, // ключі = array_keys(downtime_limits)
      "active": null | {
        "application_id": N|null, "hours": N,
        "started_at": "ISO8601", "elapsed_minutes": N
      }
    }
  ]
}
```

**Сортування:** active != null (за `elapsed_minutes DESC`) → решта (за `total_hours DESC, logs_count DESC`).
**Особливість:** водій з активним простоєм, що почався поза 7-денним вікном, ВСЕ ОДНО з'являється у `data` з `total_hours=0`.

### `GET /api/system/dashboard/routes-statuses`

Не про простої, але створено в тій самій сесії. Top-20 напрямків (`loading_location → unloading_location`) з breakdown по статусам (без `cancelled`, без `archive=true`, без `active=false`, без NULL-локацій). Фільтри з `DashboardRequest`.

## Конфіг

`config/crud.php → applications`:

```php
'downtime_hours' => [9, 11, 24, 45],        // legacy-ключ, ще використовується деінде
'downtime_limits' => [45 => 1, 24 => 2, 11 => 4, 9 => 4],
'downtime_window_days' => 14,
```

Додавання нової опції (наприклад, `30 => 1`) — достатньо для:
- автоматичного відображення в `downtime_hours_options`,
- `breakdown` у дашборд-звіті,
- валідації `SetDowntimeRequest`.

## Тести

- `tests/Unit/AppApi/DowntimeUsageServiceTest.php` — 8 сценаріїв (вікно, скасування, перетин водіїв).
- `tests/Feature/AppApi/SettingsEndpointTest.php` — 4 сценарії.
- `tests/Feature/Dashboard/DriversDowntimeTest.php` — 8 сценаріїв (active outside window, multi-active edge).
- `tests/Feature/Dashboard/RoutesStatusesTest.php` — 12 сценаріїв (фільтри, top-20, null-локації).

Усі — `DatabaseTransactions`, нічого не видаляють з реальної БД.

## Пов'язані

- [[10-Work/Projects/buktrek/decisions/2026-05-11-downtime-logs-append-only]] — ADR.
- [[10-Work/Projects/buktrek/sessions/2026-05-11-downtime-limits-and-dashboard-reports]] — сесія розробки.
- [[10-Work/Projects/buktrek/docs/mobile-api]] — AppApi контекст.
- [[10-Work/Projects/buktrek/docs/INDEX]]
