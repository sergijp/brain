---
title: "Проект: mono-system — верифікація 3 планів + глибокий аналіз Transfers v2"
date: 2026-07-20
tags: [mono-system, work, session]
category: session
project: mono-system
status: completed
aliases: []
pinecone_indexed: false
---

# Мета сесії

1. Знайти й перевірити наявні плани в репо (3 файли від 2026-06-11).
2. Верифікувати кожен план проти поточного коду (після планів було 4 коміти) і внести правки.
3. Глибокий аналіз TRANSFERS-V2-PLAN.md: чи покриті сценарії з еталонних прикладів (`~/Downloads/routes-table-original.html`, `interactive-map-original.html`), посадка/повернення/скасування, швидкість пошуку + аналіз живої БД.

# Виконано

- **3 паралельні агенти-верифікатори** перевірили всі твердження планів проти коду → всі 3 плани оновлені (позначки ⚠️, дата ревізії 2026-07-20).
- `REFACTOR-BOOKING-TRIPS-PLAN.md`: виправлено рішення №2 (once() відсутній у Laravel 10.48 → explicit pre-fetch + параметр), уточнено validateOrderData (читає relation tickets, НЕ view), blast radius 14/10 файлів (+PrivatBank v1).
- `REFACTOR-PROJECT-WIDE-PLAN.md`: п. 5.1 актуалізовано (InfobusService переписано на Guzzle 2026-06-17, але timeout/retry так і немає; креди вже в env), п. 3.1 переписано (мемоізація на інстансі User замість once()), нова знахідка ActivitiesController:19 (інстанціювання довільного класу з request), test22 розширюється замість видалення.
- `TRANSFERS-V2-PLAN.md` — найбільші доповнення:
  - еталонні сценарії (15 маршрутів = 8 фізичних + 7 комбінованих, хаби Чернівці/Хмельницький/Умань) замаплені на тест-кейси, включно з «довозкою» (Ізмаїл) і нічним layover;
  - розділ «Нюанси фінального проходу» (8 пунктів) + «Аналіз реальних даних» (таблиця замірів БД);
  - Фаза 6 розширена: createTrip не копіює також boarding/unboarding/bus_id.

# Важливі рішення (ADR)

| Рішення | Обґрунтування |
|---|---|
| once() → explicit pre-fetch + опційний параметр | once() — helper Laravel 11; проєкт на 10.48; статична мемоізація небезпечна через tenant-switching у воркерах |
| TripScope-мемоізація → метод на інстансі User | інстанс живе один request; жодного протікання між джобами |
| transfers_max_layover 720 → **1440 хв** | приклад «Гдиня - Львів 13:00 - Херсон» = layover 14–18 год, 12 год його відрізає |
| Нова Фаза 0 для Transfers v2 — гігієна даних | 75% trip_station — мертві рядки trip_id=NULL (FK ON DELETE SET NULL) → чистка + FK CASCADE |
| Кеш пошуку стиковок — лише для гостей | TripScope не діє на Query Builder; user-обмеження застосовувати на збагаченні top-N |

# Проблеми й як вирішили

- **once() fatal error була б у рантаймі** — знайдено верифікатором до імплементації.
- **BFS обходить TripScope** (visibility агентів) → routes.is_visible у джойн + user-зріз на top-N.
- **journeyId підробний** (base64) → обов'язкова перевалідація стиковки в bookJourney.
- **Ініціація оплати** — прогалина плану: сума платежу з одного order; для journey треба чекаут по сумі всіх orders journey_uuid (LiqPay.php + v1 SiteApi LiqPay).
- **Часові пояси** — відкрите питання: якщо адміни вводять місцевий час станцій, layover міжнародних стиковок має похибку ±1–2 год; потрібна конвенція/TZ-мапа.

# Аналіз БД (dev, 2026-07-20)

- mono-system: 23 945 trips (948 майбутніх, ~18/день), trip_station 1.6M рядків, з них **1.19M (75%) сміття trip_id=NULL**; робочий набір BFS майбутніх рейсів ~24k рядків; avg 17 станцій/рейс.
- boarding/unboarding = 1 на **100%** рядків (обмеження не працюють — узгоджено з багом createTrip).
- **Дрейф схеми**: dev-БД має індекси trips.date/active, trip_station.station_id/order/... — їх НЕМАЄ в міграціях (додані вручну) → на проді може не бути.
- Legacy transfer-парувань: route_station — 1, trip_station — 200 → backfill майже нічого не дасть, хаби розмічати вручну.
- Вердикт швидкості: BFS на цих обсягах з denorm departure_at + індексами = одиниці-десятки мс; precomputed-таблиця не знадобиться.

# Артефакти

- Оновлені: `REFACTOR-PROJECT-WIDE-PLAN.md`, `REFACTOR-BOOKING-TRIPS-PLAN.md`, `TRANSFERS-V2-PLAN.md` (у корені репо, не закомічено)
- Еталонні приклади: `~/Downloads/routes-table-original.html`, `~/Downloads/interactive-map-original.html` (у репо відсутні)
- БД-запити виконувались через PHP PDO (mysql-клієнта на машині немає): `php -r '... new PDO("mysql:host=127.0.0.1...")'`

# Пов'язані нотатки

- [[2026-06-15-busfor-tripcontroller-explode-n1]]
- SECURITY-AUDIT.md (репо) — перетини з планами
