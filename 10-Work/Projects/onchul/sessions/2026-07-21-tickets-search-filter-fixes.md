---
title: "Проект: onchul — Фікс QueryException у пошуку квитків + фільтр маршруту"
date: 2026-07-21
tags: [onchul, work, session, crud, tickets, filter]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Виправити критичний баг у CRUD квитків (ambiguous 'id' при сортуванні за departure + глобальний пошук) та додати новий фільтр у список квитків для пошуку за маршрутом рейсу.

## Виконано

| Задача | Результат |
|--------|-----------|
| **Баг: ambiguous 'id'** при сортуванні + пошуку | ✅ Виправлено в `TicketsCrudController.php` (префікси таблиць `tickets.` у searchLogic) |
| **Фіча: фільтр «Маршрут»** у списку квитків | ✅ Додано select_from_array фільтр в `setupListOperation()` |
| **Тести** на обидві задачі | ✅ 2 нові feature-тести, усі зелені |

## Важливі рішення (ADR)

| Рішення | Чому | Альтернативи |
|---------|------|--------------|
| Фікс **тільки** в `TicketsCrudController.php`, не в generic CRUD-шарі | Амбіґуітет виникає лише у цьому контролері: sortLogic JOIN'ує trips і trip_station, а searchLogic не кваліфіковував `id`/`number` стовпців. Generic ListOperation коректна. | Фіксити в ModelsHelper::applySearchQuery (перефіксити весь generic шар) — надто широко, ризик регресій |
| Фільтр маршруту через **whereHas**, не raw JOIN | Уникаємо додаткових JOIN'ів, які могли б конфліктувати з sortLogic (już JOIN'ує trips і станції). whereHas(':trip') — чисто і безпечно. | Raw `join('trips')` у filterLogic — ризик перехрестя з JOIN'ами в sortLogic, повтор ambiguous-column |
| Активні маршрути — використаємо наявний `scopeActive()` | Механізм уже є у Route.php:390, не потребує нового коду. | Додати новий scope або фільтр-special-case — дублювання логіки |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| QueryException 1052 `Column 'id' in where clause is ambiguous` при sort+search | Додавали префікс таблиці `tickets.` до всіх орwhere-колонок у searchLogic: `->orWhere('tickets.id', ...)`, `->orWhere('tickets.number', ...)` тощо |
| Вибір опцій фільтра — Route::active() велика кількість маршрутів? | Select_from_array рендерить усі активні маршрути; для майбутнього: переведи на ajax-search у RoutesCrudController::routeSearch() |
| Чи дійсно глобальний RouteScope ховає потрібні маршрути для адміна? | Перевіритися, адмін має обійти scope через Gate::before — тести підтвердили що активні маршрути видні |

## Артефакти

- **Змінено:** 
  - `app/Http/Controllers/Api/Crud/TicketsCrudController.php` (фікс searchLogic + новий select_from_array фільтр 'route_id')
- **Нові тести:**
  - `tests/Feature/Crud/TicketsListSortDepartureWithSearchTest.php` (3 кейси: asc/desc + пошук)
  - `tests/Feature/Crud/TicketsSearchRouteFilterTest.php` (3 кейси: фільтр лише своїм маршрутом, скалярне значення, комбо з sort)
- **Міграції:** немає
- **Команди:** `./vendor/bin/phpunit tests/Feature/Crud/TicketsListSortDepartureWithSearchTest.php`, `./vendor/bin/phpunit tests/Feature/Crud/TicketsSearchRouteFilterTest.php` — обидві зелені

## Пов'язані нотатки

- [[CRUD динамічні аксесори]] — generic CRUD викликає методи за іменем; обидва фільтри/sort коректні з point of view框架
- [[Система прав-ролей]] — фільтр маршруту фільтрує за наявним scopeActive, адмін обходить через Gate::before

## Примітки

- **Не закомічено** (за правилом: коміт лише за явним проханням користувача).
- **Follow-up:**
  - Для великої кількості маршрутів: миграція select_from_array на ajax-search в RoutesCrudController.
  - Звірити, що всі інші контролери з JOIN'ами в sortLogic також мають квалісіковані пошукові колонки (потенційна регресія-точка для подальшого аудиту).
