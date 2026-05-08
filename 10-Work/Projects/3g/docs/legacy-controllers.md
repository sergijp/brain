---
title: "Legacy Controllers — план розбиття god-classes"
date: 2026-05-08
tags: [3g, architecture, refactoring, tech-debt]
category: docs
project: 3g
status: active
aliases: ["3g-legacy", "3g-refactoring"]
pinecone_indexed: false
---

# Legacy Controllers — техдовг

Топ-5 найбільших файлів і план їх розбиття. Стек: Laravel 10, PHP 8.1+, Vue 3, Vue 2.x → 3 (потрібен апгрейд L10→L11 паралельно з виносом у пакети).

## Топ-5 файлів

| Файл | Рядків | Стан |
|---|---|---|
| `TripsCrudController.php` | **1709** | god-controller |
| `WidgetsController.php` | **1154** | віджети/звіти |
| `Trip.php` (model) | 1085 | god-model |
| `RoutesCrudController.php` | 713 | роздутий CRUD |
| `Ticket.php` (model) | 673 | дисконт-логіка inline |

## P1 — критично

### `TripsCrudController.php` (1709)

- `dd($e->getMessage())` у catch у **production** (район L1540): `cancelTrip`, `tripUpdate`, `closeTrip`, `uncloseTrip`. → `Log::error` + graceful response.
- **Дубль SMS-логіки**: `sendAllSms()` L261-319 vs `sendSmsMessage()` L321-376 — ~55 рядків майже ідентичних. → один `SendTripSmsAction`. **(вже частково через `TicketNotificationService`, див. [[notifications]])**
- `reportDriver()` L1059-1210 (152 рядки) + dead duplicate discount-блок L1103-1115 vs активний L1116-1138. → `DriverDiscountReportService`.
- **`env()` поза config — 20+ вхождень**: L268, L329, L316-317, L1358, L1361, L1427-1428 (AlphaSms, PortMone keys). → `config/services.php`.
- Закоментований блок L590-616 (старе `bus_id`/`carrier_id`). → видалити.

### `WidgetsController.php` (1154)

god-controller віджетів/звітів. → розбити за типом віджета у `Services/Widgets/*` або `Actions/Reports/*`.

### Інше P1

- `app/Http/Controllers/LiqPay.php` — платіжний клас у Controllers. → `app/Services/Payment/LiqPayService.php`.
- `docker/**/Dockerfile` — PHP 7.2 vs composer `^8.1`. → `php:8.2-apache` + апгрейд PHP.
- `Crud/Operations/CopyOperation.php` — 2× `dd()` (типовий патерн Visson-core, повторюється з air-trans/grosser/buktreck). → `Log::error`.

## P2 — важливо

- **`Trip.php`** (1085) — god-model. Константи `STATUS_*`, `TYPE_DIRECTION_*` → `TripService`, `TripQuery`, `enum TripStatus`, `enum TripDirection`.
- **`Ticket.php`** (673) — логіка розподілу дисконтів → `DistributeDiscountAction`.
- **`Route.php`** (546) — `TYPE_EVERY_DAY`, `TYPE_EVEN`, `TYPE_ODD` → `enum RouteScheduleType`.
- **`WalletBalance`** — 8+ констант → Enums.
- **Vuex → Pinia + TypeScript** (0 `.ts` файлів зараз).
- **0 реальних тестів** — 2 `ExampleTest` заглушки, 125 міграцій без покриття. → integration-тести для `TripsCrudController`, `LiqPay`, `AlphaSms`.

## Performance — виконано (2026-04-28)

### `shortTripManagementWidget` (WidgetsController ~886)

- `loadMissing([from.city.country, to.city.country, parentTicket.from/to, trip, order.tickets, order.member])` на `$trip->tickets` — замість ~1500 lazy-load запитів.
- TicketStats prelоaded batch-запитом, груповано по `station_id` — замість N `whereHas` підзапитів.
- `Discount::query()` винесено за межі циклу станцій.
- `$trip->stations` (in-memory) замість `$trip->stations()->get()`.
- `_ticketsFrom`, `_ticketsToCount`, `_ticketsTravelingCount` встановлюються у контролері.
- `TripManagementStation` ресурс використовує pre-loaded дані (з fallback на DB).
- `TripManagementTicket` ресурс: `trip_id` замість `trip->id` (без lazy-load trip).
- `Trip::getDepartureCurrentStationDateTime()` — якщо `stations` loaded, in-memory колекція.
- `cash_amounts` query: `->with('parentTicket')`.

### `TicketsCrudController.php` (setupListOperation)

- Додано `trip.stations` до eager load — прибирає lazy у `getDepartureAttribute()`.
- Додано `returnedTicket` — прибирає ~2000 lazy-load запитів.
- `whereHas('trip', ...)` → `whereIn('trip_id', fn => select id from trips ...)` у 3 місцях.
- `texts` eager load фільтрується по `app()->getLocale()` — −3x обсягу.

## Performance — залишок

### DB індекси (потрібна міграція — найбільший виграш)

- `tickets`: `created_at`, `parent_id`, `status`, composite `(trip_id, status)`
- `trips`: `date`

### `shortTripManagementWidget`

- `$station->station->title` і `$station->bus` — lazy у `TripManagementStation`. Фікс: `->with(['station', 'bus'])` до eager load.
- `empty_places` — TicketStats per station, можна batch.
- `first_station_title`, `last_station_title`, `firstStation()->time` — 3 DB-запити × N станцій → обчислити до циклу.

## Нагадування

> Мульти-тенантності у 3g немає і не планується. Tenant-інфра в коді — dead code, видалити.

## Пов'язані

- [[INDEX]]
- [[notifications]] — `TripsCrudController` `sendAllSms`/`sendSmsMessage` тепер через `TicketNotificationService`
- [[busfor-api]] — окремий аудит зовнішнього провайдера
