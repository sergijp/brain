---
title: "Проект: mono-system — імплементація Transfers v2 (Фази 0–6)"
date: 2026-07-29
tags: [mono-system, work, session, transfers]
category: session
project: mono-system
status: completed
aliases: []
pinecone_indexed: false
---

# Проект: mono-system — імплементація Transfers v2 (Фази 0–6)

## Мета сесії

Реалізувати `TRANSFERS-V2-PLAN.md` — замінити ручне парування пересадок на автоматичний
пошук стиковок через хаби. Фази 0–6 у коді, з тестами. Продакшн — окремо.

Процесні вимоги від власника: відмічати зроблене й вести окремий список дій для сервера.

## Виконано

| Фаза | Що зроблено | Результат |
|------|-------------|-----------|
| 0 | Гігієна даних: команда `transfers:cleanup-trip-stations`, FK `SET NULL` → `CASCADE` | **1 190 602** мертвих рядків видалено, таблиця 425 МБ → 138 МБ; CASCADE перевірено відкатним тестом |
| 1 | `is_transfer_hub` на обох pivot; денормалізація `departure_at`/`arrival_at` + 3 індекси; налаштування; команди `backfill-station-timestamps` і `doctor` | запит 276.48 мс / 16 022 рядки → **0.21 мс / 20 рядків** |
| 2 | `ConnectionSearchService` — BFS по хабах із відсіканням за домінуванням, `FRONTIER_CAP=50`, захист від циклів | теплий пошук **60 мс** (21 мс БД, 7 мс BFS, 32 запити) при бюджеті 200–300 мс |
| 3 | `BookingService::bookJourney()` + `buildLegTickets()` + `validateJourney()`; `getJourney` endpoint | один ордер, одна транзакція, 9 перевірок валідності |
| 4 | Каскад скасування й повернення по `journeyChain()`; блокування переоформлення плеча | легасі-пересадки не зачеплені |
| 5 | Чекбокс хаба у формі маршруту; видалено `AddTransferStationPopup` з UI | позначка їде через обидва препроцесори |
| 6 | Пропагація `is_transfer_hub`, `boarding`, `unboarding`, `bus_id` у рейси при генерації | закрито три шляхи, де поля губились |
| — | Тестова інфраструктура: `DatabaseTransactions` по dev-базі | **40 тестів**, ~50–60 с |

## Важливі рішення

Головне рішення винесено в окремий ADR: [[10-Work/Projects/mono-system/decisions/2026-07-29-one-order-per-journey]] —
подорож зберігається як **один ордер**. Це викреслило з плану multi-order checkout,
зміни у вебхуках платіжок і сутність `journey_uuid`.

| Питання | Рішення | Чому |
|---------|---------|------|
| Чи вимагати хаб з обох боків пересадки | Ні, тільки на плечі, що **приїжджає** (`REQUIRE_HUB_ON_DEPARTURE = false`) | інакше адміну довелося б позначати вдвічі більше станцій |
| Тестова база | dev-база в транзакціях (`DatabaseTransactions`) | «дешева альтернатива»; `RefreshDatabase` витер би dev — заборонено в докблоці `TransfersTestCase` |
| Легасі-код пересадок | **Не видаляти** | `getAdditionalOptionsTrip` викликається з `Busfor/TripController:56` і `External/TripController:73` — видалення зламало б партнерські API |
| Захист від розсинхрону часів | Хук `TripStation::saving` | нуль зайвих запитів на гарячому шляху: мовчить, якщо `departure_at` є і час не змінювався |

## Проблеми й як вирішили

- **Знайдено 4-й шлях розсинхрону денормалізованого часу, якого план не передбачав.**
  - **Причина:** адмін може редагувати час станції прямо на рейсі через CRUD, минаючи
    і `createTrip`, і `syncWithRoute`. Плюс зміна `trips.date` зсуває час усіх станцій,
    не торкаючись їхніх рядків.
  - **Фікс:** хук `TripStation::saving` + `TripObserver::updated`. Обидва описані в
    [[10-Work/Projects/mono-system/docs/connection-search]].

- **Власник продукту зупинив зміни у сторонніх API.**
  - **Причина:** я змінив 5 API-ресурсів, щоб віддавати плечі подорожі. Для `GlobalApi`,
    `ExternalApi` і `BusforApi` подорож має виглядати як **одна поїздка й один квиток**.
  - **Фікс:** усі 5 ресурсів відкочено через `git checkout`. Обмеження внесено в пам'ять.

- **Регресія в моєму ж коді:** `isJourneyLeg()` спочатку перевіряв лише наявність
  `parent_id`. Легасі `bookTransfer` теж його ставить — я б заблокував переоформлення
  легасі-пересадок. Звужено до перевірки «в тому самому ордері», додано окремий тест.

- **⚠️ Виправлення власного твердження про checkout.** У `BookingController::getPaymentForm`
  стояло `'amount' => $request->input('amount') * count($tickets)` — множення ціни одного
  квитка на кількість. Я замінив це на `$order->amount` і подав як фікс живого бага.
  **Перевірка 2026-07-29 показала, що метод ніде не зареєстрований** (`grep` по `routes/` —
  жодного маршруту), а всередині ще й падає на `Tenancy::getTenant()` — фасаді, вирізаному
  разом із tenancy. Живі шляхи LiqPay (`SiteApi`/`GlobalApi` `OrderController::getFormData`)
  **завжди використовували `$order->amount`** і зламані ніколи не були.
  Зміна коректна, але правила мертвий код.

- **Статичний кеш автобусів у тестовому сценарії переживав відкат транзакції** →
  12 помилок FK. Мемоізацію прибрано повністю.

## Крок 2 — фікси (2026-07-29)

### Валюта в сесії

`Currency::current()` — сесія, а якщо порожня, то валюта з `default = 1`. Той самий
фолбек уже був у `Route::getClearPrice` і `Trip::getClearPriceFromTo`, у решті місць
його забули. Патерн `where('code', Session::get('currency'))->first()->id` знайдено
в **7 місцях**; виправлено 4 живих: `Trip::getClearPriceBuCurrentStations`,
`Ticket::getTripPrice`, `BookingService` ×2 (там `$currency` мовчки ставав null
і осідав у `orders.currency_id`).

Поза HTTP сесія порожня завжди — сесію заповнює `Controller::__construct`. Тобто
падало все, що йде з команди, джоби чи черги.

### N+1 у `Route::createTrip` — виявився значно гіршим

Заміряно на маршруті #29 (41 станція, 504 ціни): **7610 запитів, 4160 мс**.
Мій попередній звіт «458 запитів» був заниженим.

Розклад: ліниві `from`/`to` на кожній ціні тягли RouteStation, ті через `$with`
— станцію з текстами, а `create()` додавав вставку, читання назад, запит валюти
і запис в activity_log, чий опис ще й питав рейс.

Фікс: eager-load `from`/`to` з `->without('station')` + bulk insert цін пачками.
**Стало 54 запити, 137 мс** — у 140 разів менше запитів, у 30 разів швидше.
Джоба генерації рейсів ходить щодня.

### 🔴 Побічна знахідка: activity_log роздутий автогенерацією

`activity_log` — **853 МБ, 1 239 597 рядків**, з них **455 647 (37%) — `TripPrice`**,
тобто записи про автозгенеровані ціни, які ніхто не читає. Bulk insert їх більше
не створює; ручне редагування цін іде через CRUD і логується як раніше.

Історичні 455 тис. рядків лишились — чистка потребує окремого рішення.

### Activity-лог станції маршруту

`RouteStation::getDescriptionForEvent` падав на `$this->route->name`, коли маршрут
невидимий через глобальний скоуп. Зроблено null-safe: побічна дія більше не валить
основну операцію. Заодно додано `is_transfer_hub` у список полів, що логуються.

### Мертвий tenancy-код

Клас `App\Entities\System\Website` і фасад `Tenancy` **не існують** (перевірено
`class_exists` = false), але згадуються в 13 файлах. Видалено те, на що немає
жодного посилання: `CreateTenant`, `TriggerUpdatedEventOnTenants`, `UpdateUsers`,
`Listeners/Tenant/CacheSettings`, `config/tenancy.php`. У `EventServiceProvider`
прибрано 6 імпортів неіснуючих лістенерів.

`config('settings')` заповнює `AppServiceProvider::boot()` — `CacheSettings` був
закоментований у `$listen` і ні на що не впливав.

### phpunit.xml

`<coverage processUncoveredFiles>` → `<source>`. Попередження зникло.

**Після всіх фіксів: 40 тестів проходять, застосунок піднімається, 525 маршрутів.**

## Знайдено, але не виправлено — потребує рішення власника

| Що | Де | Чому не чіпав |
|----|-----|---------------|
| Публічний ендпоінт падає на `Website::query()` | `LoginController::customerRegistration`, зареєстрований у `routes/api.php:25` | видалення живого маршруту — рішення власника |
| Мертвий метод із фатальним `Tenancy::getTenant()` | `BookingController::getPaymentForm` | ніде не зареєстрований; видалити чи лишити — рішення власника |
| Клас пошти падає в конструкторі, ніде не інстанціюється | `Mail\Admin\Tickets\TicketsSold` | імпортується в `PrivatBank/OrderController` — тека сторонніх API |
| Метод посилається на неіснуючий клас, ніде не викликається | `ConvertData::convertToCurrenciesSite` | `App\Entities\Tenant\Directories\Currency` не існує |
| ~~Рахує від рейсу ордера = перше плече~~ — **хибна тривога**, перевірено 2026-07-29: віддає кількість пасажирів, а не плечей, тобто «один квиток на подорож». Міняти не треба | `orderedTickets`, `GlobalApi`/`SiteApi` `OrderCreatedResource:123` | закрито, крок 8 |
| 455 тис. рядків `TripPrice` в `activity_log` (853 МБ) | історичні дані | чистка потребує окремого рішення |

## Аналіз реальних даних (2026-07-29)

73 маршрути, 1748 `route_station`, 428 станцій, 786 майбутніх рейсів, **0 позначених хабів**.

Топ міст за кількістю маршрутів майже точно збігся з `mainHubs` з еталонної карти
`~/Downloads/interactive-map-original.html`: Умань 42, Вінниця 41, Хмельницький 41,
Чернівці 37, Дніпро 34, Львів 31, Харків 24, Херсон 16.

**Позначення 8 міст вручну = 298 чекбоксів у 61 формі маршруту** + 4988 рядків
у `trip_station` майбутніх рейсів. Звідси рішення робити команду `transfers:mark-hubs`.

**Пастка:** у 5 містах-хабах більше однієї станції (Львів `#155`/`#156`, Харків,
Дніпро, Чернівці, Тернопіль). Пошук збігає плечі строго за `station_id` — позначати
треба **всі** станції міста.

Легасі-парування виявилось майже порожнім: **1** запис `transfer_id` на `route_station`
і 200 на `trip_station`. Тому початкова ідея команди-конвертера втратила сенс.

## Артефакти

**Нові файли:**
```
app/Services/ConnectionSearchService.php
app/Helpers/TransfersSettings.php
app/Observers/TripObserver.php
app/Console/Commands/{CleanupTripStations,BackfillStationTimestamps,TransfersDoctor}.php
config/transfers.php
tests/Feature/Transfers/          (6 файлів, 40 тестів)
TRANSFERS-V2-SERVER-ACTIONS.md
```

**Міграції:** `database/migrations/2026_07_28_1[23]*` — 6 штук, усі ідемпотентні
через `information_schema` (прод і dev розійшлися по схемі).

**Команди:**
```bash
php artisan transfers:cleanup-trip-stations --dry-run
php artisan transfers:backfill-station-timestamps
php artisan transfers:doctor            # exit 1, якщо вмикати прапорець ще не можна
php artisan test --testsuite=Feature --filter=Transfers
```

## Наступні кроки

12 кроків, з них 8 до rollout. Порядок узгоджено з власником 2026-07-29:
vault-документація → фікси → плечі в квитку → drop `journey_uuid` → тест видимості →
лог повільних пошуків → перевірка сторонніх API → `orderedTickets` → rollout →
документація адміна → прод → скріни.

**Прапорець `transfers_v2_enabled` лишається нулем.** На проді не виконано жодного кроку.

Викинуто з плану: батчинг місць (60 мс — нема що оптимізувати), precomputed стиковки,
CI, видалення легасі-коду. Кеш результатів у Redis відкладено на майбутнє —
головна перешкода в тому, що в результаті лежить кількість вільних місць.

## Пов'язані нотатки

- [[10-Work/Projects/mono-system/project-overview]]
- [[10-Work/Projects/mono-system/docs/INDEX]]
- [[10-Work/Projects/mono-system/docs/connection-search]]
- [[10-Work/Projects/mono-system/decisions/2026-07-29-one-order-per-journey]]
- [[10-Work/Projects/mono-system/sessions/2026-07-20-plans-verification-transfers-v2-analysis]]
