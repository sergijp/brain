---
title: "onchul — Багфікси: фільтрація неактивних зупинок, дублікати при відновленні, синхронізація квот"
date: 2026-06-19
tags: [onchul, work, session, bugfix, refactoring]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
Виправити серію пов'язаних багів у системі управління маршрутами/рейсами та реалізувати відсутню синхронізацію квот.

## Виконано

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Фікс: неактивні зупинки знаходяться у пошуку | `Trip::scopeStationsQuery()` + `Route::scopeStationsQuery()` — додано SELECT аліаси `from_station_active`/`to_station_active`; PHP-фільтр у `TripsService` розширено в 2 місцях |
| 2 | Фікс: null при пошуку по видаленій станції | `getOriginalOptionsTrip` — guard після `stationById()`; nullsafe `?->` для transfer-станцій; фільтр колбек відкидає `null` trip |
| 3 | Фікс: дублікат при повторному додаванні видаленої станції | `StoreRouteStationsField` — restore soft-deleted запису замість INSERT (для Route і Trip динамічно) |
| 4 | Фікс: той самий дублікат при `SyncTripWithRouteJob` | `Trip::syncWithRoute()` — `withTrashed()` + `elseif trashed → restore()` |
| 5 | Рефакторинг: виніс логіку restore в trait | Новий `FindsOrRestoresStation` trait у `app/Entities/System/Concerns/`; підключено в `TripStation` і `RouteStation`; обидва місця використання замінено |
| 6 | Фікс: неправильний namespace `RouteStation` | `App\Entities\Tenant\RouteStation` → `App\Entities\System\RouteStation` |
| 7 | Фіча: синхронізація квот у `syncWithRoute` | Новий блок у `Trip::syncWithRoute()` — upsert по `seat_number`, prune видалених, gate через `$options` |

## Важливі рішення (ADR)

| Рішення | Варіанти | Обрано | Причина |
|---------|----------|--------|---------|
| Де фільтрувати `active` зупинки | SQL WHERE у JOIN vs PHP filter | PHP filter (SELECT аліас + умова в TripsService) | Простіше, вся логіка відсіву в одному місці |
| Дублікат станції при відновленні | Змінити unique constraint vs restore soft-deleted | Restore soft-deleted | MySQL NULL в unique — небезпечно; restore семантично правильно |
| Де розмістити restore-логіку | Inline в кожному місці vs спільний trait | Trait `FindsOrRestoresStation` | Два місця використання, уникнення дублювання |
| Перезапис квоти при синхронізації | Перезаписувати завжди vs пропускати зайняті | Перезаписувати завжди | Рішення замовника: адмін свідомо змінює |

## Артефакти

| Файл | Зміна |
|------|-------|
| `app/Entities/System/Trip.php` | `scopeStationsQuery` аліаси; `syncWithRoute` — restore + quota sync |
| `app/Entities/System/Route.php` | `scopeStationsQuery` аліаси |
| `app/Services/TripsService.php` | PHP-фільтр active (~121, ~151); guard null station (~278); filter колбек |
| `app/Crud/PreProcessors/Store/StoreRouteStationsField.php` | Динамічний restore через trait |
| `app/Entities/System/Concerns/FindsOrRestoresStation.php` | **НОВИЙ** — trait з `findTrashedOrNewForParent()` |
| `app/Entities/System/TripStation.php` | `use FindsOrRestoresStation`, `parentRelation()` |
| `app/Entities/System/RouteStation.php` | `use FindsOrRestoresStation`, `parentRelation()` |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Неактивні зупинки в пошуку; null crashes | Вибір аліасів у scopeStationsQuery + PHP-фільтр в TripsService + guard после stationById |
| Дублікати у `route_stations` / `trip_stations` при відновленні видаленої станції | Restore soft-deleted запису замість INSERT (через новий trait `FindsOrRestoresStation`) |
| `SyncTripWithRouteJob` не відновлює видалені станції | Додано `withTrashed()` + логіка restore у `Trip::syncWithRoute()` |
| Неправильний namespace для `RouteStation` в кода | Оновлено на `App\Entities\System\RouteStation` |
| Квоти не синхронізуються при зміні маршруту | Новий upsert-блок у `syncWithRoute()` з pruning видалених |

## Edge cases зафіксовані
- Проміжна неактивна зупинка B не блокує рейс A→C (фільтр лише на from/to)
- Back-trip фільтр (~151 у TripsService) теж виправлено
- `SyncTripWithRouteJob` — відновлення trashed stations при синхронізації
- `nullsafe ?->` для transfer-станцій в getOriginalOptionsTrip

## Пов'язані нотатки
- [[onchul-architecture]]
- [[onchul-quotas]]
