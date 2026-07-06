---
title: "Проєкт: 3g — Один єчек і сума водію для трансферних пасажирів (is_transfer_route)"
date: 2026-07-06
tags: [3g, work, session, echeck, transfer, fiscalization, driver-cabinet]
category: session
project: 3g
status: in-progress
aliases: ["Трансферна фіскалізація", "is_transfer_route", "Подвійний єчек трансфер"]
pinecone_indexed: false
---

# Один єчек і сума водію для трансферних пасажирів

## Мета сесії
Трансферний (довозний) пасажир має **два квитки у двох Order-ах** (parent на трансферному рейсі + child на основному). При закритті станцій єчек надсилався **двічі** (на кожному рейсі), і водій довозного рейсу помилково бачив суму до збору. Треба: фіскалізувати **рівно один раз** і не показувати суму водію на довозному плечі — але **лише коли пасажир реально пересідає**; якщо їде трансферним рейсом без пересадки — чек і сума мають бути.

## Root cause
Трансферна поїздка = 2 квитки у 2 різних `Order`. Idempotency єчека — **per-Order** (`orders.echeck_id`), тому кожен Order фіскалізується незалежно при закритті «своєї» станції → 2 чеки. Дзеркально — `WidgetsController::cashTicketsQuery()` мав вимкнений guard по парі, тож довозний parent показував суму водію.

## Ключове рішення (архітектура)
Єдиний детермінований критерій **«довозне плече»** = рейс трансферний (`is_transfer_route = true`) **І** квиток має `childTicket` (пасажир пересідає). Інкапсульовано у `Ticket::scopeTransferFeederLeg()` (SQL) + `isTransferFeederLeg()` (in-memory), перевикористано і в echeck-, і в cash-логіці. Квиток **без** `childTicket` (без пересадки) — фіскалізується й сума показується нормально.

## Виконано (по блоках)
- **Блок A — поле `is_transfer_route` + синхронізація**
  - Міграції: `2026_07_06_000001_add_is_transfer_route_to_routes_table`, `2026_07_06_000002_add_is_transfer_route_to_trips_table` (+ backfill майбутніх рейсів `WHERE trips.date >= CURDATE()`).
  - `Route.php`, `Trip.php` — fillable + cast `bool`; синхронізація в `Route::createTrip()`.
  - CRUD-галочка на **маршруті** (`RoutesCrudController`) і **рейсі** (`TripsCrudController`, редагована, tab Settings).
  - `lang/uk/crud.php` = «Трансферний (довозний) маршрут», `lang/en` = «Transfer route».
- **Блок B — єчек (1 чек на пару)**
  - `Ticket.php` — `scopeTransferFeederLeg()` + виключення довозного плеча симетрично у `scopePendingEcheck()` і `scopeIncludedInEcheck()` (`whereNot(transferFeederLeg())`).
  - `arrived()`, `System/TicketsController`, `SendEcheckSmsJob` підхоплюють scope автоматично; force-диспатчі ручної відправки не чіпали.
- **Блок C — сума водію**
  - `WidgetsController::cashTicketsQuery()` виключає довозне плече + eager-load без N+1.
  - `TripManagementTicket` resource — `price=0`/`seat_payment=false`/`hide_price` для довозного плеча.
  - `TripStation.php` — eager-load для fallback-шляху; `Tickets.vue` — `!ticket.hide_price` ховає рядок.
- **Code review** (reviewer): підтвердив, що дедуп при закритті станцій **надійний** (симетрія scope, немає колізії назв, N+1 safe). Знайдено 3🔴 + 2🟡 + 3🟢 суміжних.
- **Verify + галочка на рейсі:** підтверджено ланцюг echeck при `trip.is_transfer_route=true`; додано редаговану галочку на рейс; знайдено наявний ре-синк `Trip::syncWithRoute()`.
- **Діагностика «sync не переносить галочку»:** корінь — на маршрутах **0 записів** `is_transfer_route=true` (галочка не збережена бо **SPA не пересобрано**), `syncWithRoute` справний; додано явний перенос як страховку.

## Важливі рішення (ADR-lite)
| # | Рішення | Чому |
|---|---------|------|
| 1 | Назва колонки `is_transfer_route`, НЕ `is_transfer` | `Trip::is_transfer` — рантайм-alias, керує `BookingService::book():138`; реальна колонка з цією назвою зламала б бронювання трансферів |
| 2 | Критерій = `is_transfer_route && childTicket` (не лише мітка рейсу) | Пасажир без пересадки на трансферному рейсі має отримувати чек і суму |
| 3 | `childTicket` скрізь через `withoutGlobalScope(TicketScope::class)` | Global `TicketScope` ламає lazy-load пари |
| 4 | Знахідка 2: офіс (`trips-management`) бачить суму, ховати лише водію | Персонал потребує суму для звірки |
| 5 | Знахідка 4 (скасований child → feeder): **залишити як є** | Свідоме продуктове рішення |
| 6 | Знахідка 5: ре-синк через наявний `/sync-trips-by-route`, `RouteObserver` можливо не потрібен | Механізм `syncWithRoute` вже є |

## Проблеми й як вирішили
- **Колізія назви `is_transfer`** → окрема колонка `is_transfer_route`.
- **TicketScope ховає пару** → `withoutGlobalScope` в усіх зверненнях до `childTicket`/`parentTicket`.
- **`ReportsController::$onlyEcheck` (рядок ~196)** будує власну вибірку в обхід scope → у змішаному ордері довозне плече потрапляє в аудит-експорт (`EcheckTicketsExport`) з реальною сумою. 🔴 **Не виправлено** (на паузі).
- **«sync не переносить галочку»** → насправді галочка не збережена на маршруті, бо **не зроблено `npm run build`**; backend-персистенс справний (доведено rollback-тестом).

## Стан / незавершене
- ❗ **Не закомічено, міграції в чистому середовищі не запускались** (у поточній dev-БД колонки вже є).
- ❗ Потрібно: `npm run build` → поставити галочку на маршруті → зберегти → `/sync-trips-by-route`.
- ⏸ **Review-виправлення на паузі:** 1 (frontend вкладка «Рейс»: `TripTickets.vue`, `StationTicketsModal.vue`), 2 (resource context-branch офіс vs водій), 3 (`ReportsController $onlyEcheck`).
- Тести (PHPUnit) не писались/не запускались — немає `.env.testing` (RefreshDatabase знищила б основну БД).

## Артефакти
**Команди:** `php artisan migrate` · `npm run build` · `/sync-trips-by-route`
**Змінені файли:** `database/migrations/2026_07_06_000001*`, `2026_07_06_000002*`, `app/Entities/Tenant/Route.php`, `Trip.php`, `Ticket.php`, `TripStation.php`, `app/Http/Controllers/Api/WidgetsController.php`, `app/Http/Controllers/Api/Crud/RoutesCrudController.php`, `TripsCrudController.php`, `app/Http/Resources/System/Trip/Management/TripManagementTicket.php`, `resources/js/crud/base/operations/trip-management/tickets/Tickets.vue`, `lang/uk/crud.php`, `lang/en/crud.php`
**Гілка:** `driver`

## Пов'язані нотатки
- [[project_echeck_module]]
- [[project_echeck_fiscal]]
- [[project_echeck_station_close_bug]]
- [[project_ticket_scope_relationships]]
