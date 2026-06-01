---
title: "Проєкт: onchul — час станцій JSON → нативний MySQL TIME"
date: 2026-06-01
tags: [onchul, work, session]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

# onchul — час станцій JSON → нативний MySQL TIME

## Мета сесії

Перевести зберігання часу виїзду/прибуття (`time` / `time_arrival`) у таблицях `route_station` та `trip_station` зі застарілого JSON-формату `{"HH":"08","mm":"00"}` на коректний тип. Гілка `migrate_version`.

## Виконано

| Задача | Результат |
|--------|-----------|
| Аналіз поточної логіки часу | Це час доби, повна дата = `trip.date + trip_day + HH:mm`; 5 raw-SQL з `JSON_EXTRACT`, інтерфейс `{HH,mm}` у PHP/Vue/API |
| Новий cast `App\Casts\TimeOfDay` | БД `TIME` ↔ PHP `['HH'=>'09','mm'=>'45']` (zero-pad, толерантний до рядка) |
| Create-міграції route_station/trip_station | `string` → `time` default `'08:00:00'` (для свіжих інсталяцій) |
| Конвертаційна міграція | `2026_06_01_000000_convert_station_time_to_time_type` — ідемпотентна (guard по `DATA_TYPE`), `MAKETIME(...)`, з `down()` |
| Перемкнено cast у моделях | `RouteStation`, `TripStation`: `time`/`time_arrival` → `TimeOfDay::class` |
| Спрощено raw-SQL | `Trip.php` (date_from/date_to), `TripsCrudController` (×2), `TicketsCrudController` → `TIMESTAMP(date, time)` |
| Конвертація даних виконана | 361+ рядків, типи колонок тепер `time`, дані коректні |

## Важливі рішення (ADR)

- [[10-Work/Projects/onchul/decisions/2026-06-01-station-time-native-time-column]] — зберігати як нативний `TIME` + cast-обгортка `{HH,mm}` для мінімального блас-радіусу.

## Проблеми й як вирішили

- **Дані містять і числовий `HH` (`{"HH":9}`), і рядковий (`"08"`)** — конвертація через `JSON_UNQUOTE`+`CAST AS UNSIGNED` обробляє обидва. Сухий прогон `SELECT` підтвердив 0 проблемних/поза-діапазоном рядків перед мутацією.
- **`php artisan migrate` падає на сторонній міграції** `2024_11_11_200000_create_ticket_returned_table` (`Table already exists`) — наявна проблема середовища (out-of-order міграція без запису), НЕ повʼязана зі зміною. Обійшов через `migrate --path=...`. **Follow-up:** полагодити запис у таблиці `migrations`.
- **Pint переформатовував цілі старі файли** (Trip.php — 230 рядків шуму) — відкотив через `git checkout` і застосував лише точкові правки; Pint лишив тільки на 2 нових файлах. Підсумковий diff: 15+/13−.

## Артефакти

**Нові файли:**
- `app/Casts/TimeOfDay.php`
- `database/migrations/2026_06_01_000000_convert_station_time_to_time_type.php`

**Змінені:** `RouteStation.php`, `TripStation.php`, `Trip.php`, `TripsCrudController.php`, `TicketsCrudController.php`, дві create-міграції станцій.

**Команди:**
- `php artisan migrate --path=database/migrations/2026_06_01_000000_convert_station_time_to_time_type.php`
- Верифікація: cast read `{"HH":"09","mm":"45"}` → `09:45`; raw-SQL `date_from=2025-09-08 08:00:00`, `date_to=...14:30:00`; write round-trip ок.

## Незавершене / next steps

- Ручна перевірка в адмінці: CRUD round-trip часу станцій у формі маршруту + пошук рейсів на фронті.
- Полагодити сторонню `ticket_returned` міграцію, щоб `php artisan migrate` проходив без `--path`.
- За потреби — прогнати Pint по всьому проєкту окремим коммітом.

## Пов'язані нотатки

- [[10-Work/Projects/onchul/sessions/2026-06-01-laravel12-vue-migration]]
- [[10-Work/Projects/onchul/decisions/2026-06-01-station-time-native-time-column]]
