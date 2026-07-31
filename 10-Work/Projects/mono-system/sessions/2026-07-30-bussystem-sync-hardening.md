---
title: "Проект: mono-system — доведення синку Bussystem до робочого стану за зразком 3g"
date: 2026-07-30
tags: [mono-system, bussystem, infobus, sync, work, session]
category: session
project: mono-system
status: completed
aliases: ["Bussystem sync hardening"]
pinecone_indexed: false
---

## Мета сесії

Розібрати `SyncBussystemTicketJob` у mono-system, порівняти з робочою реалізацією
в проєкті `3g` (той самий API `get_tickets`, інші рейси/станції), і доповнити
mono-версію тим, чого їй бракує — не переносячи те, що специфічне для 3g.

## Виконано

### Аналіз
- Прочитано обидві реалізації повністю. Масштаб розриву: джоба 85 vs 327 рядків,
  сервіс 202 vs 1660, друга джоба (звірка далеких вікон) у mono відсутня взагалі,
  міграцій Bussystem 1 vs 9.
- Складено список 14 конкретних дефектів mono-версії + список того, що з 3g
  **не підходить** (їхні дані/схема/контракти).

### Реалізовано (етапи 1–4 плану)

| # | Що | Файл |
|---|---|---|
| 1 | HTTP-таймаут 120 с + connect_timeout (був дефолт Laravel 30 с при заявлених API 120 с) | `BussystemDispatcherService::getTickets()` |
| 2 | Обробка 403 (`ip_not_whitelisted`) і не-2xx окремо від `invalid_response` | там само |
| 3 | `error_type`: credentials / params / infrastructure / generic | там само |
| 4 | Маскування логіна/пароля в логах і полі `raw` | `maskCredentials()` |
| 5 | Fallback для одиночного JSON-обʼєкта без ключа `item` (квиток мовчки зникав) | там само |
| 6 | Індекси на `tickets.ticket_api` і `error_tickets.ticket_api` | міграція `2026_07_30_100001` |
| 7 | Пошук існуючих: `withoutGlobalScope(TicketScope)` + `whereNull('parent_id')` + `array_map('strval')` + `orderBy('id','asc')` | `SyncBussystemTicketJob` |
| 8 | `try/catch` на кожен квиток + лічильники + підсумковий лог | там само |
| 9 | Статус `reserve` → створення як PREBOOKED | `BussystemTicketStatusResolver` |
| 10 | `buy` + локальний PREBOOKED → SOLD | там само |
| 11 | Каскад скасування на `childTicket` (друге плече пересадки) | там само |
| 12 | `normalizeTimedate()` — захист від `0000-00-00` у `cancel_timedate` | там само |
| 13 | `freePlace` для `ticket.seat === '***'` | `mapToLegacyTicket()` + `CreateTicketJob` |
| 14 | Парсер ціни через regex замість списку 5 валют | `CreateTicketJob` |
| 15 | Guard на порожню назву маршруту + екранування LIKE | `CreateTicketJob`, dry-run роут |
| 16 | Telegram-алерти з рейт-лімітом 60 хв на тип помилки | `BussystemFailureReporter` |
| 17 | Друга джоба — звірка далеких вікон ланцюжком | `SyncBussystemTicketStatusCheckJob` |
| 18 | Dry-run роут переведено на спільний резолвер (мав власну копію логіки, що розʼїхалась) | `routes/api.php` |

### Нові файли
- `app/Services/Bussystem/BussystemTicketStatusResolver.php`
- `app/Services/Bussystem/BussystemTicketWindowFetcher.php`
- `app/Services/Bussystem/BussystemFailureReporter.php`
- `app/Jobs/Trips/SyncBussystemTicketStatusCheckJob.php`
- `database/migrations/2026_07_30_100001_add_index_to_ticket_api_columns.php`

## Важливі рішення (ADR)

| Рішення | Альтернатива | Чому так |
|---|---|---|
| Окреме queue-зʼєднання `redis-long` (retry_after 300) для черги `infobussync` | підняти `retry_after` у `redis` з 60 до 300 | `retry_after` спільний для ВСІХ джоб на зʼєднанні (пошта, звіти). 120-секундний HTTP-виклик при retry_after=60 змушував воркер брати джобу вдруге паралельно. Окреме зʼєднання ізолює зміну; ключі Redis ті самі (той самий driver/connection), змінюється лише retry_after. |
| Не переносити з 3g: `gender`, seed-міграції з їхніми station_id/city_id, `findManualDuplicateTicket`, `book()`/`free_places`/`originalFromStation` | скопіювати цілком | Немає колонки `gender`; їхні числові ID не відповідають нашим станціям; ручні дублікати — їхня історія з member 29; у нас `bookOriginal(importTicket: true)` і `getFreeSeatsByFromTo()`. |
| `lang` лишено `'ua'` (не переведено на `'en'`, як у 3g) | одразу `'en'` | Висновок 3g («для ua/uk API віддає російські назви») зроблено на їхньому payload. Винесено в env — перевірити через `GET /api/test-bussystem-raw` перед увімкненням. |
| Запитане місце зайняте у нас → підставляємо найменше вільне з warning, а не відмова | кидати в `error_tickets` | Наша карта місць легально розходиться з bussystem (диспетчер пересаджує вручну); відмова валила б кожен квиток з колізією номера. |
| Числові рівні резолвінгу станцій (`station_ids`, `point_cities`, `route_api_id`) НЕ реалізовано | перенести одразу | Потрібні лише якщо city-level не вистачає — залежить від наших даних. Відкладено до перевірки (див. «Лишилось»). |

## Проблеми й як вирішили

- **Порожня назва маршруту → `LIKE '%%'`** матчив усі рядки `route_api_route`,
  `->first()` чіпляв квиток до довільного чужого маршруту. Додано guard + `ESCAPE`.
- **`explode(" ", carrier)` без limit** → `Undefined array key 1` при відсутньому
  прізвищі. → `explode(..., 2)` + `?? null`.
- **`Arr::first()` у фільтрі вільних місць** — замикання ігнорувало аргументи;
  замінено на пряме порівняння рядками (int vs numeric string).
- **Dry-run роут мав власну копію класифікації** і вже не знав ні про `reserve`,
  ні про PREBOOKED→SOLD, ні про каскад — переведено на спільний резолвер з
  `apply: false`.

## Артефакти

- Змінено 10 файлів, додано 5. ~670 рядків.
- Перевірено: `php -l` по всіх файлах, автозавантаження нових класів,
  `php artisan schedule:list`, `php artisan migrate --pretend`.
- **Міграція НЕ застосована** — виконати `php artisan migrate`.
- Після деплою: `php artisan config:clear`, `php artisan horizon:terminate`
  (зміна зʼєднання супервізора).

## Верифікація

Прогін після реалізації (26 функціональних перевірок через `Http::fake` +
перевірки на реальній БД):

- парсинг відповіді: одиночний JSON-обʼєкт без `item`, список під `item`, XML,
  `no_found`, 403, HTTP 500, `dealer_no_activ`, `max_31days`, маскування
  креденшелів — усе ок;
- `mapToLegacyTicket`: `seat='***'` → `freePlace=true`, `'14'` → `false`;
- `WindowFetcher`: `ticket_id='0'` не втрачається, item без `ticket_id`
  рахується, дедуп між вікнами, 403 обриває наступні вікна;
- `normalizeTimedate`: `0000-00-00 00:00:00` → null;
- резолвер: усі гілки без локального квитка;
- **каскад перевірено на реальній парі #485/#486** — `child_would_cancel=true`,
  dry-run (`apply: false`) нічого не змінив.

**Знайдений і виправлений дефект власної правки:** `'freePlace'` у масиві
`$ticket` брався з `$this->data['freePlace']`, а логіка підбору місця — з
ширшого `$requestedPlaceIsFree` (що враховує ще й `place === '***'`). Для даних
з `'***'` без явного ключа це давало «взяли будь-яке вільне, але закріпили як
власне» — рівно та дірка, яку правка закривала. Обчислення перенесено вище
масиву, обидва місця тепер читають одне значення.

**Дефект тест-скрипта (не коду):** `Http::fake()` у Laravel **зливає** stub-и, а
`Http::clearResolvedInstances()` не прибирає синглтон `Http\Client\Factory` з
контейнера — перші 10 перевірок хибно падали, поки не додано
`app()->forgetInstance(Factory::class)`.

## Заміряно по БД (локальна копія, 101 902 квитки)

| Метрика | Значення |
|---|---|
| дочірні квитки пересадки (`parent_id` не null) | 113 |
| групи дублів `ticket_api` | 10 |
| `route_api` з >1 `route_id` | 2 |
| рядків у плані без індексу на `ticket_api` | ~50 640 |

Тобто каскад і `orderBy('id','asc')` — не теорія, а реальні випадки в цій базі.

## Сценарний прогін джоб (2026-07-31)

Окрім 26 юніт-перевірок — 4 набори (усі зелені): юніт, LIKE-екранування,
сценарії джоб, сценарії `CreateTicketJob`. Джоби прогнані повністю
(`handle()`) на справжній БД з підробленим HTTP і `Queue::fake()`; усе, що
писало, — у транзакції з `rollBack()`.

Перевірено: лічильники сходяться з `processed`; `reserve` → `target_status =
prebooked` і диспатч у чергу `infobussync`; `403` → `RuntimeException` (ретрай
Horizon), `dealer_no_activ`/`max_31days` → без винятку; скасування реального
локального квитка з `canceled_at`; ланцюжок вікон звірки (диспатч наступного,
зупинка на останньому, тихий вихід за межами); `WithoutOverlapping`
(`releaseAfter=null`, `expiresAfter=180`); `CreateTicketJob` на порожньому/
шаблонному `route`, без прізвища, з кривим `interval` — без винятків.

**Головна знахідка — блокер, не помічений раніше:** `bussystem_city_aliases`
порожня (0 рядків), сідер не входить у `DatabaseSeeder`. Синк, увімкнений у
такому стані, відправив би **100 %** квитків у `error_tickets`. Заміряно:
0 із 16 міст резолвиться до сідера, 13 із 16 — після (решта — Utena/Gdynia,
яких немає в наших `cities`). Задокументовано в `Kernel.php`, у докблоці
`resolveRouteStation()` і в [[bussystem-ticket-sync]].

**Два «провали», що виявились не дефектами:**
- `missing_ticket_id` рахується по вікнах і не дедуплікується (нічим —
  у таких item якраз немає id), тож один item у двох вікнах дає 2. Уточнено
  докблок `BussystemTicketWindowFetcher::fetch()`.
- `error_tickets.price` — `int(11)` (при `tickets.price` = `double(8,2)`), тож
  `52.65` у записі про ПОМИЛКУ округлюється до `53`. Схема, що існувала й до
  змін; на справжніх квитках ціна точна.

## Продовження 2026-07-31 (після вмикання на проді)

**Інцидент.** Ввімкнули джоби — замість 6 сьогоднішніх продажів заїхали сотні
квитків. Причина: `INFOBUS_SYNC_DAYS_AHEAD=29` вмикав прохід `departure`, який
тягне ВСІ квитки на рейси найближчих 30 днів незалежно від дати продажу, і кожен
відсутній локально створює. На базі, де синк давно не працював, це імпорт усього
бекклогу. Дефолт виправлено на `0`; постійну звірку майбутнього робить
`SyncBussystemTicketStatusCheckJob`, яка нічого не створює (`canCreate: false`).
Квитки користувач почистив вручну.

**Безпека.** Дебаг-роути `/api/test-bussystem-*` виявились БЕЗ автентифікації
(група `api` — це лише Sanctum-stateful + throttle + bindings), а `raw` віддає
вузол `passenger`: імена, прізвища, телефони. Додано гейт: у `local` вільно, на
інших оточеннях потрібен `?token=<INFOBUS_DEBUG_TOKEN>`; якщо змінна не задана —
404 (щоб «забули поставити токен» не означало «відкрито всім»).

**Dry-run у роуті.** `/api/test-bussystem-sync` переписано: показує поквитково,
що затягнеться, що сяде в рейс (з id рейсу і долею місця), що піде в
`error_tickets` і з якої причини. Параметри: `date`, `days_ahead`,
`only_departure`, `limit`, `all`. Саме `days_ahead` дозволяє подивитись наперед,
що заїде при вмиканні `departure`, не вмикаючи його.

**Дедуп по пасажиру** — див. [[bussystem-ticket-sync]], розділ «Дедуп перед
бронюванням». Ключове уточнення від замовника: менеджер, заводячи квиток вручну,
вказує агента — тому пошук обмежено `order.member_id = config('infobus.member_id')`.
Дані підтвердили критичність: ручні квитки на майбутніх рейсах лежать під
`site`/`Busfor API`/`KLR bus`/`ElinTrans`, і без фільтра ми прив'язали б
`ticket_api` до чужого каналу продажу.

**Команда `error-tickets:clear`** — `--before`, `--ticket-api`, `--force`,
пачками, з підтвердженням (`ConfirmableTrait`). `ErrorTicket` без SoftDeletes,
видалення остаточне.

**Діагностика двох невдалих квитків (не відтворюються локально):**
- «рейс не знайдено на цю дату» (Kharkiv - Praha, 04.08): локально маршрут
  однозначний, станції резолвляться, рейси на всі дати є, `getTrips` повертає
  рейс. Отже на проді бракує самого рейсу — питання до
  `CronGenerateTripsForRouteJob`.
- «немає вільних місць» (trip 84017): локально 34 вільних із 34, заброньовано 0.
  На проді 0 вільних → місця вже зайняті, найімовірніше ручними двійниками. Новий
  дедуп цю причину і закриває.
- Побічно: на trip 84017 `closed_places` = 47 при 34 місцях у автобусі — схоже на
  залишок від попереднього автобуса, окремий баг у даних.

## Лишилось (свідомо не робилось)

1. `resolveRouteStation()` досі робить `->first()` при кількох кандидатах —
   недетерміновано (у 3g це `pickDeterministic()` по найменшому `route_station.order`).
2. Дизамбігуація маршруту за `time_from` — стосується всього 2 рядків
   `route_api_route`, пріоритет низький.
3. Підтвердити `config('infobus.lang')` на реальному payload через
   `GET /api/test-bussystem-raw`.
4. Обидві джоби лишаються **закоментованими** в `Kernel.php` — блокер той самий,
   що й був: whitelist серверного IP на боці bussystem.

## Повʼязані нотатки

- [[3g]] — референсна реалізація тієї самої інтеграції
- [[mono-system]]
