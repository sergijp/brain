---
title: "Проект: onchul — імпорт старих квитків, трансфери, overbooking"
date: 2026-07-20
tags: [onchul, work, session]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Розібрати й довести до бойового імпорту скрипт завантаження старих квитків зі старої бази `vonchul` у поточний проєкт `onchul_new`, врахувавши коректне резолвування маршрутів (на основі станцій), пересадки (трансфери з фідерними маршрутами), виправлення live-бага в системі букінгу трансфертів, обробку overbooking і почистити SQL-дамп баз даних.

## Виконано

| Завдання | Результат |
|----------|-----------|
| Розібрано структуру скрипту імпорту | ✅ Знайдено `app/Console/Commands/ImportTicketsFromOld.php`, `app/Services/OldTicketsImportService.php`, `config/old-import.php`, конекшн `mysql_old` (vonchul) |
| Побудовано імпорт клієнтів | ✅ `clients:import-from-old` читає `old_clients` таблицю, матчить за нормалізованим телефоном (+380/380 варіанти), 24133 клієнтів імпортовано |
| Виявлено й виправлено резолв маршруту | ✅ Переписано на station-based (пара станцій) замість flights_id (структурно недостатній; ~29% квитків лягали в неправильні маршрути) |
| Додано поріг вибірки даних | ✅ `IMPORT_LOOKBACK_DAYS=2` (майбутні booking >= today-2дні) для обробки збірних рейсів |
| Розібрано архітектуру пересадок | ✅ Routes 5/6/7 мають transfer_id (станція Львів id21) → фідерні маршрути; live-букінг створює parent/child пари |
| Виявлено й виправлено live-баг в BookingService | ✅ Баг у `bookTransfer()` (~468-470): clamp нижньої межі брав pivot замість transfer_station_from_id → 4 регресійні тести |
| Реалізовано import parent/child пар | ✅ Parent (основний route, СТАРА ціна), child (фідерний route, price=0) в одній транзакції; всі 297 квитків 5/6/7 розподілені |
| Обробка overbooking конфліктів місткості | ✅ 42 квитки не влазили на 5 рейсах (17/18/19/24/25.07) → рішення: імпортуємо все, старе місце завжди, обмеження місткості не скіпуємо |
| Code review (reviewer) | ✅ 0 критичних; закрито 🟡 ambiguous-логи та route_station.active фільтри |
| Написано тести | ✅ 20 тестів `OldTicketsImportServiceTest.php` + 4 `BookTransferClampTest.php`; DatabaseTransactions (НЕ RefreshDatabase) |
| Бойовий імпорт клієнтів | ✅ `clients:import-from-old` — 0→24133 клієнтів, без конфліктів |
| Бойовий імпорт квитків | ✅ `tickets:import-from-old --import` — Found=Imported=1070, Skip=0; 1367 ticket-рядків (773 одиночних + 297 пар×2), 297 child, 609 з client_id, 1367 Orders |
| Почищено SQL-дамп базу | ✅ mysqldump --default-character-set=utf8mb4; видалено DEFINER з VIEW; 5 JSON-колонок корректні; activity_log присутній; size 19M |
| Діагностовано RangeError на /admin/trips/{id}/report | ✅ Root cause: getFreeSeatsCountByFromTo при overbooking = негативне число → фронт RangeError; фікс скасовано користувачем |

## Важливі рішення (ADR)

| Рішення | Чому | Альтернативи |
|---------|------|--------------|
| **Station-based резолв маршруту** | Стара конфіг `flights=>[1=>4,2=>3]` структурно недостатня — під одним flights_id змішані квитки на різні напрямки. Дедукація через пару станцій (from.order < to.order) дає 99.8% точність. | flights_id з підрахунком дефолту через flightsMap при неоднозначності |
| **Поріг вибірки today-2дні** | Збірні рейси мають розрив дати рейсу й посадки. Константа `IMPORT_LOOKBACK_DAYS=2` фільтрує майбутні booking. | Без поріга або більший проміжок — ризик конфліктів з попередніми імпортами |
| **Price transfer на parent, не на child** | Переносимо стару ціну повністю на parent (основний route). Child (фідерний) має price=0 БЕЗ перерахунку за live-тарифом — щоб не задвоювати виручку. | Поділити ціну 50/50 або перерахувати за новим тарифом — обидва призведуть до розбіжностей з фінансами |
| **Overbooking: усі квитки, старе місце** | 42 квитки не влазили через зміну автобусу (55-57→49 місць) на проблемних рейсах. Рішення: дублі місць прийнятні, обмеження місткості не скіпуємо — користувач переглянути вручну. | Скіпувати overbooking квитки або переназначити місця — втрата даних |
| **Автобуси не чіпати** | Route 3-7 мають статичний bus_id (49-місний MAN LionsCoach). Старі системи вручну перепризначали для рейсів. Новий імпорт не зачіпає bus_id. | Спроба автоматично перепризначити або замінити автобуси — невідомі критерії старої логіки, ризик невідповідності |
| **Clamp-баг в bookTransfer — окремий трек** | Баг у `BookingService::bookTransfer()` (clamp нижньої межі) — ДОПОВНЮВАННЯ live-системи, не частина імпорту. Виправлено окремо з 4 регресійними тестами. | Змішати фіксування з імпортом — ускладнювало б діагностику й тестування |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| **Route mismapping (~29% квитків)** | Переписано резолв на station-based: маршрут = активний route, що містить обидві станції у порядку from.order<to.order; flightsMap дефолт при неоднозначності. Точність 99.8%. |
| **Пересадки 5/6/7 не імпортувалися** | Реалізовано parent/child букінги в одній транзакції; parent на основному route, child на фідерному (transfer маршруті), parent_id спільна; 297 пар розподілені. |
| **Live-баг: clamp у bookTransfer() не створював child** | Виявлено: clamp нижньої межі брав `pivot` замість `transfer_station_from_id`. Виправлено симетризацією clamp. Написано 4 регресійні тести (BookTransferClampTest). |
| **Overbooking конфлікти місткості** | 42 квитки на 5 рейсах (17/18/19/24/25.07). Рішення: рядки імпортуються, місце = старе завжди, обмеження місткості не скіпуються. Користувач переглядає вручну — сказано про дублі місць. |
| **SQL-дамп hex-кодування JSON (#3144/#3140/#1227)** | Переекспорт через `mysqldump --default-character-set=utf8mb4` у корінь проєкту (`onchul_new_2026-07-20.sql`); видалено DEFINER з VIEW; 5 JSON-колонок чисті; activity_log присутній; size 19M (чистий UTF-8). Усунено всі 3 помилки. |
| **RangeError на /admin/trips/{id}/report** | Діагностовано: `getFreeSeatsCountByFromта` при overbooking = негативна кількість вільних місць → фронт `v-for="i in freePlaces"` → RangeError. Root cause: TripReportManager.vue:98 + TripReportResource.php:30. Почато фікс (frontend Math.max(0), backend clamp), але **користувач СКАСУВАВ** — фікс не застосовано. Остався латентний баг. |

## Артефакти

### Змінені файли (в origin/dev, не локально 2026-07-20 EOD)
- **app/Services/OldTicketsImportService.php** — station-based резолв, lookback-фільтр, parent/child persist, overbooking, ambiguous-лог, active-фільтр
- **app/Console/Commands/ImportTicketsFromOld.php** — підтримка `--import` флага
- **app/Services/BookingService.php** — фікс clamp у `bookTransfer()` (~468-470)
- **config/old-import.php** — коментар про станції й перегляд
- **tests/Feature/Import/OldTicketsImportServiceTest.php** — 20 тестів (резолв, перегляд, lookback, дефолт, parent/child, quantity)
- **tests/Feature/Booking/BookTransferClampTest.php** — 4 регресійні тести (clamp на різних маршрутах)

### Команди
- `php artisan clients:import-from-old` — читає `old_clients`, матчить за телефоном, пише 24133 рядків
- `php artisan tickets:import-from-old [--import]` — preview або бойовий імпорт 1070 квитків

### База даних
- **onchul_new_2026-07-20.sql** — експорт через mysqldump, 19M, UTF-8, JSON чисто, no DEFINER, activity_log присутній
- **onchul_new_2026-07-20.sql.bak** — бекап до прибирання DEFINER

### Результати імпорту (1 раз бойовий)
```
Clients: 0 → 24133 (import-from-old)
Tickets: Found=1070, Imported=1070, Skip=0
Rows: 1367 ticket (773 solo + 297×2 pairs = 594 parent/child)
Orders: 1367 автоматично створено
Clients з id: 609/1070 (57%)
Routes: 1 (route3), 2 (route3), 3 (route4), 4 (route3), 5 (94 parents), 
        6 (115 parents), 7 (88 parents), інші мінорні
```

### Auto-memory оновлено
- project_old_tickets_import.md — що імпортовано, дата 2026-07-20, 1070 квитків
- bug_transfer_feeder_clamp.md — clamp-баг в bookTransfer(), виправлено з тестами

## Пов'язані нотатки

- [[project-transfer-3g-alignment]] — архітектура трансфертів (parent/child моделі, фідерні маршрути)
- [[project_old_tickets_import]] — auto-memory про імпорт (є посилання на цю сесію в vault)
- [[2026-07-03-import-tickets-from-vonchul]] — попередня сесія з підготовкою імпорту (клієнти, тест-рани)
- Баг #clamp-transfer-feeder — live-система, 4 регресійні тести, окремий трек
- Латентний баг RangeError на /admin/trips/{id}/report — залишився (скасовано користувачем)
