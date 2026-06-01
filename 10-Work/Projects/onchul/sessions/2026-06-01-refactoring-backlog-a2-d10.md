---
title: "Проєкт: onchul — рефакторинг-беклог (A2-A3, B4, C7-C8, D10)"
date: 2026-06-01
tags: [onchul, work, session, refactoring]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

# onchul — рефакторинг-беклог по кроку

## Мета сесії

Продовження роботи над VTS (гілка `migrate_version`). Після фундаменту (час станцій → нативний `TIME`, денормалізація `departure_at`/`arrival_at`) — проходимо беклог із `refact.md` «по кроку», кожен пункт окремо з підтвердженням.

## Виконано

| Пункт | Результат |
|-------|-----------|
| **A2** | Видалено 3 мертвих методи дат із `Route.php` (`getDepartureDateTime`, `getStationDateTimeByStationId`, `...Arrival`) — `routes` не має колонки `date` (лише `setting_date`), `Carbon::parse(null)`=`now()`; нуль викликачів (усі споживачі — `Trip`) |
| **A3** | `Trip::getDepartureDateTimeAttribute` зведено до делегата `return $this->getDepartureDateTime();` — прибрано баг (не додавав `trip_day`) + мертвий `->format()` |
| **B4** | N+1 у `TripListResource` — `ReturnRule::where()->get()` на кожен рейс → статичний кеш `returnRules()` (по локалі) + `withContents()` (eager-load текстів). Query-log: 2 запити на весь список замість ~5×N |
| **C7** | 3 рядкові конкатенації `time['HH'].':'.time['mm']` → аксесори `time_minute_departure`/`_arrival` (`Busfor/RouteStationsResource`, `ItinerariesCrudController`) |
| **C8** | Прибрано дубльований `whereHas('route', active)` у `TripsCrudController::setupListOperation` |
| **C9** | Won't-fix: `ItineraryStation.time_arrival` — чисто display-рядок `"16:30"`, ніде не в Carbon/пошуку; конвертація зламала б фронт без виграшу |
| **D10** | Інфраструктура роутів/міграцій — `migrate` + `route:list` + `route:cache` тепер працюють (деталі нижче) |

## D10 — деталі (розрослося)

1. **Міграція** `2024_11_11_200000_create_ticket_returned_table` → ідемпотентна (`Schema::hasTable` guard). Дубль на вже наявну таблицю.
2. **`route:list` падав** на відсутньому класі → видалено мертві фронт-роути `routes-list`, `route/{slug}` (`Frontend\RoutesController` ніколи не існував).
3. **8 битих биндингів** (системний Laravel-резолв через `app('router')->getRoutes()` + `method_exists`): видалено всі 8 — мертві дублі або вимкнена BlaBlaCar-фіча, жоден без живого фронт-виклику.
4. **`route:cache` падав** на 4 дубльованих іменах → перейменовано `reports.trips`, `password.reset.form`, `profile.my-archive-orders`, `documentation` (канонічні `password.reset` POST та `page` для `{page}/{subs?}` лишилися — останнє юзає `MenuItems`).
5. **Результат:** 0 битих роутів, `route:list`/`route:cache` exit 0.

## Важливі рішення

- **A3 — делегат, не видалення:** аксесор спершу видалили (grep не показав читачів) → `BadMethodCallException`, бо generic-CRUD кличе `$trip->departure_date_time` динамічно за іменем. Урок: CRUD-аксесори не видаляти наосліп.
- **C9 won't-fix:** свідомо лишили inconsistency, бо `time_arrival` itinerary — окрема display-фіча зі своїм контрактом-рядком.
- **D10 #2 / BlaBlaCar:** `getStations` ніколи не був реалізований; належав вимкненій BlaBlaCar-інтеграції (методи закоментовані). Роути видалили, закоментовані методи + Vue-UI лишили як пауза-фічу.

## Проблеми й як вирішили

- **Хибна статична перевірка роутів** — `class_exists` без `vendor/autoload.php` + без урахування group-`namespace` давала фальшиві «MISSING». Розвʼязка: завантажувати реально зарезолвлені роути через `app('router')->getRoutes()` + `$route->getAction('controller')`.
- **route:cache блокувався дублями імен** — окремий клас проблеми, не повʼязаний із method-missing; виявлено лише після фіксу `route:list`.

## Артефакти

- Змінено: `app/Entities/System/Route.php`, `Trip.php`, `app/Http/Resources/TripListResource.php`, `Busfor/RouteStationsResource.php`, `ItinerariesCrudController.php`, `TripsCrudController.php`, `routes/api.php`, `routes/web.php`, `database/migrations/2024_11_11_200000_create_ticket_returned_table.php`
- Трекер: `refact.md` (корінь проєкту) — оновлено статуси
- Перевірки: `php artisan tinker` (query-log, route-резолв), `route:list`/`route:cache` exit 0, `php -l`

## Стан / далі

**Зроблено:** A1-A3, B4, C7-C8, D10; C9 won't-fix.
**На паузі (за рішенням користувача):** B5 (searchTrips→Resource), B6 (getTrips SQL-фільтри), D11 (тести), D12 (pint весь проєкт).

## Пов'язані нотатки

- [[2026-06-01-station-time-native-time-column]] — фундамент (час → TIME)
- [[2026-06-01-laravel12-vue-migration]]
- Auto-memory: `project-refactoring-tracker`, `project-blablacar-disabled`, `feedback-crud-dynamic-accessors`
