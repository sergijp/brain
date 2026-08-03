---
title: "Пошук стиковок (Transfers v2) — архітектура"
date: 2026-07-29
tags: [mono-system, architecture, transfers, search]
category: docs
project: mono-system
status: active
aliases: ["mono-system-connection-search", "transfers-v2"]
pinecone_indexed: false
last_verified: 2026-08-03
---

# Пошук стиковок (Transfers v2)

## Контекст

До v2 пересадки задавались **вручну**: адмін на станції маршруту вказував конкретний
інший маршрут (`route_station.transfer_id` + `transfer_station_from_id`/`transfer_station_to_id`).
Одна станція — одна заздалегідь прописана пересадка. Це не масштабується: у базі
73 маршрути, і руками попарно зв'язати їх неможливо. Станом на 2026-07-29 у базі
рівно **1** такий запис на `route_station` і **200** на `trip_station`.

v2 замінює це на **автоматичний пошук**: адмін позначає станцію як **хаб**
(`is_transfer_hub`), а система сама знаходить усі комбінації рейсів, які через цей
хаб стикуються.

Що треба знати, щоб не зламати:

- Пошук працює **за прапорцем** `transfers_v2_enabled`. Вимкнений = система поводиться
  рівно як до v2.
- Легасі-пересадки **не видалені** і продовжують працювати паралельно.
  Див. [[2026-07-29-one-order-per-journey]] про те, як вони розрізняються.
- Пошук читає `trip_station.departure_at`/`arrival_at` — **денормалізовані** колонки.
  Якщо вони розійдуться з `time`/`trip_day`/`trips.date`, пошук почне брехати.

## Модель

```
station A ──рейс 1──▶ ХАБ ──рейс 2──▶ station B
                      ▲
                 is_transfer_hub = 1
              (на trip_station рейсу, що ПРИЇЖДЖАЄ)
```

Подорож (journey) = 2–3 плечі. Кожне плече — відрізок одного рейсу від станції до станції.
Пересадка можлива лише там, де плече, яке **приїжджає**, має `is_transfer_hub = 1`.

| Сутність | Роль |
|----------|------|
| `route_station.is_transfer_hub` | де адмін ставить позначку (джерело істини) |
| `trip_station.is_transfer_hub` | копія на рейсі; саме її читає пошук |
| `trip_station.departure_at` / `arrival_at` | денормалізований абсолютний час |
| `settings.transfers_*` | параметри пошуку, кешуються в `config('settings.*')` |

## Ключові контракти

1. **Прапорець вимикає все.** `transfers_v2_enabled = 0` ⇒ `searchTrips` не повертає
   `journeys`, `bookJourney` недосяжний. Відкат = один рядок у `settings`.

2. **Позначка живе на маршруті, копіюється в рейс.** Адмін ставить на `route_station`.
   У `trip_station` вона потрапляє двома шляхами: при генерації (`Route::createTrip`)
   і при синхронізації (`Trip::syncWithRoute`). Пошук читає **тільки** `trip_station`.

3. **`departure_at`/`arrival_at` мусять збігатися з формулою.** Формула — та сама,
   що в `Trip::scopeStationsQuery`:
   `TIMESTAMP(trips.date + INTERVAL trip_day DAY + INTERVAL time.HH HOUR + INTERVAL time.mm MINUTE)`.
   PHP-версія (`TripStation::scheduleTimestamp`) навмисно **додає інтервали**, а не
   використовує `setTime()` — щоб збігатися з MySQL при переході через добу.

4. **`journeyId` від клієнта — недовірений.** Це base64 масиву `{trip_id, from_id, to_id}`,
   підробний. `BookingService::validateJourney()` перевіряє все наново перед бронюванням:
   станції належать рейсам, порядок `order`, посадка/висадка дозволені, плечі стикуються
   на одній станції, ця станція — хаб, layover у вікні, маршрути різні, станції не
   повторюються, рейс активний і не закритий.

5. **Подорож = один ордер.** Див. [[2026-07-29-one-order-per-journey]].

6. **Пересадка збігається строго за `station_id`.** Не за містом. Наслідок — див. Gotchas.

## Алгоритм

`app/Services/ConnectionSearchService.php`

BFS по хабах із відсіканням. Працює на «скелеті» — `trip_id, station_id, order,
departure_at, arrival_at, is_transfer_hub` через Query Builder, **без моделей Eloquent**.

| Метод | Рядок | Що робить |
|-------|-------|-----------|
| `searchJourneys()` | 50 | вхідна точка; повертає Collection подорожей |
| `firstFrontier()` | 94 | перший рівень: усі плечі зі стартових станцій |
| `expand()` | 131 | наступний рівень BFS |
| `pruneFrontier()` | 207 | відсікання за домінуванням + `FRONTIER_CAP = 50` |
| `findLegs()` | 233 | один SQL: `trip_station f × trips × routes × trip_station tt` |
| `enrich()` | 284 | ціни й місця — **лише** для фінальних top-N |
| `assembleJourney()` | 320 | збирає JSON подорожі |
| `dataReady()` | 427 | чи заповнені `departure_at` (кеш 300 с) |

**Дороге рахується в кінці.** Ціни (`getTripPriceFromTo`) і місця (`getTripPlaces`)
викликаються тільки для `transfers_max_results` (10) фінальних подорожей, відсортованих
за сумарним часом у дорозі. Це зводить дорогу частину з сотень викликів до ~20–30.

**Заміряно на dev (2026-07-28):** теплий пошук 60 мс сумарно — 21 мс БД, 7 мс BFS,
32 запити. Бюджет був 200–300 мс.

## Денормалізація — навіщо

Було: час станції обчислювався в SQL на льоту з `trips.date + trip_day + JSON time`.
Обчислений вираз **не індексується** — MySQL мусив прочитати всі рядки й порахувати кожен.

Стало: `departure_at`/`arrival_at` — фізичні колонки з індексами.

**Заміряно:** старий запит 276.48 мс, скановано 16 022 рядки → новий **0.21 мс**, 20 рядків.

Індекси на `trip_station`:
`(station_id, is_transfer_hub, departure_at)`, `(station_id, departure_at)`, `(trip_id, order)`.

## ⚠️ Чотири шляхи запису — де може виникнути розсинхрон

Це найкрихкіше місце підсистеми. Денормалізована колонка правдива лише поки **всі**
шляхи запису її оновлюють. Знайдено чотири:

| # | Шлях | Хто оновлює | Файл |
|---|------|-------------|------|
| 1 | Генерація рейсу з маршруту | `Route::createTrip` — інжектить у масив | `Route.php:344` |
| 2 | Синхронізація рейсу з маршрутом | `Trip::syncWithRoute` | `Trip.php:417` |
| 3 | **Зміна `trips.date`** | `TripObserver::updated` | `Observers/TripObserver.php:15` |
| 4 | **Редагування станції рейсу через CRUD** | хук `TripStation::saving` | `TripStation.php:122` |

Шляхи **3 і 4 план не передбачав** — знайдені при реалізації.

- **№3:** зміна дати рейсу зсуває час усіх його станцій, не торкаючись їхніх рядків.
  Обсервер перераховує їх усі.
- **№4:** адмін редагує час станції прямо на рейсі. Хук `saving` ловить це.
  Він навмисно **нічого не робить**, якщо `departure_at` уже заповнене й
  `trip_day`/`time`/`time_arrival` не змінились — тобто **нуль зайвих запитів** на
  гарячому шляху.

**Страховка:** `php artisan transfers:doctor` порівнює збережені значення з формулою
й повертає exit 1, якщо є розбіжність. Запускати перед вмиканням прапорця.

## Callsite-и

| Файл | Що |
|------|-----|
| `app/Services/ConnectionSearchService.php` | пошук |
| `app/Services/BookingService.php` | `bookJourney()`, `buildLegTickets()`, `validateJourney()` |
| `app/Http/Controllers/Api/System/BookingController.php` | `searchTrips` (+`journeys`, `search_ms`), `getJourney`, `bookTickets` |
| `app/Entities/Tenant/Ticket.php` | `journeyChain()`, `isJourneyLeg()`, `scopeWithoutLegacyTransferChildren()`, `number_html` |
| `app/Http/Controllers/Api/Crud/TicketsCrudController.php` | список квитків: скоуп + eager-load parent/child |
| `app/Http/Controllers/Api/Crud/Community/ClientsListCrudController.php` | квитки клієнта: той самий скоуп |
| `app/Entities/Tenant/TripStation.php` | `scheduleTimestamp()`, `applyScheduleTimestamps()`, хук `saving` |
| `app/Helpers/TransfersSettings.php` | типізовані геттери налаштувань |
| `app/Console/Commands/TransfersDoctor.php` | перевірка перед вмиканням |
| `app/Console/Commands/BackfillStationTimestamps.php` | заповнення часів для існуючих рейсів |
| `app/Console/Commands/CleanupTripStations.php` | чистка мертвих рядків (Фаза 0) |

## Налаштування

`settings` → `config('settings.*')`, дефолти в `config/transfers.php`.

| Ключ | Дефолт | Що робить |
|------|--------|-----------|
| `transfers_v2_enabled` | 0 | головний прапорець |
| `transfers_max_legs` | 3 | максимум плечей |
| `transfers_min_layover_minutes` | 30 | мінімум на пересадку |
| `transfers_max_layover_minutes` | 1440 | максимум (доба — через нічні стиковки) |
| `transfers_max_results` | 10 | скільки подорожей збагачувати й віддавати |
| `transfers_slow_search_ms` | 500 | поріг логування в канал `transfers`; `0` вимикає |

## Спостереження

Повільні пошуки пишуться в `storage/logs/transfers-slow-YYYY-MM-DD.log` (канал `transfers`,
ротація 30 днів). У контексті: станції, дата, `max_legs`, скільки запитів і рядків з'їв BFS,
скільки подорожей знайдено й віддано, `user_id`.

Навіщо окремий файл: швидкість залежить від даних, які змінюються щодня — рейси
генеруються й від'їжджають. Скаргу «пошук висів у вівторок» у четвер уже не відтворити.
У спільному `laravel.log` такий запис потонув би.

У відповіді `searchTrips` є ще `search_ms` — миттєва метрика на час rollout.

## Gotchas / підводні камені

- **У місті може бути кілька станцій, і пошук їх не об'єднує.** Львів — це
  `#155 «Львів Автовокзал»` (30 маршрутів) і `#156 «Львів»` (29). Так само роздвоєні
  Харків, Дніпро, Чернівці, Тернопіль. Якщо плече приїжджає на один вокзал, а наступне
  їде з іншого — **стиковки не буде**. Тому позначати хабом треба **всі** станції міста.
  Зворотний бік правильний: пошук ніколи не запропонує пересадку між двома вокзалами
  одного міста — пасажира не змусять їхати через місто.

- **Легасі-пересадки живі паралельно.** `TripsService::getAdditionalOptionsTrip:183`
  підміняє рейс на пов'язаний, якщо на станції стоїть `transfer_id`. Цей метод
  викликається зокрема з `Busfor/TripController:56` і `External/TripController:73` —
  **видаляти його не можна**, зламає партнерські API.

- **`orders.trip_id` для подорожі — це лише перше плече.** Будь-який підрахунок
  «від рейсу ордера» побачить тільки його. Але це не завжди помилка: `orderedTickets`
  у `GlobalApi`/`SiteApi` `OrderCreatedResource:123` рахує саме так — і **правильно**,
  бо віддає кількість пасажирів, а не плечей, тобто «один квиток на подорож».
  Заміряно 2026-07-29: подорож на 2 пасажирів → 2, а не 4. Міняти не треба.

- **Партнерські API не захищені від чужої подорожі.** Створити її вони не можуть
  (немає жодного посилання на `ConnectionSearchService`/`bookJourney`; `create` бере
  один `trip_id`). Але якщо подорож до них потрапить, `OrderinfoResource` віддасть
  **два квитки на двох рейсах**, а `RetinfoResource` — лише перше плече з половиною
  ціни. Досяжним це робить те, що `GlobalApi\OrderController::orderinfo` і
  `External`/`Busfor` `getOrderWithTickets` **не фільтрують за `member_id`**.
  Перевірено практично 2026-07-29; рішення власника не ухвалене.

- **Списки квитків ховали друге плече.** У `TicketsCrudController::setupListOperation`
  і `ClientsListCrudController::getTicketsByClient` стояло `whereNull('parent_id')` —
  фільтр, що ховав «тіньові» квитки legacy-пересадок (113 штук у базі, часто з ціною 0).
  Плече v2 має `parent_id` так само й теж зникало: квиток пересадкового рейсу не можна
  було ні відкрити, ні роздрукувати. Замінено на скоуп
  `Ticket::scopeWithoutLegacyTransferChildren()` — «корінь **або** батько в тому самому
  ордері». Перевірено 2026-08-03: ховає рівно ті самі 113 рядків, що й раніше.
  **Будь-який новий список квитків має вживати цей скоуп, а не `whereNull('parent_id')`.**

- **Опис подорожі збирає `Ticket::journeySummary()`.** Повертає плечі, пересадки й повну
  суму, або `null` для звичайного квитка й legacy-пересадки. Метод живе на моделі, бо
  потрібен двом місцям: полю `journey_legs` у картці квитка (`GetJourneyLegsField`) і
  PDF-квитку, який отримує пасажир (`pdf.ticket.index`, змінна `$journey`). Раніше логіка
  була тільки в CRUD-полі, і PDF нічого про подорож не знав — пасажир бачив «Прага → Львів»
  без згадки, що далі є друге плече.

- **Дефолтний фільтр списку квитків розривав подорож.** Без заданих фільтрів
  `TicketsCrudController` показує лише квитки з рейсами **на сьогодні**. Плечі подорожі
  майже завжди їдуть різними днями (перше сьогодні, друге завтра), тож одразу після
  продажу оператор бачив половину. Додано `orWhere`: показати квиток, якщо інше плече
  того самого ордера їде сьогодні. `whereNotNull('parent_id')` стоїть **перед** підзапитом
  — без цього відсіву EXISTS виконувався б для кожного зі 100 тис. квитків і список
  важчав уп'ятеро (1110 мс проти 221; з відсівом — 201 мс). `where`, а не `whereDate`:
  `trips.date` має тип DATE та індекс, функція над колонкою його вимикає.
  Свідоме обмеження: якщо перше плече проїхало вчора, у дефолтному списку його не буде.

- **`getJourney` мусить вантажити `tickets`.** Карта місць (`BusPlaces::isBooked`)
  рахує зайняті **виключно** з `trip.tickets`. У `getJourney` цього eager-load спершу
  не було, і оператор бачив повністю вільний автобус на першому плечі. Набір полів той
  самий, що в `getTrip`: `trip_id, place, from_id, to_id` + `activeStatus()`.

- **Автопідбір місць іде з кінця салону.** `buildLegTickets` робить `reverse()` над
  `getFreeSeatsByFromTo()` — передні місця цінніші й лишаються під ручний продаж.
  `reverse()` навмисно **в `buildLegTickets`, а не в `getFreeSeatsByFromTo`**: той метод
  викликають ще сім місць, зокрема `GlobalApi` й `SiteApi` `OrderController` — зміна
  порядку в ньому поїхала б у зовнішні контракти. «Кінець» тут — кінець у порядку схеми
  автобуса, а не «найдалі від водія».

- **Глобальні скоупи не діють на Query Builder.** `TripScope`/`TicketScope`/`RouteScope`
  застосовуються тільки до Eloquent. BFS іде через Query Builder, тому фільтри
  (активність, `sales_closed`, доступні маршрути агента) **продубльовані вручну**
  в `findLegs()`. Змінили скоуп — перевірте `findLegs`.

- **Тести ганяються по dev-базі в транзакціях.** `DatabaseTransactions`, ніколи
  `RefreshDatabase` — останній витер би dev-базу. Це зафіксовано в докблоці
  `TransfersTestCase`. CI немає, тести запускаються вручну.

- **Дефолт `REQUIRE_HUB_ON_DEPARTURE = false`.** Хаб потрібен лише на плечі, що
  приїжджає. Якби вимагали з обох боків, довелося б позначати вдвічі більше станцій.

## Пов'язані

- [[INDEX]]
- [[2026-07-29-one-order-per-journey]] — ADR про один ордер
- Tier-2 pointer: `~/.claude/projects/-Users-serhiin-Data-Source-mono-system/memory/architecture_connection_search.md`
- План у репозиторії: `~/Data/Source/mono-system/TRANSFERS-V2-PLAN.md`
- Дії на сервері: `~/Data/Source/mono-system/TRANSFERS-V2-SERVER-ACTIONS.md`
