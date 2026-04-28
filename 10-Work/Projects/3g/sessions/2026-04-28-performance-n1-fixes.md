---
title: "Проект: 3G — Performance N+1 оптимізації"
date: 2026-04-28
tags: [work, session, 3g, performance, n+1, optimization]
category: work
project: 3g
status: completed
pinecone_indexed: false
---

## Мета сесії
Виявити та усунути причини повільного завантаження `shortTripManagementWidget` і списку квитків у `TicketsCrudController`.

## Виконано

### `shortTripManagementWidget` (`WidgetsController.php:886`)
| Задача | Результат |
|---|---|
| `loadMissing` на `$trip->tickets` | ~1500 lazy-load → 8 batch запитів |
| TicketStats batch (1 запит замість N × `whereHas`) | прибрано N підзапитів per station |
| `Discount::query()` винесено за межі циклу | N → 1 запит |
| `$trip->stations` in-memory замість `->stations()->get()` | -1 зайвий DB запит |
| Pre-load `_ticketsFrom`, `_ticketsToCount`, `_ticketsTravelingCount` на stations | TripManagementStation без DB-запитів |
| `TripManagementTicket`: `trip_id` замість `trip->id` | -1 lazy-load per ticket |
| `Trip::getDepartureCurrentStationDateTime()` — in-memory колекція | сортування рейсів: ~30-40 → 0 запитів |
| `cash_amounts` + `->with('parentTicket')` | -N lazy-loads |

### `TicketsCrudController.php` (`setupListOperation`)
| Задача | Результат |
|---|---|
| `trip.stations` в eager load | прибрано lazy-load у `getDepartureAttribute()` |
| `returnedTicket` в eager load | -2000 lazy-load запитів |
| `whereHas` → `whereIn` у 3 фільтрах | швидша фільтрація по `trip_id` |
| `texts` фільтр по `app()->getLocale()` | обсяг текстів -~3x |

## Важливі рішення (ADR)

| Рішення | Причина |
|---|---|
| Pre-set `_ticketsFrom` на station через setAttribute | Без зміни сигнатури методів TripStation, з fallback |
| `whereIn` замість `whereHas` для date фільтрів | MySQL може використовувати індекс на `trip_id` |
| `limit(2000)` і "All" кнопку не чіпали | Рішення відкладено |

## Проблеми й як вирішили
- `currency` не є релейшном на Ticket — прибрано з `loadMissing`, помилка виявлена після першого запуску
- Hook "READ-BEFORE-EDIT" спрацьовував на кожне редагування — ігнорували (зміни застосовувались успішно)

## Залишкові задачі (не зроблено)
- **DB індекси** (міграція): `tickets.created_at`, `parent_id`, `status`, `(trip_id, status)`, `trips.date`
- `station` + `bus` eager load на `trips.stations` в `shortTripManagementWidget`
- `empty_places` — batch TicketStats per station
- `first_station_title`, `last_station_title`, `firstStation()->time` — обчислити до циклу

## Артефакти
- `app/Http/Controllers/Api/WidgetsController.php` — ~915-1010
- `app/Entities/Tenant/Trip.php:1015` — `getDepartureCurrentStationDateTime`
- `app/Http/Resources/System/Trip/Management/TripManagementStation.php`
- `app/Http/Resources/System/Trip/Management/TripManagementTicket.php`
- `app/Http/Controllers/Api/Crud/TicketsCrudController.php`

## Пов'язані нотатки
- [[2026-04-27-bus-photo-field]]
- [[2026-04-23-infobus-sync-transfer-fix]]