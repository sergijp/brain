---
title: "Проект: air-trans — Рефактор DriverTripDate + DriverTripDateService"
date: 2026-04-21
tags: [work, session, air-trans, backend, refactor]
category: work
project: air-trans
status: completed
pinecone_indexed: false
---

## Мета сесії

Вирішити баг: при видаленні водія і повторному плануванні того самого (рейс+дата+автобус) з новим водієм — створювався дублікат DTD, а квиток залишався прив'язаний до старого (сирота без водія у UI). Розширити логіку на всі сценарії видалень Bus/Driver/DTD.

## Виконано

| Задача | Результат |
|---|---|
| Змінено identity DTD | Унікальний ключ `(trip_id, date, bus_id)` замість `(driver_id, trip_id, date)` |
| Міграція з дедупом | `2026_04_21_100845_refactor_driver_trip_dates_keys.php` — деdup активних дублікатів, hard-delete soft-deleted конфліктів, новий unique index |
| Новий `DriverTripDateService` | Вся логіка DTD/Ticket синхронізації в одному місці (upsertSlot, deleteSlot, syncTicketLink, onBusDeleted, onDriverDeleted…) |
| Новий `DriverObserver` | При soft-delete водія → `driver_id = null` на активних DTD |
| Оновлений `BusObserver` | Тепер також занулює `bus_id/dtd_id` на квитках при видаленні автобуса |
| `AppServiceProvider` | Реєстрація `DriverObserver` |
| `PlaningTripsOperation` | `planingTripsGenerate` через `upsertSlot`; `planingTripsDestroy` занулює квитки |
| `TripsDispatcherCrudController` | `assignBusDriver` (гілка без dtd_id) через `upsertSlot` |
| `TicketsCrudController` | `afterCreateAction` + новий `afterUpdateAction` через `syncTicketLink` |
| Переклади | `slot_already_taken` в uk/en |

## Важливі рішення (ADR)

| Рішення | Чому |
|---|---|
| DTD identity = (trip, date, bus) | DTD — «слот автобуса»; водій — атрибут. Квитки лишаються прив'язані при зміні водія |
| При soft-delete водія → null driver_id на DTD | DTD слот валідний, просто «без водія»; наступне планування оновить driver_id |
| При soft-delete автобуса → null bus_id+dtd_id на квитках | Квитки лишаються активними, чекають перепризначення |
| Delete DTD (планування) → null dtd_id на квитках | Дозволити видалення; квитки лишаються з bus_id |
| Delete DTD (диспетчер) → 422 якщо є квитки | Існуюча поведінка збережена |
| DriverTripDateService як центральна точка | Уникнення дублювання логіки у 4+ контролерах/observer'ах |

## Проблеми й як вирішили

| Проблема | Рішення |
|---|---|
| Міграція падала: `Can't DROP unique index` | В БД вже були застосовані попередні міграції (2026-04-17), яких немає у файлах. Спростили міграцію — лише деdup + новий індекс |
| `UniqueConstraintViolationException` при додаванні індексу | MySQL unique охоплює ВСІ рядки включно з soft-deleted. Додали hard-delete soft-deleted дублікатів перед `CREATE UNIQUE INDEX` |

## Артефакти

- `app/Services/DriverTripDateService.php` — новий
- `app/Observers/DriverObserver.php` — новий
- `database/migrations/2026_04_21_100845_refactor_driver_trip_dates_keys.php` — новий
- `app/Observers/BusObserver.php` — оновлений
- `app/Providers/AppServiceProvider.php` — оновлений
- `app/Crud/Operations/PlaningTripsOperation.php` — оновлений
- `app/Http/Controllers/Api/Crud/TripsDispatcherCrudController.php` — оновлений
- `app/Http/Controllers/Api/Crud/Directories/TicketsCrudController.php` — оновлений

## Пов'язані нотатки

- [[air-trans/sessions/2026-04-20-planing-trips-fix]] (якщо є)