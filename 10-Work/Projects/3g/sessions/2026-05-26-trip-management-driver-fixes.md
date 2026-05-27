---
title: "Проект: 3g — Trip Management driver fixes"
date: 2026-05-26
tags: [3g, work, session, trip-management, driver]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Доопрацювання driver-інтерфейсу управління рейсом: фільтрація по `checked`, сортування місць, очищення git worktrees.

## Виконано

| Задача | Результат |
|--------|-----------|
| Додати `free_places` до `loadBusPlaces` | Додано ключ у response — дані вже були на `$trip->free_places` після `getAdditionalOptionsTrip()` |
| Видалити застарілі git worktrees | Видалено 3 locked worktrees з `.claude/worktrees/` через `git worktree remove -f -f` |
| `tickets_traveling` — фільтр по `checked = 1` | `WidgetsController` pre-compute та fallback `getTicketsTravelingChecked()` у `TripStation` |
| `tickets` у `TripManagementStation` — сортування по місцю | `sortBy('place')->values()` в resource |
| `report.tickets` — фільтр `checked = 1` + сортування | `filter(fn($t) => $t->checked)->sortBy('place')->values()` у `WidgetsController` |

## Важливі рішення

| Рішення | Обґрунтування |
|---------|---------------|
| `tickets_traveling` залишили як count (не collection) | Фронтенд використовує як число — не можна змінювати |
| Fallback метод `getTicketsTravelingChecked()` у `TripStation` | `TripManagementStation` resource використовується з 3 контролерів, pre-compute є лише в `WidgetsController` |
| Фільтрація в resource а не в моделі | Простіше, не змінює контракт `getTicketsFrom()` |

## Артефакти

- `app/Crud/Operations/TripManagementOperation.php` — додано `free_places` у response `loadBusPlaces`
- `app/Entities/Tenant/TripStation.php` — додано метод `getTicketsTravelingChecked()`
- `app/Http/Resources/System/Trip/Management/TripManagementStation.php` — сортування `tickets`, fallback для `tickets_traveling`
- `app/Http/Controllers/Api/WidgetsController.php` — pre-compute `_ticketsTravelingCount` та `report.tickets` по `checked = 1` + sort

## Пов'язані нотатки

- [[project_performance_optimizations]] — N+1 та eager loading в тому ж контролері