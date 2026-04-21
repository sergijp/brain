---
title: "Проект: air-trans — Рефакторинг TripsDispatcherCrudController (N+1, дублювання)"
date: 2026-04-21
tags: [work, session, air-trans, backend, refactor, performance]
category: work
project: air-trans
status: completed
pinecone_indexed: false
---

# TripsDispatcherCrudController — рефакторинг

## Мета сесії

Оптимізувати контролер диспетчерського екрана рейсів: прибрати N+1 при завантаженні квитків, винести дубльовану логіку групування по автобусах, уніфікувати date-фільтри. Зберегти існуючий контракт API.

## Виконано

| Крок | Опис | Статус |
|---|---|---|
| 1 | Приватна константа `TICKET_EAGER` для `TicketResource` | ✅ |
| 2 | Приватний метод `buildBusGroup()` — єдиний source of truth для шейпу групи | ✅ |
| 3 | Прибрано окремий `Bus::whereIn(...)` у `getFilteredTickets` (читаємо з eager-loaded relation) | ✅ |
| 4 | Винесено `applyDateFilter(Builder, string)` — дубль DTD+tickets WHERE | ✅ |
| 5 | Accessor `is_planned` на Trip замість `withExists` | ❌ SKIPPED |
| 6 | `whereDate('date')` → `where('date')` | ❌ SKIPPED |
| 7 | Refactor `getTripsTickets` — прибрано dead code, повний eager-load | ✅ |

## Важливі рішення (ADR)

| # | Рішення | Причина |
|---|---|---|
| 1 | Тримати обидва: `withExists is_planned` + `withAggregate planned_id` | `is_planned` читається на фронті через `ButtonManager.vue` `show_attribute`. Заміна через `$appends` на моделі Trip торкнулась би ВСІХ серіалізацій Trip у проекті. MySQL два однакові корельовані EXISTS-підзапити оптимізує подібно, тому реальна вигода мінімальна. |
| 2 | Не міняти `whereDate` на `where` | `tickets.date` — тип `DATETIME` (див. міграцію `2025_02_27_103312_create_tickets_table.php`). `where('date', '2026-04-21')` не матчить `'2026-04-21 00:00:00'` надійно. `driver_trip_dates.date` — тип `DATE`, але там уже `where` використовується. |
| 3 | Канонічний eager-load: `client, contactPerson, flight, bus, from.texts, to.texts, trip.texts, driverTripDate.bus, driverTripDate.driver` | `TicketResource::toArray()` читає всі ці поля. Пропущені в старому коді: `client`, `contactPerson`, всі `.texts`, `driverTripDate.bus/driver`. Це N+1 помноження на кількість квитків. |
| 4 | Dead code `$settingsUser` / `$user` прибрано з `getTripsTickets` | Змінні не використовувались, статичний аналіз підсвічував. Підтверджено з користувачем. |

## Проблеми й як вирішили

| Проблема | Рішення |
|---|---|
| MySQL `server has gone away` на introspection `settings` table | Визначено як окрема проблема з'єднанням/Docker. Не пов'язано з рефакторингом — це schema introspection (Doctrine DBAL). Залишено користувачу на діагностику `wait_timeout` / `docker logs db`. |
| Чи не зламає `is_planned` accessor фронт | grep `is_planned` у `resources/js/**` → знайдено `TripDispatcherList.vue` (`bus.is_planned`, працює через мій `buildBusGroup`) та `ButtonManager.vue` (`entry.is_planned` через `show_attribute`). Другий — на рівні Trip-моделі, саме його й обслуговує `withExists`. Не чіпати. |
| Пре-існуючі static-analysis warnings | Магічні методи Laravel, unused public actions (routes), unknown columns на моделях без phpdoc — NOT регресії, ігноровано. |

## Артефакти

### Змінений файл
- `app/Http/Controllers/Api/Crud/TripsDispatcherCrudController.php`
  - Нове: `TICKET_EAGER` const, `applyDateFilter()`, `buildBusGroup()`
  - Refactored: `getFilteredTickets`, `getTripTickets`, `getTripsTickets`, `setupDateSliderDefaults`, `setupListOperation` (filter function)
  - Видалено: import `SettingUser`, dead code `$user`/`$settingsUser`

### Перевірені (read-only)
- `app/Http/Resources/System/TicketResource.php` — джерело правди для eager-load
- `app/Entities/System/Directories/Ticket.php` — relations `bus, client, contactPerson, driverTripDate, flight, from, to, trip` підтверджено
- `app/Helpers/ModelHasTexts.php` — trait `texts()` relation
- `database/migrations/2025_02_27_103312_create_tickets_table.php` — `date` = DATETIME
- `database/migrations/2026_04_15_000001_create_driver_trip_dates_table.php` — `date` = DATE
- `resources/js/crud/base/operations/list/TripDispatcherList.vue` — споживач `bus.is_planned`
- `resources/js/crud/base/buttons/ButtonManager.vue` — споживач `entry.is_planned` через `show_attribute`

### План рефакторингу (artifact поза vault)
`/Users/serhiin/.claude/plans/glowing-jumping-blum.md`

## Команди верифікації

```bash
php -l app/Http/Controllers/Api/Crud/TripsDispatcherCrudController.php  # ✅ no syntax errors
php artisan test --filter TripsDispatcher                                # якщо є тести
```

UI smoke: відкрити диспетчер → список рейсів на сьогодні → відкрити рейс з 20+ квитками → призначити водія/автобус.

## Пов'язані нотатки

- [[2026-04-20-driver-trip-date-refactor]] — попередня фаза роботи над DTD
- [[2026-04-20-soft-deletes-bugfixes]]
- [[2026-04-20-ticket-checked-nullable]]
- [[trips-dispatcher-controller]] — системна документація (docs/)