---
title: "Синхронізація квитків Bussystem (get_tickets) — архітектура"
date: 2026-07-30
tags: [mono-system, architecture, bussystem, infobus, sync]
category: docs
project: mono-system
status: active
aliases: ["mono-system-bussystem-sync", "get_tickets", "infobus-sync"]
pinecone_indexed: false
last_verified: 2026-07-30
---

# Синхронізація квитків Bussystem (get_tickets)

## Контекст

Квитки, продані через дилерську мережу bussystem, треба затягувати до нас.
Історично це робив **HTML-скрапер** кабінету диспетчера
(`App\Services\InfobusService` + `SyncInfobusTicketJob` + `ChackedStatusInfobusTicketJob`).
Скрапер вимкнено; замість нього — офіційний JSON/XML-метод
[`get_tickets`](https://bussystem.eu/api/uk/reports/dispatcher/get_tickets/).
Код скрапера лишається в репозиторії як fallback, але в розкладі закоментований.

Станом на 2026-07-30 нова інтеграція теж **не увімкнена** в
`app/Console/Kernel.php` — блокер: whitelist серверного IP на боці bussystem.

## Компоненти

```
App\Services\BussystemDispatcherService        ← HTTP + парсинг + мапінг у legacy-форму
App\Services\Bussystem\
   ├─ BussystemTicketWindowFetcher             ← тягне вікна дат, дедуп за ticket_id
   ├─ BussystemTicketStatusResolver            ← класифікує/застосовує перехід статусу
   └─ BussystemFailureReporter                 ← класифікація збою + Telegram
App\Jobs\Trips\SyncBussystemTicketJob          ← основний синк (кожні 15 хв)
App\Jobs\Trips\SyncBussystemTicketStatusCheckJob ← звірка далеких вікон (раз на добу)
App\Jobs\Tickets\CreateTicketJob               ← створення квитка (спільний зі скрапером)
```

Резолвер, фетчер і репортер спільні для обох джоб **і** для dry-run роуту
`GET /api/test-bussystem-sync` — саме тому вони винесені: до цього роут мав
власну копію класифікації й устиг розійтися з реальною поведінкою джоби.

## Вікна дат

API дозволяє інтервал **не більше 31 дня** (помилка `max_31days`); всюди
жорстко обмежено 29.

| Джоба | Вікна | Навіщо |
|---|---|---|
| `SyncBussystemTicketJob` | `buy`: сьогодні..сьогодні | нові продажі, у т.ч. на далекі рейси |
| | `departure`: сьогодні..+N (`infobus.sync_days_ahead`, 0 = вимкнено) | звірка: повернення, переноси, броні |
| `SyncBussystemTicketStatusCheckJob` | `departure`: [+1..+29], [+30..+58], ... × `infobus.status_check_windows` | квитки на рейси ДАЛІ, ніж дістає перша джоба |

Друга джоба обходить **одне вікно за виконання** й сама диспатчить наступну —
інакше N послідовних викликів по 120 с не влізли б у `$timeout`/`retry_after`.
Захищена `WithoutOverlapping('bussystem-status-check')->dontRelease()`.

## Матриця статусів

`ticket.status` з API → локальна дія:

| API | Локально є? | Дія |
|---|---|---|
| `cancel` | так | → `CANCELLED` + `canceled_at`, **каскадом на `childTicket`** |
| `cancel` | ні | нічого |
| `reserve` | ні | створити як `PREBOOKED` |
| `reserve` | так | нічого |
| `buy` | ні | створити як `SOLD` |
| `buy` | так, `PREBOOKED` | → `SOLD` (бронь викупили) |
| `buy` | так, інше | нічого |
| інше | — | `Log::warning` |

Друга джоба працює з `canCreate: false` — `buy`/`reserve` без локального квитка
рахується як `missing_locally`, а не створюється.

## ⚠ Передумова запуску: сідер aliases

`bussystem_city_aliases` **має бути заповнена** до вмикання синку:

```bash
php artisan db:seed --class=BussystemCityAliasSeeder
```

Сідер **не входить** у `DatabaseSeeder`, тож на свіжому оточенні таблиця
порожня. А порожня таблиця означає, що `resolveRouteStation()` повертає `null`
завжди → `CreateTicketJob` не знаходить жодної станції → **кожен** квиток синку
падає в `error_tickets`. Фолбеку немає (на відміну від 3g, де лишився ще й
legacy LIKE по `texts.title`).

Заміряно на локальній копії 2026-07-31:

| Стан | Резолвиться міст реальних маршрутів |
|---|---|
| таблиця порожня (як зараз) | **0 із 16** |
| після сідера (729 записів, 364 міста) | **13 із 16** |

Решта 3 — Utena і Gdynia: цих міст немає в наших `cities`/`texts` узагалі, тож
для них помилка резолву коректна.

## Дедуп перед бронюванням (два бар'єри в CreateTicketJob)

1. **По `ticket_api`** — квиток уже заведений синком. `withoutGlobalScope` +
   `whereNull('parent_id')`.
2. **По пасажиру** — той самий пасажир уже заведений МЕНЕДЖЕРОМ вручну. Такий
   квиток не має `ticket_api`, тож бар'єр 1 його не бачить, і синк забронював би
   ту саму поїздку вдруге (друге місце, друге замовлення).

Ключ бар'єра 2: **рейс + агент + телефон + ім'я**.

| Складова | Як нормалізується / чому саме так |
|---|---|
| телефон | останні 9 цифр — `380671112233`, `0671112233`, `+38 (067) 111-22-33` дають один ключ |
| ім'я | токени `name+surname`, lowercase, **відсортовані** — менеджер міг ввести у зворотному порядку, а з API це один рядок, що ріжеться по пробілу |
| агент | `order.member_id = config('infobus.member_id')` — заводячи квиток, менеджер вказує агента, від якого той прийшов |
| місце | **не входить у ключ** — менеджер міг пересадити, його розсадка головна |
| відрізок | уточнення, не жорсткий фільтр: спершу точний збіг `from_id`/`to_id`, інакше збіг по рейсу + warning |

**Фільтр по агенту — захисний, не косметичний.** Заміряно на живих даних
(2026-07-31): квитки з `ticket_api` майже всі під `INFOBUS API (177562)` —
12 463 шт., а ручні без `ticket_api` на майбутніх рейсах лежать під зовсім
іншими агентами (`site`, `Busfor API`, `Закарпатавтотранс`, `KLR bus`,
`ElinTrans`) — жодного під 177562. Без фільтра збіг телефон+ім'я прив'язав би
`ticket_api` до квитка чужого каналу продажу. Хибне спрацювання тут гірше за
пропущений дубль.

При збігу — `ticket_api` прив'язується до наявного квитка, **місце/статус/ціна
не чіпаються**, застарілий `error_ticket` прибирається. Ідемпотентно: наступний
прохід ловить бар'єр 1.

Бар'єр 2 стоїть **після** підбору місця, але **перед** записом — тому квиток, що
інакше впав би з «немає вільних місць» (бо місце вже зайняте його ж ручним
двійником), тепер просто прив'язується.

## Пастки (все — реальні баги, не гіпотези)

1. **Каскад на друге плече пересадки.** Дочірній квиток має **той самий
   `ticket_api`**, що й батьківський (звʼязок через `parent_id`). Без каскаду
   скасування лишало друге плече `SOLD` назавжди. Перевірка дитини має
   відпрацьовувати **навіть якщо батько вже CANCELLED** (його могли скасувати
   через адмінку).
2. **`TicketScope` ховає квитки.** Джоби не викликають `setUserResolver()`, тож
   `request()->user()` — випадковий залишок від іншої джоби на тому ж воркері.
   Скрізь потрібен `withoutGlobalScope(TicketScope::class)`. Окремо: ліниве
   `$ticket->childTicket` **наново застосовує скоуп** і повертає `null` — треба
   `->childTicket()->withoutGlobalScope(...)->first()`.
3. **`whereNull('parent_id')`** у пошуку існуючих — інакше дочірній квиток
   зійде за «квиток уже є» і заблокує створення батьківського.
4. **`array_map('strval', array_keys(...))`** — `array_keys()` кастує числові
   рядкові ключі до int, PDO біндить їх цілими проти `varchar`, MySQL кастує
   КОЛОНКУ → індекс на `ticket_api` не працює.
5. **`0000-00-00 00:00:00`** у `cancel_timedate` — валідний вхід для
   `strtotime()`, але MySQL strict mode кидає `QueryException` при записі в
   `canceled_at`. Нормалізується в `BussystemTicketStatusResolver::normalizeTimedate()`.
6. **`ticket.seat === '***'`** = «місце не закріплене». Без прапорця `freePlace`
   `(int)'***' === 0`, і пасажиру перше вільне місце **закріплювалось** як його
   власне — загроза подвійного продажу.
7. **Порожня назва маршруту** → `LIKE '%%'` матчить усі рядки `route_api_route`.
   Потрібен guard + `ESCAPE` (назва приходить ззовні).

## Черга й таймаути

`infobussync` крутиться на окремому queue-зʼєднанні **`redis-long`**
(`config/queue.php`) з `retry_after = 300` замість 60. Причина: HTTP-виклик
`get_tickets` за докою триває до 120 с, і при `retry_after = 60` воркер вважав би
джобу завислою й брав її **вдруге паралельно**. Піднімати `retry_after` у
звичайному `redis` не можна — воно спільне для всіх джоб.

Ланцюжок обмежень, який треба тримати узгодженим:

```
config('infobus.timeout') = 120        ← один HTTP-виклик
   ↓
SyncBussystemTicketJob::$timeout = 260 ← до 2 послідовних викликів + запас
SyncBussystemTicketStatusCheckJob::$timeout = 150 ← 1 виклик + запас
   ↓
queue.connections.redis-long.retry_after = 300  ← має бути більшим за обидва
```

`config/horizon.php` → `supervisor-2` вказує на `redis-long`. Після зміни —
`php artisan horizon:terminate`.

## Класифікація збоїв

`BussystemDispatcherService` повертає `error_type`; `BussystemFailureReporter`
вирішує, що з ним робити:

| `error_type` | Лог | Telegram | Кидає виняток (→ ретрай Horizon) |
|---|---|---|---|
| `credentials` (`dealer_no_activ`) | error | так | **ні** — саме не полагодиться |
| `infrastructure` (403, обрив мережі) | error | так | **так** — може минути |
| `params` (`max_31days`, формат дат) | error | ні | ні — баг у коді |
| `generic` | warning | ні | ні |

Telegram рейт-лімітований: один алерт на `error_type` раз на 60 хв, ключ спільний
для обох джоб (одна поломка зачіпає обидві).

## Дебаг-роути

- `GET /api/test-bussystem-raw` — сирий payload, усі поля без обробки
- `GET /api/test-bussystem-sync` — dry-run: розклад по діях резолвера +
  причини падінь, **без жодного запису**

## Що НЕ реалізовано (і чому)

Референсна реалізація в проєкті `3g` має додатково: числові рівні резолвінгу
станцій (`bussystem_station_ids`, `bussystem_point_cities`,
`route_api_route.route_api_id` + backfill), дизамбігуацію маршруту/рейсу за
`route.time_from`, детермінований tie-break при кількох станціях-кандидатах,
дедуп ручних квитків без `ticket_api`.

Наразі `resolveRouteStation()` резолвить лише на рівні міста через
`bussystem_city_aliases` і робить `->first()` при кількох кандидатах —
недетерміновано.

**Заміряно на локальній копії БД (2026-07-30, 101 902 квитки):**

| Метрика | Значення | Висновок |
|---|---|---|
| дочірні квитки (`parent_id` не null) | **113** | каскад скасування потрібен — не гіпотетичний випадок |
| групи дублів `ticket_api` (серед батьківських) | **10** | `orderBy('id','asc')` перед `keyBy()` обовʼязковий |
| `route_api` з більш ніж одним `route_id` | **2** | дизамбігуація за `time_from` має сенс, але пріоритет низький |
| `WHERE ticket_api IN (...) AND parent_id IS NULL` без індексу | план через `tickets_parent_id_foreign`, ~50 640 рядків | індекс на `ticket_api` виправдано |

Також підтверджено емпірично: `array_keys()` на масиві з ключем `'11734120'`
повертає його типом **integer** — звідси необхідність `array_map('strval', ...)`.

Також не перенесено як несумісне: `gender` (немає колонки), seed-дані 3g
(їхні `station_id`/`city_id`), `book()` замість нашого
`bookOriginal(importTicket: true)`, `free_places`/`originalFromStation`.

## Повʼязані

- [[2026-07-30-bussystem-sync-hardening]] — сесія, у якій це реалізовано
- [[connection-search]] — пересадки v2 (звідки `parent_id`/`childTicket`)
- [[project-overview]]
