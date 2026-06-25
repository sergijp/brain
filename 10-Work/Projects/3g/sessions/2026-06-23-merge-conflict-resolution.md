---
title: "Проект: 3g — Вирішення merge-конфліктів (dev ← driver)"
date: 2026-06-23
tags: [3g, work, session, merge, conflicts]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Вирішення merge-конфліктів після злиття гілки `driver` у `dev`. Конфлікти виникли між двома паралельними feature-гілками: station access control (dev) та surveys/driver features (driver).

## Виконано

| Файл | Статус | Що зроблено |
|------|--------|-------------|
| `lang/en/crud.php` | ✅ | Об'єднано `bus_services` (dev) + `survey_*` ключі (driver) + відновлено `route_access_restricted` блок (8 ключів station access, що випали при мержі) |
| `lang/uk/crud.php` | ✅ | Об'єднано `bus_services` (dev) + `question`/`survey_results`/`selected_places` (driver), прибрано дублікат `confirm_arrival_with_unchecked_tickets` |
| `app/Entities/System/Member.php` | ✅ | Конфлікт 1 → HEAD (`$fillable` з `route_access_restricted`+`station_access_restricted`), конфлікти 2–3 → driver (мемоізація `static $cache` в `getTotalPercents()`) |
| `app/Services/Api/v1/External/Resources/TripInfoResource.php` | ✅ | Всі 6 конфліктів → HEAD (driver мав лише FQCN замість аліасів і менше вирівнювання) |
| `app/Services/Api/v1/External/Resources/TripListResource.php` | ✅ | Всі 10 конфліктів → HEAD (тільки форматування) |
| `app/Services/Api/v1/External/Resources/RouteResource.php` | ✅ | Чистий після мержу |
| `app/Services/TripsService.php` | ✅ | 4 конфлікти → HEAD (transfer search, agent check, tickets filter) |
| `app/Entities/Tenant/Trip.php` | ✅ | Конфлікти 1,2,4 → HEAD; конфлікт 3 → driver (критичний логічний баг виправлено вручну після помилкового вибору) |
| `app/Entities/Tenant/TripStation.php` | 🔄 | Проаналізовано, рекомендовано driver (новий метод `getTicketsTravelingChecked`) |

## Важливі рішення (ADR)

### Конфлікт 3 у `scopeStationsQuery` (Trip.php) — логічний баг
**Проблема:** HEAD версія `->when(! is_null($date), ...)` разом із `->when(! is_null($date) && ! is_null($dateTo), ...)` викликала подвійний WHERE при пошуку за діапазоном дат — жодного рейсу не повертала.

**Рішення:** взято driver: `->when(! is_null($date) && is_null($dateTo), ...)` — умови тепер взаємовиключні. Виправлено вручну після того як користувач помилково взяв HEAD.

### lang/en/crud.php — втрата station access ключів при мержі
Git взяв `'routes' => 'Маршрути'` (driver) замість `'routes' => 'Routes'` (HEAD) і дропнув 8 ключів station access, що йшли після нього у HEAD. Відновлено вручну з git index (`:2:` версія).

### Member.php — мемоізація getTotalPercents()
Driver гілка додала `static $cache[]` для кешування результату per-member. Взято driver для конфліктів 2-3 (return з кешем), HEAD для конфлікту 1 (fillable з новими полями).

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Зміни в `lang/en/crud.php` зникали після збереження (IDE перезаписував) | Відновили через `git show :2:` і дописали вручну у два прийоми |
| Конфлікт 3 у Trip.php вирішено неправильно (HEAD замість driver) | Виявлено при перевірці, виправлено Edit-ом одного рядка |
| lang/uk/crud.php мав дублікат ключа у driver-версії | Прибрано при злитті |

## Артефакти

- Перевірено PHP синтаксис всіх файлів: `php -l`
- Перевірено відсутність маркерів: `grep -c "<<<<<<"`
- Перевірено повний ланцюг `TripsService → TripListResource → Controller` — функціонал не зламався
- Перевірено всі виклики методів Member.php (`isRouteRestricted`, `allowedRoutes`, `hiddenStationsByRoute`, `isStationRestricted`, `getTotalPercents`) — всі визначені і коректно викликаються

## Пов'язані нотатки

- [[station-access-control]] — feature station access (route_access_restricted, StationAccessScope)
- [[project_surveys_custom_routes]] — surveys module (survey_title, question, survey_results ключі)
- [[project_bus_services]] — bus_services JSON поле і переклади
