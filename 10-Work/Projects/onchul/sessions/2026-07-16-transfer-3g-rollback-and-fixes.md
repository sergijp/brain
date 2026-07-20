---
title: "Проект: onchul (VTS) — відкат другої схеми довозки до моделі 3g + пакет фіксів"
date: 2026-07-16
tags: [onchul, transfer, booking, backend, frontend]
category: session
project: onchul
status: completed
aliases: ["onchul-transfer-3g-rollback"]
pinecone_indexed: false
---

# Відкат помилкової другої схеми довозки → модель 3g + пакет фіксів

**Гілка:** `transfer` · **Стан:** НЕ закомічено (~20+ файлів + нові поля)

## Мета сесії

Виправити помилку попередньої сесії [[2026-07-15-transfer-3g-alignment]]: у ній довозки нібито привели до еталона 3g (`/Users/serhiin/Data/Source/3g`), але фактично збудували **другу схему автобуса** + явний двомісний контракт, чого в 3g немає. Ця сесія **відкочує** ту помилку до справжньої моделі 3g (одна фідерна схема) і додає низку суміжних виправлень.

> Довозка (transfer) = пара квитків через `tickets.parent_id`. **НЕ плутати** з пересадкою (transplantation) — її в onchul немає.

## Головна помилка, яку виправили

У сесії 15.07 підміну автобуса в адмінському `getTrip` хибно кваліфікували як «хак, якого немає в 3g», і прибрали її. Насправді це **і Є механізм 3g**: і адмінка, і публічний сайт ходять через `TripsService::getAdditionalOptionsTrip()`, який ПІДМІНЯЄ основному рейсу `bus`/`tickets`/`stations`/`free_places`/`closed_places` на фідерні — оператор бачить **одну схему (фідера)**. Прибравши підміну, зламали адмінку і зверху добудували другу схему + двомісний контракт (`transferId` + `tickets[].transfer`). Рішення користувача — відкотити все це до моделі 3g.

## Виконано

| # | Блок | Результат |
|---|------|-----------|
| 1 | **Відкат до однієї схеми 3g:** видалено `getSystemOptionsTrip()`+`buildTransferLegTrip()`, `bookExplicitTransferPair()`+`bookExplicitTransferLegs()`, параметр `$transferTrip` з `book()`. Адмінський `getTrip` (осн. + back_trip) знову через `getAdditionalOptionsTrip()`. Прибрано контракт `transferId`+`tickets[].transfer`. Фронт: видалено `ChooseTransferPlaces.vue`, почищено 4 компоненти до однієї схеми. Автопідбір основного плеча = останнє вільне (`sortByDesc('number')`), обране місце → дочірній | ✅ |
| 2 | **Знято право Spatie `tickets-transfer-create`** — прибрано `assertCanCreateTransfer()` (був у `bookTransfer()`, яким ходить і публічний сайт → 403 з адмінським текстом клієнту), ключі в `lang/uk\|en/permissions.php`, Vue-гейти. В 3g перевірки немає | ✅ |
| 3 | **Місце в PDF/email (`virtual_place`):** новий аксесор `Ticket::getVirtualPlaceAttribute()` віддає місце ДИТИНИ (обране вручну), якщо `childTicket->isTransferFeederLeg()`. Застосовано в `pdfFile()` + 3 мейли пасажиру. Eager-load childTicket проти N+1 | ✅ |
| 4 | **Відомість рейсу:** на рядку довозної дитини — маршрут+ціна БАТЬКА (повна), але МІСЦЕ дитини. Розведено `fiscal_price` (для показу, повна) і нове `sum_price` (=0 для feeder) — щоб об'єднана відомість не задвоювала виручку (4500, не 9000) | ✅ |
| 5 | **Пошук — перетин вільних місць обох плечей** (порт `original_free_places` з 3g): `getOriginalOptionsTrip` зберігає снапшот основного плеча, фільтр робить перетин обох; `free_seats_count` = min(обидва). Passcount-перевірка на обидва плеча (`SearchController` мерджить passcount у request) | ✅ |
| 6 | **Квоти (`quota_places`):** відновлено ОРИГІНАЛЬНИЙ onchul-контракт (не порт 3g). Новий `TripsService::getQuotaPlaces()` збирає uuid квотних місць, віддає окремим полем `quota_places` (для довозки — від фідера). Фронт `isQuoted()` + `.tickets-count-quota` вже існували, лише не годувались даними | ✅ |
| 7 | **Баг «Tickets: [45] not available»:** автопідбір у `book()` міняв `placeNumber`/`busId`, але лишав старий `placeUuid` (фідерного місця); `validateOrderData` ловив його у closed_places основного рейсу (спільні uuid, bus_id=4). Фікс: синхронізувати `placeUuid` через `Trip::getPlaceUuidByNumber()` | ✅ |

## Важливі рішення (ADR)

| # | Питання | Рішення | Чому |
|---|---------|---------|------|
| 1 | Друга схема автобуса + двомісний контракт (ADR #6 сесії 15.07) | **Скасовано** → одна фідерна схема 3g | Підміна автобуса в `getTrip` — це і є механізм 3g, а не хак |
| 2 | Право `tickets-transfer-create` | Прибрано повністю | Немає в 3g; `assertCanCreateTransfer` у `bookTransfer()` ламав публічний сайт (403) |
| 3 | Дискримінатор для `virtual_place` | На прапорці **ДИТИНИ**, не батька | Інверсія `is_transfer`: onchul ставить на дитину, 3g на батька — дослівний порт 3g зламав би легасі. Свідоме відхилення від 3g заради легасі |
| 4 | Ціна у відомості | Розведено «ціну показу» (`fiscal_price`, повна) і «ціну суми» (`sum_price`=0 для feeder) | onchul має об'єднану відомість + поле sum, яких у 3g немає — інакше задвоєння виручки |
| 5 | Квоти | Відновлено оригінальний onchul-контракт `quota_places`, НЕ порт 3g `setQuotaClosedPlaces` (мертвий стаб) | Фронт має готовий контракт, який ніколи не годувався; повноцінного quota-as-closed бекенду в onchul не було |
| 6 | Де блокувати місця довозки | На **фідерному** рейсі (як 3g — карта й бронювання читають фідер), не на основному | Рішення користувача, модель 3g. `getFreeSeatsByFromTo` навмисно не чіпали (у 3g теж closed/quota-сліпе) |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Помилкова друга схема + двомісний контракт (внесені 15.07) | Повний відкат до `getAdditionalOptionsTrip()` (одна схема) |
| `assertCanCreateTransfer()` у `bookTransfer()` давав 403 з адмінським текстом клієнту публічного сайту | Право знято повністю (немає в 3g) |
| PDF/email друкували автопідібране місце батька замість обраного місця дитини | Аксесор `getVirtualPlaceAttribute()` з дискримінатором на прапорці дитини |
| Об'єднана відомість задвоювала виручку (9000 замість 4500) | Поле `sum_price`=0 для feeder-ноги, mergeSum по ньому |
| Пошук віддавав довозку доступною при повному ОДНОМУ плечі | Снапшот `original_free_places` + перетин обох плечей |
| Квотне місце показувалось «зайнятим», а не «закритим» | Окреме поле `quota_places` (оригінальний onchul-шлях, не 3g) |
| «Tickets: [45] not available» при бронюванні довозки | Синхронізація `placeUuid` з призначеним місцем (`getPlaceUuidByNumber()`) |
| MySQL 5.7 відвалювався (`SQLSTATE[HY000] [2006]` / `FD_SETSIZE=1024`) за днями аптайму | `brew services restart mysql@5.7`; профілактика — знизити `table_open_cache` |

## Артефакти

**Бекенд:**
- `app/Services/TripsService.php` — видалено `getSystemOptionsTrip`/`buildTransferLegTrip`; додано `getQuotaPlaces()`, `original_free_places` у `getOriginalOptionsTrip`, `loadReportTrip`
- `app/Services/BookingService.php` — видалено `bookExplicitTransferPair`/`bookExplicitTransferLegs`/`$transferTrip`; фікс `placeUuid`-sync у `book()`; знято `assertCanCreateTransfer`
- `app/Entities/System/Ticket.php` — новий `getVirtualPlaceAttribute()`
- `app/Entities/System/Trip.php` — `getPlaceUuidByNumber()`
- `app/Http/Controllers/Api/System/BookingController.php`, `SearchController` (passcount merge)
- `app/Http/Requests/{Booking/BookingRequest, ReassignTicketRequest}.php` — прибрано `transferId`/`tickets[].transfer`
- `app/Crud/Operations/ReassignTicketOperation.php`
- `app/Http/Resources/System/Trip/Report/TripReportTicketsResource.php`
- `app/EXCELExports/Reports/TripExport.php`
- `app/Mail/Admin/Tickets/Ticket.php`, `Mail/.../OrderBookingSold.php`, `Mail/.../OrderTicketsSold.php`
- `lang/uk/permissions.php`, `lang/en/permissions.php` — прибрано ключі `tickets-transfer-create`

**Фронт:**
- Видалено `resources/js/components/booking/Trip/ChooseTransferPlaces.vue`
- `BookTripManager.vue`, `BookPlacesForm.vue`, `TicketReassignManager.vue`, `ChoosePlace.vue` — назад до однієї схеми
- `TripReportManager.vue` — mergeSum по `sum_price`
- Vue-гейти права `tickets-transfer-create` прибрано

**Нові поля/контракти:**
- `sum_price` (0 для feeder-ноги), `quota_places`, `original_free_places`

## Стан і наступні кроки

- **Нічого не закомічено** (~20+ файлів + нові поля). Наступний крок — коміт (розбити по 7 блоках або одним), користувач ще не дав команду.
- **Тести не писали** — рішення користувача (Feature-тести раніше видалені, коміт 5116aa7, ~3800 рядків; покриття лише Unit).
- **Пастка інфри:** агентам заборонено `git stash` (був інцидент — правки побували в stash при зовнішньому мерджі).
- Осиротілий рядок у таблиці `permissions` (`tickets-transfer-create`) видалити руками через адмінку — каскад підчистить пивоти; міграцію не робили.

## Пов'язані нотатки

- [[2026-07-15-transfer-3g-alignment]] — попередня сесія, чиє ключове рішення (друга схема + двомісний контракт) **ця сесія скасовує**
- [[2026-07-14-transfer-dovozka-feature]] — первинне портування довозки з 3g
- [[2026-07-03-trip-report-merge-trips]] — об'єднана відомість (де `sum_price` доречний)
- [[2026-07-03-import-tickets-from-vonchul]] — легасі-квитки з інверсією `is_transfer`
