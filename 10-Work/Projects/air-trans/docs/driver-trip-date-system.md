---
title: "DriverTripDate — логіка планування рейсів"
date: 2026-04-21
tags: [air-trans, backend, logic, planning, bus, driver]
category: docs
project: air-trans
status: done
---

# DriverTripDate — логіка планування рейсів

## Що таке DTD?

`DriverTripDate` (DTD) — це **«слот автобуса на рейсі у конкретну дату»**.

```
DTD = {
  trip_id   ← рейс (маршрут + розклад)
  date      ← конкретна дата поїздки
  bus_id    ← який автобус їде (nullable)
  driver_id ← хто веде (nullable, змінюється)
  active    ← чи активний слот
}
```

> [!important]
> DTD — це НЕ «водій на рейсі». Водій — атрибут, що може змінюватись або бути відсутнім. Ідентичність DTD — **(trip_id, date, bus_id)**.

---

## Стани квитка

Квиток (`Ticket`) може знаходитись у одному з трьох станів:

| Стан | bus_id | driver_trip_date_id | Опис |
|---|---|---|---|
| **Без автобуса** | null | null | Квиток продано, автобус не призначено |
| **З автобусом, без планування** | B | null | Автобус відомий, але DTD ще не створено |
| **Запланований** | B | DTD | Є слот з водієм (або без, якщо водія видалили) |

---

## Як відбувається планування

### 1. Додавання квитка окремо (TicketsCrudController)

```
Користувач вказує: рейс + дата + автобус
→ afterCreateAction / afterUpdateAction
→ DriverTripDateService::syncTicketLink()
→ Шукає активний DTD за (trip, date, bus)
→ Якщо знайдено → tickets.driver_trip_date_id = dtd.id
→ Якщо ні → tickets.driver_trip_date_id = null
```

### 2. Планування діапазону дат (PlaningTripsOperation)

```
Диспетчер вказує: рейс + діапазон дат + автобус + водій
→ planingTripsGenerate()
→ Для кожного дня: DriverTripDateService::upsertSlot()
  → firstOrNew по (trip_id, date, bus_id) withTrashed
  → Якщо trashed → restore
  → Оновити driver_id (навіть якщо водій інший!)
  → save()
  → attachOrphanTickets() → прив'язати квитки без dtd_id
```

> [!note]
> Якщо вже є DTD для цього (trip, date, bus) але з іншим водієм — водій просто оновлюється, дублікату не виникає.

### 3. Призначення через диспетчер (TripsDispatcherCrudController::assignBusDriver)

Два шляхи:

**З dtd_id** (редагування існуючого):
```
Оновити bus_id, driver_id на існуючому DTD
→ Синхронізувати bus_id на квитках DTD якщо bus змінився
```

**Без dtd_id** (нове призначення):
```
DriverTripDateService::upsertSlot()
→ Прив'язати незалінковані квитки
```

---

## Що відбувається при видаленнях

```
┌──────────────┬─────────────────────────────┬────────────────────────────┐
│ Подія        │ DriverTripDate              │ Ticket                     │
├──────────────┼─────────────────────────────┼────────────────────────────┤
│ delete Bus   │ soft-delete (каскад)        │ bus_id = null, dtd_id=null │
│ restore Bus  │ restore                     │ лишається без bus¹         │
│ delete Driver│ driver_id = null (залиш.)   │ без змін (dtd_id живий)    │
│ delete DTD   │ soft-delete                 │ dtd_id = null              │
│   (планув.)  │                             │ (bus_id лишається)         │
│ delete DTD   │ 422 якщо є квитки           │ —                          │
│   (диспетч.) │                             │                            │
└──────────────┴─────────────────────────────┴────────────────────────────┘
```

¹ Після відновлення автобуса квитки без `bus_id` потрібно перепризначити вручну через диспетчер.

---

## DriverTripDateService

Весь доменний код — в одному місці: `app/Services/DriverTripDateService.php`.

```php
// Upsert слот (основний метод)
upsertSlot(tripId, date, busId, driverId): DriverTripDate

// Видалити слот (+ занулити квитки)
deleteSlot(dtdId): void

// Синхронізувати прив'язку квитка до DTD
syncTicketLink(Ticket): void

// Прив'язати квитки без dtd_id на слот
attachOrphanTickets(DriverTripDate): void

// Каскади
onBusDeleted(busId): void
onBusRestored(busId): void
onDriverDeleted(driverId): void
```

---

## Observer'и

| Observer | Trigger | Дія |
|---|---|---|
| `BusObserver::deleting` | Bus soft-deleted | `onBusDeleted` |
| `BusObserver::restored` | Bus restored | `onBusRestored` |
| `DriverObserver::deleting` | Driver soft-deleted | `onDriverDeleted` |

---

## Унікальний індекс БД

```sql
UNIQUE KEY driver_trip_dates_trip_date_bus_unique (trip_id, date, bus_id)
```

> [!warning]
> MySQL unique index охоплює **всі рядки**, включно з soft-deleted. При міграціях, що додають unique index на таблицю з SoftDeletes, потрібно спочатку **hard-delete** soft-deleted рядки, що конфліктують.

`bus_id` nullable — MySQL трактує NULL≠NULL, тому кілька DTD без автобуса на ту саму (trip, date) не конфліктують.

---

## Пов'язані файли

| Файл | Роль |
|---|---|
| `app/Services/DriverTripDateService.php` | Доменна логіка |
| `app/Entities/System/Directories/DriverTripDate.php` | Модель |
| `app/Crud/Operations/PlaningTripsOperation.php` | Планування діапазону |
| `app/Http/Controllers/Api/Crud/TripsDispatcherCrudController.php` | Диспетчер |
| `app/Http/Controllers/Api/Crud/Directories/TicketsCrudController.php` | CRUD квитків |
| `app/Observers/BusObserver.php` | Каскад Bus → DTD → Ticket |
| `app/Observers/DriverObserver.php` | Каскад Driver → DTD |

## Пов'язані документи

- [[INDEX]]
- [[trips-dispatcher-controller]] — диспетчерський екран, споживач DTD (TICKET_EAGER, `is_planned`)
