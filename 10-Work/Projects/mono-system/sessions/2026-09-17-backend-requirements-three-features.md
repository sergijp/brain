---
title: "Проект: mono-system — BACKEND-REQUIREMENTS: короткі посилання, сповіщення водія, доступ до пересадки"
date: 2026-09-17
tags: [mono-system, work, session, tickets, transfers, notifications]
category: session
project: mono-system
status: completed
aliases: []
pinecone_indexed: false
---

# BACKEND-REQUIREMENTS: три фічі під готовий фронт

## Мета сесії

Розібрати `BACKEND-REQUIREMENTS.md` — накопичувальний файл вимог до бекенду для
фронтенд-заготовок, які вже написані, — і реалізувати всі три розділи. Кожен
розділ власник уточнював поверх написаного, і в усіх трьох випадках уточнення
змінювало рішення.

## Виконано

### Фіча 3 — коротке посилання на квиток

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Таблиця й модель | `short_links` (поліморфна) + `ShortLink`: код 10 символів без `0/O/1/l/I`, переюз живого коду, ретраї на колізію |
| 2 | Публічна точка входу | `GET /t/{code}` — свіжий PDF inline, лічильник переходів, власна 404-сторінка |
| 3 | Кнопка в CRUD | Трейт `CopyTicketLinkOperation` у `TicketsCrudController`, відповідь рівно `{"link": ...}` |
| 4 | Термін дії | `Ticket::journeyArrival()` — кінець дня прибуття; для плеча подорожі — кінець **усієї** подорожі |

Рішення: [[10-Work/Projects/mono-system/decisions/2026-09-17-ticket-short-links]]

### Фіча 2 — сповіщення «водій позначив, що пасажир не з'явився»

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Таблиця й модель | `driver_status_notifications` + `DriverStatusNotification`: денормалізований знімок події |
| 2 | Запис і подія | `TicketObserver::updated()` — лише `not_showed_up` і лише від водія; payload події отримав блок `driver_notification` |
| 3 | Ендпоінти | `GET` список, `DELETE {id}`, `DELETE` усіх — під `can:dashboard-driver-status-notifications` |
| 4 | Фронт | Повна картка сповіщення, хрестик на елементі, «Очистити все»; `actor_type` прибрано |

### Фіча 1 — доступ до пересадки на станції

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Схема | `route_station.all_members` (default **true**) + pivot `route_station_transfer_member` |
| 2 | Ендпоінт і право | `POST .../transfer-hub-members` + `candidates`, право `routes-transfer-hub-members` |
| 3 | Видача | `GetRouteStationsField` віддає `transfer_hub_all_members`/`transfer_hub_members` |
| 4 | Пошук | `ConnectionSearchService::visibleHubExpression()` — закритий хаб виглядає як «не хаб» |
| 5 | Фронт | `TransferHubMembersPopup.vue`, усюди `agent` → `member`, пошук користувачів |

Рішення: [[10-Work/Projects/mono-system/decisions/2026-09-17-transfer-hub-access]]

## Важливі рішення

- [[10-Work/Projects/mono-system/decisions/2026-09-17-ticket-short-links]] —
  короткий код із терміном дії замість прямого посилання на PDF у `/storage`.
- [[10-Work/Projects/mono-system/decisions/2026-09-17-transfer-hub-access]] —
  поіменний список користувачів на станції; дефолт «бачать усі».

Дрібніші рішення:

| # | Питання | Рішення | Чому |
|---|---------|---------|------|
| 1 | Коли кидати `ChangeStatusTicket` | Перенесено з `updating` в `updated` | З `updating` подія летіла ДО запису: при невдалому `save()` диспетчер бачив статус, якого в базі немає |
| 2 | Як фронт розрізняє сповіщення водія | Блок `driver_notification` у payload | `actor_type` був би узагальненням, якого власник не хотів; порожнє поле = не показувати |
| 3 | Джерело списку користувачів для пересадки | Власний `candidates`, не `getUsers` | `getUsers` жорстко віддає агентів і вже використовується формою бронювання |
| 4 | Чи показувати клієнтів у дропдауні | Лише через пошук від 2 символів | Клієнти — майже вся таблиця `members`, повний список не поміститься |
| 5 | Прив'язка доступу | До `route_station`, без копії в `trip_station` | Доступ не розклад: має діяти одразу, а не після `syncWithRoute` |

## Проблеми й як вирішили

- **Bug (побічний, не чіпали):** будь-який `abort(404)` у web-групі віддає 500
  - **Причина:** `resources/views/errors/404.blade.php` успадковує `layouts.app` і
    `inc.components.page-title.index` — обох в'ю в репо давно немає
  - **Обхід:** `ShortLinkController` віддає власну сторінку. Глобально баг лишився —
    картка в Trello Mono, Backlog

- **Помилка типу:** `Ticket::pdf()` повертає `Symfony\...\Response`, а не
  `Illuminate\Http\Response` — перший запит до `/t/{code}` падав у 500

- **Тест PDF мовчки пропускався:** `config('snappy.pdf.binary')` дає `null` —
  ключ у `config/snappy.php` закоментований, пакет шукає `wkhtmltopdf` у PATH.
  Замінено на `ExecutableFinder`

- **Пастка в назвах:** таблиця маршрутних станцій — `route_station` (однина), а
  документ вимог усюди пише `route_stations`

- **Пастка при перевірці:** у маршруті може бути кілька хабів (у #14 їх дев'ять),
  тож `firstWhere('is_transfer_hub', true)` у ручній перевірці дивився не на ту
  станцію і створював враження, що код не працює

## Артефакти

Нове:

- `database/migrations/2026_09_17_140000_create_short_links_table.php`
- `database/migrations/2026_09_17_150000_create_driver_status_notifications_table.php`
- `database/migrations/2026_09_17_160000_add_transfer_hub_access_to_route_station.php`
- `database/migrations/2026_09_17_160100_add_transfer_hub_members_permission.php`
- `app/Entities/Tenant/ShortLink.php`, `app/Entities/Tenant/DriverStatusNotification.php`
- `app/Http/Controllers/ShortLinkController.php`
- `app/Http/Controllers/Api/DriverStatusNotificationsController.php`
- `app/Http/Controllers/Api/System/TransferHubMembersController.php`
- `app/Crud/Operations/CopyTicketLinkOperation.php`
- `resources/views/short-link/not-found.blade.php`
- `tests/Feature/Transfers/{ShortLinkTest,DriverStatusNotificationTest,TransferHubAccessTest}.php`

Змінене: `Ticket.php`, `RouteStation.php`, `TicketObserver.php`,
`ConnectionSearchService.php`, `GetRouteStationsField.php`, `TicketsCrudController.php`,
`routes/api.php`, `routes/web.php`, фронт (`TransferHubMembersPopup.vue`,
`DriverStatusNotifications.vue`, `RouteStation.vue`, `store/index.js`, `api-bridge.js`),
`lang/uk|en/crud.php`, `BACKEND-REQUIREMENTS.md`.

Перевірка:

```bash
php artisan test tests/Feature/          # 227 passed
npx vite build                           # проходить
```

Плюс ручні перевірки на стенді під реальними токенами (короткий лінк віддає PDF,
водій створює сповіщення, диспетчер ні, ендпоінти гейтяться правами). Тестові
Passport-токени відкликані, змінені рядки повернуті у вихідний стан.

## Лишилось у Backlog

- Баг глобального `errors/404.blade.php` (будь-який 404 у web-групі → 500)
- `Ticket::getPdfLink()` лишився вгадуваним — ним досі користуються листи

## Пов'язані нотатки

- [[10-Work/Projects/mono-system/decisions/2026-09-17-ticket-short-links]]
- [[10-Work/Projects/mono-system/decisions/2026-09-17-transfer-hub-access]]
- [[10-Work/Projects/mono-system/decisions/2026-07-29-one-order-per-journey]]
- [[10-Work/Projects/mono-system/project-overview]]
