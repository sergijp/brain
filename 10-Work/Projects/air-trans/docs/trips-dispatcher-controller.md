---
title: "Air-trans — TripsDispatcherCrudController: архітектура та логіка"
tags: [air-trans, backend, controller, dispatcher, architecture]
created: 2026-04-21
status: done
---

# TripsDispatcherCrudController — архітектура

> [!info]
> Контролер обслуговує диспетчерський екран: список рейсів на обрану дату + відкриття рейсу з квитками, згрупованими по автобусах + призначення водіїв/автобусів.
>
> Шлях: `app/Http/Controllers/Api/Crud/TripsDispatcherCrudController.php`

## Три основні сценарії

### 1. Список рейсів на дату — `setupListOperation` + `setupDateSliderDefaults`

Виводяться тільки ті рейси, які на обрану дату **мають або квитки, або DTD-слот**.

**Правило видимості рейса** (реалізовано в `applyDateFilter`, викликається з `setupDateSliderDefaults` + filter `date_slider_value`):

```php
Trip::whereHas('tickets', fn($q) => $q->where('date', $date))
    ->orWhereHas('driverTripDates', fn($q) => $q->where('date', $date)->where('active', true));
```

**Агрегати, що підвантажуються до кожного рейса:**

| Колонка | Як | Призначення |
|---|---|---|
| `adults_count` | `withSum tickets.count_adults on date=$date` | Лічильник дорослих |
| `children_count` | `withSum tickets.count_children on date=$date` | Лічильник дітей |
| `is_planned` | `withExists driverTripDates where date=$date && active=true && doesntHave('tickets')` | Булевий прапорець — чи є запланований слот БЕЗ квитків |
| `planned_id` | `withAggregate(...id)` ідентична умова | ID того слота для побудови кнопки/лінку |

> [!note]
> Обидва агрегатори залишаються з дизайну: `is_planned` — UI-прапорець, `planned_id` — FK для дій. Заміна через accessor на моделі Trip торкнулась би глобально всіх серіалізацій — не робимо.

**Фронт-споживачі `is_planned`:**

- `resources/js/crud/base/operations/list/TripDispatcherList.vue` — бейдж `{{ $t('base.planned') }}` біля групи (на рівні `bus.is_planned` у відкритому рейсі).
- `resources/js/crud/base/buttons/ButtonManager.vue` — `entry[show_attribute]` → delete-кнопка показується тільки якщо `is_planned` truthy на Trip.

### 2. Відкриття рейсу — `getTripTickets` → `getFilteredTickets`

Вхід: `trip_id`, `date`, `search`. Вихід: колекція «груп по автобусу».

**Джерела даних групи:**

1. **Квитки рейсу на дату** — групуються по `ticket.bus_id ?? ticket.driverTripDate?.bus_id`.
2. **DTD-слоти (запис у `driver_trip_dates` з `active=true`), яких нема серед квитків** — додаються як порожні групи з `is_planned: true`.

**Шейп групи** (будує `buildBusGroup()`):

```json
{
  "dtd_id": "int|null",
  "bus_id": "int|null",
  "busname": "string (bus.number | 'без автобуса')",
  "capacity": "int",
  "link": "route passlists",
  "trip_id": "int",
  "date": "YYYY-MM-DD",
  "tickets": "TicketResource[]",
  "driver_id": "int|null",
  "driver_name": "string|null",
  "is_planned": "bool (тільки для порожніх DTD-слотів)"
}
```

**Stale DTD**: якщо `firstTicket->driverTripDate->bus_id` не збігається з ключем групування — DTD ігнорується (дані протухли після зміни автобуса на квитку).

### 3. Призначення водія/автобуса — `assignBusDriver`

Два шляхи:
- **Є `dtd_id`** → оновити існуючий DTD, якщо змінився `bus_id` — синхронізувати всі `tickets.bus_id` прив'язані до цього DTD.
- **Нема `dtd_id`** → через `DriverTripDateService::upsertSlot($tripId, $date, $busId, $driverId)` створити/знайти, потім прикріпити «безхозні» квитки:
  - якщо передано `current_bus_id` — квитки цього автобуса без `driver_trip_date_id`
  - інакше — квитки зовсім без автобуса і без DTD

## TICKET_EAGER — канонічний eager-load

```php
private const TICKET_EAGER = [
    'client',
    'contactPerson',
    'flight',
    'bus',
    'from.texts',
    'to.texts',
    'trip.texts',
    'driverTripDate.bus',
    'driverTripDate.driver',
];
```

> [!important]
> Це **обов'язковий** список для всіх місць, де тягнуться квитки під `TicketResource`. Пропуск `client`, `contactPerson`, `flight` або будь-якого `.texts` → N+1 помноження на кількість квитків.
>
> Джерело правди: `app/Http/Resources/System/TicketResource.php`. Якщо resource оновлюється (нові поля) — оновити цю константу.

## Типи колонок `date`

| Таблиця | Тип | Фільтр |
|---|---|---|
| `tickets.date` | `DATETIME` | **Потрібно** `whereDate('date', $date)` — `where('date', $date)` не матчить час-частину |
| `driver_trip_dates.date` | `DATE` | `where('date', $date)` OK |

## Ключові файли

- `app/Http/Controllers/Api/Crud/TripsDispatcherCrudController.php`
- `app/Http/Resources/System/TicketResource.php`
- `app/Entities/System/Directories/Ticket.php`
- `app/Entities/System/Directories/DriverTripDate.php`
- `app/Entities/System/Directories/Trip.php`
- `app/Services/DriverTripDateService.php` — `upsertSlot()`
- `app/Helpers/ModelHasTexts.php` — `texts()` relation trait
- `resources/js/crud/base/operations/list/TripDispatcherList.vue`
- `resources/js/crud/base/buttons/ButtonManager.vue`

## Пов'язані документи

- [[driver-trip-date-system]] — повна архітектура DTD + soft-deletes