---
title: "Проект: 3g — Виправлення багів Station Access Control"
date: 2026-05-14
tags: [3g, work, session, bugfix, station-access, php, vue, mysql]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

# Виправлення багів Station Access Control

## Мета сесії

Продовження роботи над Station Access Control (per-Route × Station blacklist). Усунути баги що виявились після першої імплементації:
1. `hiddenMap` дані не повертались у Vue компонент при відкритті user
2. SQL crash у `StationAccessScope` через MySQL обмеження
3. Null crash у `TripsService` при пошуку по заблокованій станції
4. Аудит інших API на предмет схожих null crashes

## Виконано

### Bug 1 — hiddenMap повертався як JSON array `[]` замість object `{"1":[2]}`

**Симптом:** збережені в БД станції не показувались у Vue компоненті після перевідкриття user.

**Root cause:** PHP gotcha — `$hiddenMap[(string) $row->route_id][] = $stationId` автоматично конвертує numeric-string ключ "1" в integer 1. Масив `[1 => [2]]` через `json_encode` стає `[[2]]` (sequential JSON array з нульовим індексом), а не `{"1":[2]}` (object). Vue потім читав ключ "0" замість "1".

**Fix:** `app/Crud/PreProcessors/Get/GetUserRouteField.php` — кастуємо до `(object)` перед поверненням:
```php
$hiddenMap = (object) $hiddenMapRaw;
```

### Bug 2 — SQL: Unknown column 'trip_station.trip_id' in 'on clause'

**Симптом:** crash при будь-якому запиті до Trip-related даних під restricted user.

**Root cause:** MySQL не дозволяє посилатись на зовнішню таблицю всередині `JOIN ON` clause у підзапиту. `StationAccessScope` мав:
```sql
NOT EXISTS (
  SELECT 1 FROM member_route_station AS mrs
  JOIN trips ON trips.id = trip_station.trip_id   -- ❌ outer table в ON
  WHERE mrs.station_id = trip_station.station_id
  AND mrs.route_id = trips.route_id
)
```

**Fix:** `app/Scopes/StationAccessScope.php` — переписали так, що `JOIN ON` посилається лише на внутрішні таблиці, а outer table refs пішли в `WHERE`:
```sql
NOT EXISTS (
  SELECT 1 FROM member_route_station AS mrs
  JOIN trips ON trips.route_id = mrs.route_id     -- ✅ обидві з підзапиту
  WHERE mrs.station_id = trip_station.station_id
  AND trips.id = trip_station.trip_id             -- ✅ outer ref у WHERE
)
```

### Bug 3 — Null crash у TripsService.getOriginalOptionsTrip line 304

**Симптом:** `Attempt to read property "station_id" on null` коли restricted user шукає по заблокованій станції.

**Root cause:** `$trip->stationById()` шукає по `$this->stations` колекції, яка вже відфільтрована scope. Для прихованої станції — повертає null.

**Fix:** `app/Entities/Tenant/Trip.php::stationById()` — додано fallback. Спочатку шукає у scoped колекції (без зайвого запиту для normal case), якщо null — робить окремий запит з `withoutGlobalScope` (внутрішня business логіка потребує справжньої топології рейсу).

### Bug 4 — Аудит та фікси null crashes у інших API

Crash на null property access **не** оброблюється custom JSON handler (lardiyel `parent::render()`). У результаті — HTTP 500 замість обробленої помилки. Це критично якщо у користувача кешовані дані з тепер-прихованою станцією і він намагається забронювати.

**Виправлені місця:**
- `BookingController::bookTickets()` лінії 242-249 — null guard + `withoutGlobalScope` fallback
- `BookingController::getTripPrice()` лінії 619-622 — null guard з JSON error response
- `TripController::getTripPrice()` лінії 528-535 — null guard для основного trip
- `TripController::getTripPrice()` transfer лінії 575-578 — null guard для transfer trip
- `WidgetsController` лінії 1047-1049 — `withoutGlobalScope` + `value()` замість `->first()->order`

`BookingService::validateOrderData()` вже мав `assertCanAccess()` guard (лінії 81-88) — отже crafted request з забороненою станцією поверне коректний 403.

## Важливі рішення (ADR)

| Рішення | Обґрунтування |
|---------|---------------|
| `(object)` cast у `GetUserRouteField` | Єдиний надійний спосіб гарантувати JSON object у PHP коли ключі numeric strings |
| `stationById()` робить fallback до unscoped query | Це internal business method — для розрахунку ціни/місць потрібна реальна топологія. Authorization — окремий gate у `BookingService` |
| `BookingController.bookTickets` теж використовує `withoutGlobalScope` fallback | Те саме обґрунтування — внутрішня логіка `getTripPlaces`, security gate далі через `assertCanAccess` |
| `WidgetsController` ticket search — `withoutGlobalScope` без fallback | Це search існуючих квитків — агент має бачити свої квитки незалежно від поточних обмежень станцій |
| `TripController::getTripPrice` — null guard без unscoped fallback | Це user-facing price endpoint. Якщо станція прихована — користувач не має отримувати ціну. Повертаємо `E_NODATA` |
| `DB::table('member_route_station')` замість `hiddenStationsByRoute()` BelongsToMany | Не потрібен Station model з relations; майбутній `StationAccessScope` на Station міг би рекурсивно заблокувати сам запит |

## Проблеми й як вирішили

| Проблема | Як знайшли | Рішення |
|----------|-----------|---------|
| Vue не показує збережені дані | console.log у `setValue()` → `[[2]]` замість `{"1":[2]}` | Cast `(object)` у PHP |
| `member_id=2` records vs editing `member_id=1` | `\Log::debug` у Get/Store preprocessors | Зрозуміли що це різні користувачі (попередні тести з member 2) |
| SQL outer table ref в JOIN ON | MySQL exception "Unknown column ... in 'on clause'" | Переструктурували subquery |
| Crashes при пошуку | Stack trace вказав на TripsService:304 | Fallback у `stationById()` |

## Артефакти

**Файли змінено:**
- `app/Crud/PreProcessors/Get/GetUserRouteField.php` — `(object)` cast
- `app/Crud/PreProcessors/Store/StoreUserRouteField.php` — прибрано debug log
- `app/Scopes/StationAccessScope.php` — переписали subquery
- `app/Entities/Tenant/Trip.php::stationById()` — fallback без scope
- `app/Http/Controllers/Api/TripController.php` — 2× null guards (main + transfer)
- `app/Http/Controllers/Api/System/BookingController.php` — 2× null guards
- `app/Http/Controllers/Api/WidgetsController.php` — `withoutGlobalScope` + `value()`
- `resources/js/crud/base/fields/UserRoutesField.vue` — `this.fieldValue.hiddenMap` замість Proxy

**НЕ змінювалось (вже безпечно):**
- `firstStation()`, `lastStation()` — вже мають `withoutGlobalScope`
- `CreateTicketJob` — вже має `withoutGlobalScope`
- Admin CRUD контролери — `hasFullAccess()` = true → scope no-op
- Jobs/Cron — без user context → scope no-op

## Пов'язані нотатки

- [[2026-05-14-route-access-control]] — попередня сесія з Route Access (база для Station Access)
- Plan file: `~/.claude/plans/mighty-dreaming-mochi.md` — повний план Station Access реалізації