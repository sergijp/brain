---
title: "Проєкт: onchul — Квоти місць (Маршрути/Рейси) + CRUD Автопарк/Популярні рейси"
date: 2026-06-15
tags: [onchul, work, session, quotas, crud, booking]
category: session
project: onchul
status: completed
aliases: ["Квоти агентів", "trip_quotas"]
pinecone_indexed: false
---

# onchul — Квоти місць у Маршрутах/Рейсах + два CRUD у Контенті

Гілка `migrate_refact`. PHP 8.2 / Laravel 10 / Vue 3.

## Мета сесії

1. Додати два CRUD у розділ «Контент»: **Автопарк** і **Популярні рейси**.
2. Головне: реалізувати **Квоти місць** — спільний компонент для Маршрутів і Рейсів, де агенту назначаються конкретні місця автобуса, з унікальністю місць між агентами, успадкуванням Рейсом від Маршруту і впливом на пошук/бронювання.

## Виконано

| Задача | Результат |
|--------|-----------|
| CRUD «Автопарк» | Контент; назва, привʼязка до автобуса, галерея, фото, wysiwyg-текст, params (key-value JSON); hasTexts (мультимова), softDelete; новий `KeyValueField.vue` |
| CRUD «Популярні рейси» | Контент; назва, привʼязка до маршруту, активність, картинка, текст, params; softDelete (без галереї) |
| Квоти: дата-шар | Дві **нормалізовані** таблиці `route_quotas` / `trip_quotas` — рядок = одне місце (`*_id`, `member_id`, `seat_number`), `UNIQUE(*_id, seat_number)`, `INDEX(*_id, member_id)` |
| Квоти: моделі | `RouteQuota`, `TripQuota` (+ `member()` belongsTo Member); `Route::quotas()`, `Trip::quotas()` |
| Квоти: CRUD-поле `route_quotas` | `GetRouteQuotasField` (віддає `{quotas, users, busPlaces}`) + `StoreRouteQuotasField` (транзакція delete+insert, дедуп); `QuotaField.vue` (@vueform/multiselect) |
| Квоти: унікальність на фронті | Вибране місце зникає в інших рядках; вибраний агент зникає в інших рядках (`seatOptions(i)` / `agentOptions(i)`) |
| Квоти: вкладка «Квоти» | У `RoutesCrudController` + `TripsCrudController` (update-only) |
| Квоти: успадкування | `Route::createTrip()` копіює `route_quotas` → `trip_quotas` поряд із цінами |
| Квоти: логіка пошуку/броні | Фільтр у `TripsService::getTripPlaces` (єдиний chokepoint, адмін+публіка) + серверне блокування у `BookingService::bookOriginal` (`assertSeatsAllowedByQuota`, кидає `BookedPlacesException`) |
| Квоти: тести | `tests/Unit/Quota/QuotaRuleTest.php` — 15/15, **pure-unit без БД** (in-memory моделі через `setRelation`, рефлексія приватних методів, stub `hasPermissionTo`) |

## Важливі рішення (ADR)

| Рішення | Чому |
|---------|------|
| Дві окремі таблиці замість поліморфної | Гарячий шлях завжди на боці Рейсу; прямі FK + нативні індекси швидші й чистіші за `quotable_type` у кожному WHERE |
| Нормалізація: рядок = одне місце (не `seats JSON`) | `UNIQUE(*_id, seat_number)` дає унікальність на рівні БД; обидва запити («місця агента», «хто тримає місце N») — індексовані int-лукапи без парсингу JSON |
| FK = `member_id` → `members` | У проєкті **немає таблиці `users`**; auth-провайдер = `App\Entities\System\Member` (guard `api`, Passport). Усі FK у коді ведуть на `members`. Колонку назвали `member_id` за конвенцією |
| Bypass квот = наявне право `trips-skip-rules-onsearch` | Не плодити нове право; «хто має право бачити все — ігнорує квоти» |
| Адмін бачить усі місця (квоти ігноруються) | За дизайном: `AuthServiceProvider` має `Gate::before`, що дає ролі `admin` усі права → bypass завжди true для адміна. Тестувати фільтр треба під роллю `agent` |

**Правило фільтрації (єдине, у відображенні й у блокуванні):**
```
bypass        = member && member->hasPermissionTo('trips-skip-rules-onsearch')
mineSeats     = quota seat_number де member_id == member.id
allQuotaSeats = усі quota seat_number рейсу
if bypass            -> усі місця
elif mineSeats != [] -> лише місця ∈ mineSeats        (агент зі своєю квотою)
else                 -> місця ∉ allQuotaSeats         (агент без квоти: ховаємо чужі квотні)
empty quotas         -> no-op
```

## Проблеми й як вирішили

- **`user_id` vs `members`**: спочатку поле назвали `user_id` (за дослівним ТЗ), але таблиці `users` нема — навели FK на `members` і за рішенням користувача перейменували колонку на `member_id` по всіх файлах (міграції/моделі/препроцесори/Vue). Міграцію ще не запускали — зміна дешева.
- **`Sfdump` ламав entry на редагуванні Route**: у `app/Crud/Resources/EntryResource.php` у `catch` стояв залишковий `dump($e)`, що підмішував VarDumper-HTML у JSON. Замінили на `report($e); throw $e;`. Дорогою знайшли й полагодили null-небезпеку `Bus::getPlaces()` → `collect($this->places['places'] ?? [])`.
- **`Cannot read 'internal_name' of undefined`** у таблиці результатів пошуку: `TripsTableManager.vue` читає `trip.route.internal_name`, але `TripsService::getTrips` не робив eager-load `route` (був лише `whereHas('route')`). Latent-баг refactor-гілки, виплив після `npm run build`. Додали `'route'` в обидва `with([...])`. **Не** регресія квот.
- **«Квоти не працюють» (усі 50 вільні)**: причина — тест під `admin` (member 1), який через `Gate::before` має bypass. Під `agent` (member 2) фільтр дав рівно 1 вільне з 50. Підтверджено наживо тимчасовим `[QUOTA]`-логом, потім лог прибрано.

## Артефакти

**Нові файли (Квоти):**
- `database/migrations/2026_06_10_120200_create_route_quotas_table.php`
- `database/migrations/2026_06_10_120300_create_trip_quotas_table.php`
- `app/Entities/System/RouteQuota.php`, `app/Entities/System/TripQuota.php`
- `app/Crud/PreProcessors/Get/GetRouteQuotasField.php`, `app/Crud/PreProcessors/Store/StoreRouteQuotasField.php`
- `resources/js/crud/base/fields/quotas/QuotaField.vue`
- `tests/Unit/Quota/QuotaRuleTest.php`

**Змінені (Квоти/логіка):** `Trip.php` (relation + `quotaSeatNumbers`/`quotaSeatNumbersForMember`), `Route.php` (relation + copy у `createTrip`), `TripsService.php` (`filterPlacesByQuota` + eager-load `route`/`quotas`), `BookingService.php` (`assertSeatsAllowedByQuota`), `RoutesCrudController.php`, `TripsCrudController.php`, `fields.js`, переклади (`crud/base/fields`, uk+en).

**Виправлення:** `app/Crud/Resources/EntryResource.php`, `app/Entities/System/Content/Bus.php`.

**Нові файли (CRUD Автопарк/Популярні):** міграції `autoparks`/`popular_routes`, моделі `Autopark`/`PopularRoute`, контролери, `KeyValueField.vue`.

**Команди / ручні кроки (ще не виконані):**
- `php artisan migrate` — створити `route_quotas`, `trip_quotas` (+ autoparks/popular_routes)
- `php artisan db:seed --class=Database\Seeders\PermissionsTableSeeder` — права autoparks/popular-routes
- `npm run build` — `QuotaField.vue`, `KeyValueField.vue`
- `./vendor/bin/phpunit tests/Unit/Quota/QuotaRuleTest.php` — 15/15

## Незавершене / next steps

- Запустити міграції + seeder + build (не робив без явного дозволу).
- Призначити нові права ролям (`admin`/`staff`) через UI або `RolesTableSeeder`.
- Едж: при зміні автобуса сутності на менший — старі `seat_number` поза новою схемою не показуються в опціях; авточистку stale-квот не робили (поза скоупом).
- Коміт ще не робив (за правилами — лише за явним запитом).

## Пов'язані нотатки

- [[10-Work/Projects/onchul/sessions/2026-06-01-laravel12-vue-migration]]
- [[10-Work/Projects/onchul/sessions/2026-06-01-driver-strip-member-and-fields]]
- [[10-Work/Projects/onchul/decisions/2026-06-01-station-time-native-time-column]]
