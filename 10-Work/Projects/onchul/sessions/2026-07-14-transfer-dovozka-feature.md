---
title: "Проект: onchul (VTS) — transfer-dovozka feature (портування з 3g)"
date: 2026-07-14
tags: [onchul, transfer, booking, backend, frontend]
category: session
project: onchul
status: superseded
superseded_by: "[[2026-07-15-transfer-3g-alignment]]"
aliases: ["onchul-transfer-dovozka"]
pinecone_indexed: false
---

> [!warning] Модель застаріла — див. [[2026-07-15-transfer-3g-alignment]]
> Сесія 2026-07-15 привела довозки до еталона 3g і **скасувала три ADR цієї нотатки**:
> - **ADR #2** (місце довозного = автопідбір) → місце користувача тепер іде на ДОВОЗНИЙ квиток, основний отримує авто-місце; в адмінці оператор явно вибирає ОБИДВА місця.
> - **ADR #3** (кожен квиток = своя посегментна ціна) → основний квиток тримає повний маршрут A→C і ПОВНУ ціну; довозний — сегментний тариф в окремому Order.
> - **ADR #4** (`TicketReturned` на обох плечах) → запис і рефанд ЗАВЖДИ на основному квитку, див. [[2026-07-15-transfer-return-money-on-parent]].
>
> Опис «Основний (A→B)» нижче більше не відповідає коду. Решта (термінологія transfer vs transplantation, модель даних, конфіг станцій) лишається чинною.

# Реалізація функціоналу трансфер-довозка (transfer-dovozka)

## Мета сесії

Портування функціоналу **ТРАНСФЕР = ДОВОЗКА** з еталон-проєкту 3g в onchul (VTS). Довозка — це окремий короткий маршрут (підвіз), який створює ДВА пов'язані квитки:
- **Основний** (A→B) — вибір місця вручну
- **Довозний** (B→C) — автопідбір місця

**Ключова термінологія:** Розмежувати трансфер-довозку (transfer_id → заздалегідь налаштований маршрут + is_transfer_route) від пересадки (transplantation, динамічне стикування з очікуванням). Це ДВА різні концепти.

## Виконано

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Міграції: self-FK tickets.parent_id + is_transfer | ✅ Реалізовано |
| 2 | Backend: зв'язування квитків у Order::createTickets (атомарність) | ✅ Реалізовано |
| 3 | Backend: ціна обох плеч (посегментна, не 0) | ✅ Реалізовано |
| 4 | Backend: Order::calculateAmount доліковує ціну довозки | ✅ Реалізовано |
| 5 | Backend: каскадне повернення + gateway-рефанд батьківський | ✅ Реалізовано |
| 6 | Backend: is_transfer_route прапорець на routes/trips | ✅ Реалізовано |
| 7 | Backend: синк маршрут→рейс + lang UI | ✅ Реалізовано |
| 8 | Backend: право Spatie tickets-transfer-create | ✅ Реалізовано |
| 9 | Backend: видалення «очікування» (assertTransferWindow 5 год) | ✅ Реалізовано |
| 10 | Backend: місце на довозному = автопідбір (безумовний) | ✅ Реалізовано |
| 11 | Backend: 3 роути для модалки пересадки (не заходили) | ✅ Додано |
| 12 | Backend: хелпери фіскалізації пари (Ticket.php) | ✅ Портовано (не в echeck-flow) |
| 13 | Frontend: розділення UI трансфер vs пересадка | ✅ Реалізовано |
| 14 | Frontend: RouteStation.vue, RouteStationsField.vue (два контролі) | ✅ Реалізовано |
| 15 | Frontend: TripDetails.vue, Trip.vue (окремі лейбли) | ✅ Реалізовано |
| 16 | Frontend: AddTransferStationPopup.vue (фіксы рендеру) | ✅ Реалізовано |
| 17 | Frontend: TripsTableManager.vue (назва станції + вільні місця) | ✅ Реалізовано |
| 18 | Frontend: BookingForm.vue (фіксы Vue warning) | ✅ Реалізовано |
| 19 | Тести: 35 pass у tests/Feature/Booking/ | ✅ Реалізовано |
| 20 | Команда: tickets:backfill-transfer-prices [--dry-run] | ✅ Реалізовано |

## Важливі рішення (ADR)

| # | Питання | Рішення | Чому |
|---|---------|---------|------|
| 1 | Пересадка vs трансфер-довозка | Переносимо ТІЛЬКИ довозку, пересадку НЕ | Вимога користувача; довозка = налаштована, пересадка = динамічна (складніша) |
| 2 | Вибір місця на рейсі | Основний = вручну, довозний = автопідбір | Логіка UX: юзер вибирає маршрут, довозна — авто |
| 3 | Ціна за пару квитків | Кожен = своя посегментна ціна | Як 3g, прозорість дляユзера; квиток-об'єкт = окремий рядок рахунку |
| 4 | Повернення квитків | TicketReturned на ОБОХ плечах, gateway-рефанд тільки на батьківському (parent_id===null) | Зберігає консистенцію платежу (одна плата за пару) |
| 5 | free_seats_count у списку | Кількість місць КАРТИ довозного (free_places->count()) | Точніше; раніше помилково = основний автобус |

## Проблеми й як вирішили

- **Проблема 1: Дочірній квиток брав місце основного замість автопідбору**
  - **Root cause:** BookingService не перевіряв is_transfer при getFreeSeatsByFromTo
  - **Фікс:** Автопідбір зроблено безумовним для is_transfer=true

- **Проблема 2: UI плутав трансфер і пересадку**
  - **Root cause:** Спільні компоненти і лейбли, тип визначається по is_transfer або transplantation бульйок
  - **Фікс:** Повне розділення контролів (RouteStation vs RouteStationsField), окремі лейбли у TripDetails/Trip, PDF

- **Проблема 3: Розбіжність вільних місць список(46) vs карта(26) для trip 69**
  - **Root cause 1:** Масиви ламали умову трансфера (не porівнювались station_id)
  - **Root cause 2:** free_seats_count брався з основного замість карти довозного
  - **Фікс:** array-safe через toStation->station_id; free_seats_count = free_places->count() (довозний автобус)

- **Проблема 4: Ціна плеча довозки = 0**
  - **Root cause:** Legacy-записи з вікна багу (12:08-16:59, коміт 73a39a4). Поточний код правильний.
  - **Фікс:** Команда `php artisan tickets:backfill-transfer-prices --dry-run` на локалі: виправлено 3500 квитків (#874/#1272/#1274)

- **Проблема 5: Модалку конфігу пересадки не можна було відкрити**
  - **Root cause:** 3 роути для пошуку станцій не зареєстровані: `/system/routes/list`, `/routes/stations-by-route/search`, `/routes/stations-by-trip/search`
  - **Фікс:** Додано роути (контролер-методи вже були, тільки роутів бракувало)

- **Проблема 6: Назва станції відправлення й вільні місця не показувались у TripsTableManager**
  - **Root cause:** Давній недогляд frontend: стовпці не було у template + не було data-binding
  - **Фікс:** Додано назву станції (from_station.name) + стовпець free_seats_count

## Артефакти

**Міграції:**
- `tickets`: self-FK `parent_id` + bool `is_transfer`
- `routes`: bool `is_transfer_route`
- `trips`: bool `is_transfer_route` (синк з маршруту)

**Backend файли:**
- `app/Models/Order.php` — createTickets (атомарність, зв'язування)
- `app/Models/Ticket.php` — is_transfer, parent_id, хелпери фіскалізації пари (transferPairLegs, isTransferFeederLeg, scopeTransferFeederLeg, getFiscalPriceAttribute)
- `app/Models/Route.php` — is_transfer_route, синк
- `app/Models/Trip.php` — is_transfer_route
- `app/Services/BookingService.php` — bookTransfer (вилучено assertTransferWindow), автопідбір місця
- `app/Services/TripsService.php` — getFreeSeatsByFromTo (array-safe), free_seats_count (карта)
- `app/Observers/TicketObserver.php` — каскадне повернення
- `app/Console/Commands/BackfillTransferPrices.php` — нова команда (dry-run mode)
- `routes/api.php` — додано 3 роути для пошуку станцій
- `lang/uk/crud.php` — is_transfer_route label
- `config/types.php` — (перевірити, чи є ticket_type для transfer)

**Frontend файли:**
- `resources/js/crud/RouteStation.vue` — контрол трансфера
- `resources/js/crud/RouteStationsField.vue` — контрол пересадки
- `resources/js/crud/TripDetails.vue` — лейбли без OR
- `resources/js/crud/Trip.vue` — лейбли без OR
- `resources/js/crud/BookingForm.vue` — фіксы warning
- `resources/js/crud/AddTransferStationPopup.vue` — рендер (не рендерилась у template)
- `resources/js/crud/TripsTableManager.vue` — назва станції, вільні місця, видалено дату поїздки, видалено banner, видалено чекбокс
- `resources/js/utils/pdf.js` або PDF-клієнт — type transfer|transplantation
- `lang/uk/` — розділення типів

**Команди:**
```bash
# Запустити dry-run (показати, що виправиться)
php artisan tickets:backfill-transfer-prices --dry-run

# На проді (після деплою): без прапорця
php artisan tickets:backfill-transfer-prices
```

## Незавершені хвости (follow-up)

1. **CRUD-чекбокс is_transfer_route в адмінці** — поле на бекенді є, фронтенд-контрола немає (окрема мала задача)
2. **Фіскалізація пари в echeck** — хелпери портовано, не заведено в Order-flow (echeck інертна, окреме рішення)
3. **Запустити backfill на проді** — ПІСЛЯ деплою фіксу ціни
4. **qa (E2E наживо)** — не робилось
5. **docs** — не оновлено
6. **Коміт** — не робився (git rules проєкту)
7. **Мертвий код:** `Api.booking.getTripPrice` (api-bridge.js), мертві механізми (bus/active-days) у route_stations
8. **VIEW `ticket_stat_view` definer=tmp_onchul** — локальна БД, окрема інфраструктурна проблема

## Пов'язані нотатки

- [[2026-07-13-portmone-gateway-migration]] — платіжний шлюз Portmone (коминали платіж)
- [[2026-07-14-echeck-fiscalization]] — E-check фіскалізація (інертна, не в потоці)
- [[2026-07-03-trip-report-merge-trips]] — об'єднання рейсів у відомості (на паузі, баг валюти)
- [[2026-07-03-import-tickets-from-vonchul]] — імпорт квитків з vonchul (готово, чекає --import)
- [[10-Work/Projects/onchul/docs/INDEX]] — загальна архітектура
