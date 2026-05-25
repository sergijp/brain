---
title: "air-trans — client_name на квитку, notes на DriverTripDate"
date: 2026-05-25
tags: [air-trans, work, session, tickets, client, driver-trip-date, backend]
category: session
project: air-trans
status: done
aliases: [air-trans-client-name-trip-notes]
pinecone_indexed: false
---

## Мета сесії

1. Дозволити створення заявки (ticket) тільки з іменем клієнта — без телефону (клієнт без телефону не створюється).
2. Показувати це ім'я скрізь де виводяться дані пасажира.
3. Додати поле `notes` до запланованої поїздки (`DriverTripDate`) з окремим ендпоінтом для оновлення.

---

## Виконано

### 1. Заявка з іменем без телефону

| Задача | Результат |
|--------|-----------|
| Міграція `tickets.client_name` (nullable string) | ✅ Застосовано |
| `Ticket::$fillable` + accessor `getClientNameAttribute` з fallback | ✅ |
| `StoreClientField::process()` — нова логіка: id→клієнт, phone→новий клієнт, тільки ім'я→`client_name` | ✅ |
| `GetClientField::process()` — повертає `client_name` якщо немає клієнта (для форми редагування) | ✅ |
| `getClientContactPersonNameAttribute()` — fallback на `client_name` | ✅ |

### 2. Відображення client_name скрізь

| Файл | Зміна |
|------|-------|
| `TicketsResource.php` | `client.name` fallback на `client_name` (driver panel) |
| `System/TicketResource.php` | `name` через accessor (dispatcher, трансфер автобусів) |
| `TicketsCrudController.php` | пошук по `client_name` у списку |
| `TicketsController.php` | SMS-шаблон з fallback |
| `pdf/ticket/index.blade.php` | `$ticket->client_name` замість `$ticket->client->name` |
| `TripTickets.vue` | null-safe пошук + `tel:` посилання |

### 3. Notes для DriverTripDate

| Файл | Зміна |
|------|-------|
| `DriverTripDateService::upsertSlot()` | параметр `?string $notes = null` |
| `PlaningTripsOperation::planingTripsGenerate()` | валідація + передача notes |
| `PlaningTripsOperation::planingTripsUpdate()` | notes в `$request->only()` |
| `PlaningTripsOperation::planingTripsFormatRecord()` | notes у відповіді |
| `TripsDispatcherCrudController::buildBusGroup()` | notes у відповіді |
| Новий маршрут + метод `planingTripsUpdateNotes` | `PATCH planing-trips/{id}/notes` |

> `{id}` — це `id` запису `DriverTripDate` (конкретний виїзд: маршрут + дата + автобус)

---

## Важливі рішення

- **`Trip` — маршрут, не поїздка**: коментар додавали до `trips`, але відкотили — `Trip` виступає як маршрут-шаблон, коментар потрібен тільки на конкретному виїзді (`DriverTripDate`).
- **Клієнт без телефону не створюється**: ім'я зберігається в `tickets.client_name`, accessor `getClientNameAttribute` повертає `client?->name ?? client_name` — решта коду не змінювалась.
- **notes вже було в DB**: поле `notes` існувало в міграції і `$fillable` `DriverTripDate`, але не було підключено до API жодним методом.

---

## Артефакти

- `database/migrations/2026_05_25_000000_add_client_name_to_tickets_table.php`
- `app/Crud/PreProcessors/Store/StoreClientField.php`
- `app/Crud/PreProcessors/Get/GetClientField.php`
- `app/Crud/Operations/PlaningTripsOperation.php`
- `app/Services/DriverTripDateService.php`

---

## Пов'язані нотатки

- [[air-trans-ticket-validation-fixes]]
- [[air-trans-trips-dispatcher-architecture]]
- [[air-trans-soft-deletes-architecture]]
