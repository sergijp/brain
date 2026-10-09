---
title: "Проект: Buktrek — новий крут «Вартості напрямків»"
date: 2026-09-15
tags: [buktrek, work, session, crud, directories]
category: session
project: buktrek
status: completed
aliases: ["direction_costs", "Вартості напрямків"]
pinecone_indexed: false
---

# Buktrek — крут «Вартості напрямків» (direction_costs)

## Мета сесії

Додати в розділ **Довідники** новий крут «Вартості напрямків»: селекти «Звідки» / «Куди», вартість і комісія.

Під час уточнення вимог склад полів розширився: додано ще `point_id` (пункт, може бути `null`) і вибір валюти для комісії/вартості.

## Виконано

| Задача | Результат |
|---|---|
| Аналіз | Знайдено майже ідентичний крут `route_costs` — узято за взірець, крут-система генерична, окремі `.vue` не потрібні |
| Міграція + модель | `direction_costs` + `App\Entities\System\Directories\DirectionCost` |
| Backend CRUD | `DirectionCostCrudController` + `DirectionCostRequest` + роут у `routes/api.php` |
| Frontend | `api-bridge.js`, `crud-routes.js`, `breadcrumbs.js`, `panel-card` у `Directories.vue` |
| Локалізація | `lang/uk/crud.php`, `lang/uk/permissions.php` |
| Права доступу | Міграція, що ідемпотентно створює 5 прав + запис у `PermissionsTableSeeder` |
| Тести | `tests/Feature/DirectionCostCrudTest.php` — 4 тести, 27 асертів, усі проходять |
| Перевірка | `migrate`, `route:list` (9 роутів), `npm run build`, `pint`, повний сюїт |

## Схема таблиці

| Поле | Тип | Джерело селекту |
|---|---|---|
| `from_id` | FK nullable → `border_crossing_points` | Міста, attribute `title`, фільтр `active=true` |
| `to_id` | FK nullable → `border_crossing_points` | Міста, attribute `title`, фільтр `active=true` |
| `point_id` | FK nullable → `points` | Пункти, attribute `name` |
| `cost` | `decimal(10,2)` nullable | — |
| `commission` | `decimal(10,2)` nullable | — |
| `currency_id` | FK nullable → `currencies` | attribute `code`, фільтр `active=true` |

Усі FK — `onDelete('set null')`, модель із `SoftDeletes`.

## Важливі рішення

| Рішення | Чому |
|---|---|
| Копіювати структуру `route_costs`, а не узагальнювати два круди в один | Різна семантика й різні набори полів; передчасна абстракція ускладнила б обидва |
| Права заводити окремою міграцією, а не сидером | `PermissionsTableSeeder.run()` починається з `Permission::query()->delete()` — на живій БД зніс би всі права й зв'язки ролей |
| `forceCreate()` замість `firstOrCreate()` у міграції прав | У моделі `Permission` `$fillable = ['name']`, тому `guard_name` відсіюється mass assignment → MySQL 1364 |
| Права іншим ролям не роздавати автоматично | Роль `admin` і так проходить через `Gate::before`; решта — рішення користувача через крут «Права» |
| Не копіювати закоментований `searchLogic` з `RouteCostCrudController` | Там це неробочий пошук по містах (назви живуть у `texts` через `ModelHasTexts`) — копіювати баг не варто |
| Іконка `exchange-alt-solid.svg` | `route-solid.svg` уже зайнятий крутом «Вартості маршрутів» — картки в Довідниках були б однакові |

## Проблеми й як вирішили

**1. Міграція прав падала з `SQLSTATE[HY000] 1364: Field 'guard_name' doesn't have a default value`.**
`Permission::firstOrCreate(['name' => ..., 'guard_name' => 'api'])` відсіює `guard_name` через `$fillable = ['name']`. Spatie-шний `findOrCreate()` не допоміг — він теж іде через mass assignment. Розв'язано `forceCreate()` з попередньою перевіркою на існування.

**2. Знайдено побічний баг (не чіпав, окрема картка в Backlog).**
`PermissionsTableSeeder` непрацездатний: через ту саму причину падає на першому ж `insert`, але перед тим уже виконав `Permission::query()->delete()`. Плюс у його списку `PERMISSIONS` немає `route_costs` — на чистій інсталяції той крут лишиться без прав.

**3. Повний тестовий сюїт має 3 падіння.**
Перевірено через `git stash -u` — ті самі 3 падають і на чистому дереві (`DriversDowntimeTest`, `ApplicationStepsResolverTest`). Тести залежать від даних дев-БД; новий код падінь не додав.

## Артефакти

Нові файли:
- `database/migrations/2026_09_15_000000_create_direction_costs_table.php`
- `database/migrations/2026_09_15_000001_add_direction_costs_permissions.php`
- `app/Entities/System/Directories/DirectionCost.php`
- `app/Http/Controllers/Api/Crud/Directories/DirectionCostCrudController.php`
- `app/Http/Requests/CRUD/Directories/DirectionCostRequest.php`
- `tests/Feature/DirectionCostCrudTest.php`

Змінені файли:
- `routes/api.php`, `lang/uk/crud.php`, `lang/uk/permissions.php`, `database/seeders/PermissionsTableSeeder.php`
- `resources/js/api-bridge.js`, `resources/js/router/crud-routes.js`, `resources/js/config/breadcrumbs.js`, `resources/js/views/base/Directories.vue`

Команди:
```bash
php artisan migrate
npm run build
./vendor/bin/pint
./vendor/bin/phpunit --filter DirectionCostCrudTest
```

## Чек-лист «як додати новий крут у Buktrek»

1. Міграція + модель у `app/Entities/System/Directories/`
2. `Request` у `app/Http/Requests/CRUD/Directories/`
3. `CrudController` у `app/Http/Controllers/Api/Crud/Directories/`
4. `$router->crud('<name>', '...')` у `routes/api.php`
5. `CrudApi('<name>')` у `resources/js/api-bridge.js`
6. `CrudRoutes('<name>', { prefix: '/directories' })` у `resources/js/router/crud-routes.js`
7. Блок у `resources/js/config/breadcrumbs.js`
8. `<panel-card>` у `resources/js/views/base/Directories.vue`
9. Ключі в `lang/uk/crud.php` і `lang/uk/permissions.php`
10. **Права в БД** — інакше `can:<name>-read` закриє крут для всіх, крім ролі `admin`

## Пов'язані нотатки

- [[project-overview]]
- [[2026-06-22-dashboard-kpi-directions-currency-drilldown]]
