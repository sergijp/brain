---
title: "AppApi — архітектура"
date: 2026-08-24
tags: [mono-system, architecture, app-api, access-control]
category: docs
project: mono-system
status: active
aliases: ["mono-system-app-api"]
pinecone_indexed: false
last_verified: 2026-08-24
---

# AppApi — API мобільного застосунку пасажира

## Контекст

`/api/v1/app/...` — модуль для мобільного застосунку пасажира, заведений
2026-08-21 як копія `SiteApi` і доведений до потреб застосунку 2026-08-24.
Код: `app/Services/Api/v1/AppApi/`, детальний журнал змін — `CHANGES_APP_API.md`
у корені репозиторію.

**Головне, що треба знати, щоб не зламати:** застосунок ходить в API **під
токеном самого клієнта**, а не під технічним акаунтом. Це відрізняє його від
усіх інших споживачів API і є причиною всіх особливостей нижче.

## Модель доступу — хто під ким ходить

| Споживач | Під чиїм токеном | Права звідки |
|---|---|---|
| Сайт (`SiteApi`) | технічний акаунт `MONOBUS_LOGIN`, роль `Api` | 7 дозволів `api-*` у ролі |
| Сайт, кабінет | клієнт | `profile/*` не мають `can:` |
| Партнери (`GlobalApi`) | агентський акаунт | роль `Api`/`Agent` |
| **Застосунок (`AppApi`)** | **клієнт** | whitelist у `Gate::before` |

`mono-site/app/Services/ApiService.php` тримає обидва токени: `getToken()` —
системний, `getTokenClient()` — клієнтський. Застосунок так не може: технічний
пароль у білді не сховаєш.

## Ключові контракти

1. **Клієнт не має ролі.** `registration` ставить лише колонку `type='client'`,
   `assignRole()` не викликається — ролі `client` у базі немає взагалі
   (266 232 клієнти, 0 ролей). Доступ дають не ролі, а whitelist
   `AuthServiceProvider::CLIENT_API_ABILITIES` у `Gate::before`.

2. **Власність квитка асиметрична.** `orders.member_id` — продавець,
   `tickets.member_id` — пасажир. Ордерів у клієнтів 0 зі 105 840; пасажир і
   покупець розходяться у 124 982 випадках зі 124 982.

3. **Видимість квитка** — див. ADR:
   `orders.member_id = me` АБО (`tickets.member_id = me` І ордер оформлений не
   клієнтом). Живе в `TicketScope::applyForClient()`.

4. **Власність замовлення перевіряється через квитки.** У `TicketsController`
   є `visibleOrder(column, value)` — шукає ордер через `whereHas('tickets')`,
   тобто спирається на `TicketScope`. Окремої умови по `orders.member_id` у
   контролерах не треба і не має бути.

5. **HTTP-методи явні.** GET — читання, POST — мутації. `any` у модулі
   заборонений.

6. **Формат запитів, який неочевидний:**
   - `POST /buy` — `places` передається як **base64(JSON)** списку пасажирів
     (розбирає `CreateOrderRequest::validationData()`)
   - `GET /trip`, `GET /route` — `id` береться з поля `tripId` у видачі
     `GET /trips`, це base64(JSON) з `trip_id`/`from_id`/`to_id`

## Callsite-и

| Файл | Метод / місце | Призначення |
|------|---------------|-------------|
| `app/Providers/AuthServiceProvider.php` | `CLIENT_API_ABILITIES`, `Gate::before` | доступ клієнта до 7 `api-*` без ролі |
| `app/Scopes/TicketScope.php` | `applyForClient()` | правило видимості квитків для `type=client` |
| `app/Scopes/TicketScope.php` | `apply()`, гілка для решти | `order.member_id = me` — поведінка агентів, не чіпати |
| `app/Services/Api/v1/AppApi/AppApiProvider.php` | `routes()` | 35 роутів, явні GET/POST |
| `.../AppApi/Http/Controllers/TicketsController.php` | `visibleOrder()` | перевірка власності ордера через квитки |
| `.../AppApi/Http/Controllers/OrderController.php` | `getOrderWithTickets()` | `cancel`/`sell` — строго `orders.member_id = me` |
| `.../AppApi/Http/Controllers/OrderController.php` | `getFormData()` | `new LiqPay(...)` у тому ж namespace, без `use` |
| `app/Services/BookingService.php` | `book()` L139, `bookJourney()` L209 | `$order->member()->associate($orderUser)` — звідки береться продавець |
| `app/Entities/Tenant/Order.php` | `createTickets()` | `$ticketEntity->client()->associate(...)` — звідки береться пасажир |

## Матриця видимості

| Хто оформив ордер | Хто пасажир | Покупець бачить | Пасажир бачить |
|---|---|---|---|
| каса / агент / сайт | клієнт A | — (не клієнт) | так |
| клієнт A (застосунок) | клієнт A | так | так (він же) |
| клієнт A (застосунок) | клієнт B | так | **ні** |
| агент | агент-же | так (звичайний `TicketScope`) | — |

## Gotchas

- **`LiqPay.php` не має роуту, але видаляти його не можна** — `OrderController`
  створює `new LiqPay(...)` у тому самому namespace, без `use`. Аудит мертвого
  коду по імпортах його не бачить. Один раз уже видалили й зламали
  `get-form-data`.
- **`TicketScope` глобальний** — будь-яка зміна зачіпає адмінку, сайт і
  партнерів. Гілка для клієнта відокремлена саме тому. Перед зміною фіксувати
  baseline: кількість видимих квитків для агента `Api` (66 105), адміна і
  водія (126 109).
- **`profile/*` знімає скоуп** через `withoutGlobalScope(TicketScope::class)` —
  тому саме там колись і виник розрив зі списком.
- **Номер квитка передбачуваний:** `APP_TICKET_KEY + ddmmyyHHii + trip_id +
  place`. Покладатися на його невгадуваність не можна, ізоляцію тримає скоуп.
- **`Gate::before` викликає `hasRole('admin')`, а роль у базі — `Admin`.**
  spatie порівнює регістрозалежно, тож bypass не працює. Нешкідливо лише тому,
  що роль `Admin` має всі 269 дозволів напряму.
- **Невідповідний метод під `/api/*` віддає HTML SPA з кодом 200**, а не JSON
  405. Fallback перехоплює запит раніше.
- **`LiqPay.php` має `use App\Http\Controllers\InvalidArgumentException`** —
  такого класу немає, тож будь-який виняток LiqPay стає фаталом. Стосується всіх
  чотирьох копій файлу.

## Пов'язані

- [[INDEX]]
- [[../decisions/2026-08-24-client-ticket-visibility]] — ADR про правило видимості
- [[bussystem-ticket-sync]] — там теж `TicketScope` як пастка
- Журнал змін модуля: `CHANGES_APP_API.md` у корені репозиторію
- Tier-2 pointer: `~/.claude/projects/-Users-serhiin-Data-Source-mono-system/memory/architecture_app_api.md`
