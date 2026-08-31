---
title: "Проект: mono-system — AppApi: доступ клієнта, видимість квитків, HTTP-методи, чистка"
date: 2026-08-24
tags: [mono-system, work, session, app-api, access-control]
category: session
project: mono-system
status: completed
aliases: []
pinecone_indexed: false
---

# AppApi: доступ клієнта, видимість квитків, HTTP-методи, чистка

## Мета сесії

Розібрати новий модуль `AppApi` (`/api/v1/app/...`), заведений 2026-08-21 як
копія `SiteApi`, і довести його до робочого стану для мобільного застосунку:

1. проаналізувати, що в модулі є;
2. визначити, які ендпоінти застосунку не потрібні;
3. полагодити баг — клієнт не має ролі, тож API не віддає йому нічого;
4. замінити `any` на явні HTTP-методи.

## Виконано

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Аналіз модуля | 49 файлів, 47 роутів — точна копія `SiteApi`. Знайдено мертвий код і роути, що ведуть на неіснуючі методи |
| 2 | Доступ клієнта до `api-*` | Whitelist `CLIENT_API_ABILITIES` у `Gate::before`, без міграції на 266k записів |
| 3 | Видимість квитків | Гілка `TicketScope::applyForClient()` за правилом з [[10-Work/Projects/mono-system/decisions/2026-08-24-client-ticket-visibility]] |
| 4 | Відповідь на чужий/неіснуючий ордер | Хелпер `visibleOrder()` у `TicketsController`, 500 і порожні 200 замінені на 422 `E_BUYID` |
| 5 | `any` → GET/POST | 34 роути переоголошені явно; `GET /buyinit` більше не створює замовлення |
| 6 | Чистка модуля | 49 → 33 файли, 50 → 35 роутів: 15 роутів, 16 файлів, 16 методів, 33 use-імпорти |
| 7 | Прогін усіх роутів | Усі 35 резолвляться і відповідають; наскрізний сценарій купівлі пройдено |
| 8 | Документація | `CHANGES_APP_API.md` переписаний під актуальний стан, звірений із кодом скриптом |

## Важливі рішення

- [[10-Work/Projects/mono-system/decisions/2026-08-24-client-ticket-visibility]] —
  видимість квитків клієнта: покупець плюс пасажир на не-клієнтських ордерах.

Дрібніші рішення:

| # | Питання | Рішення | Чому |
|---|---------|---------|------|
| 1 | Як дати клієнту доступ до `api-*` | Whitelist у `Gate::before` замість ролі `client` з backfill | Без міграції на 266k записів, миттєво працює для всіх наявних клієнтів |
| 2 | Який сценарій повернення лишити | `get-return-price` + `return-ticket` | `return` — касовий (вибір `percent` вручну), а `return-ticket` сам рахує правило й диспатчить `ReturnTicketJob` на повернення грошей |
| 3 | Який експорт PDF лишити | `exportPDF` | Віддає сирий PDF; `exportPDFSite` — той самий вміст у base64 всередині JSON |
| 4 | Чи чіпати `SiteApi`/`GlobalApi` | Ні | Там `orders.member_id` — технічний і партнерський акаунти; фільтр по власнику зламав би сайт і партнерів |

## Проблеми й як вирішили

- **Bug:** клієнт отримував 403 на всі ендпоінти, крім `profile/*`
  - **Причина:** `registration` ставить лише `type='client'`, ролі не призначає; ролі `client` у базі немає взагалі. 28 роутів під `can:api-*`, а ці дозволи має тільки роль `Api` — технічний акаунт сайту
  - **Фікс:** whitelist із 7 abilities у `Gate::before` для `type = client`

- **Bug:** квиток видно в `profile/*`, але жодна операція з ним не працює
  - **Причина:** `TicketScope` фільтрує за `order.member_id = me`, а клієнт — не власник ордера (`orders.member_id` = продавець). `profile/*` знімає скоуп, решта ні
  - **Фікс:** окрема гілка скоупа для клієнта. Доказ до фіксу: клієнт 277360 бачив квиток `MB0508260830843013` в архіві, а `ticket/status` по ньому казав «не знайдено»

- **Хибна гіпотеза:** спершу я описав 9 ендпоінтів як відкритий витік чужих даних
  - **Насправді:** HTTP-проби показали, що `TicketScope` їх закриває — витоку немає. Проблема була протилежна: скоуп надто вузький
  - **Урок:** перевіряти запитом, а не читанням коду, перш ніж називати щось дірою

- **Bug (моя регресія, виправлена):** видалив `LiqPay.php` як мертвий — зламався `get-form-data`
  - **Причина:** `OrderController` створює `new LiqPay(...)` у тому самому namespace, без `use`, тому аудит по імпортах його не бачив
  - **Фікс:** файл повернуто; зловив прогін роутів

- **Bug:** три роути вели на неіснуючі методи — `profile/{id}/ticket`, `get-price` (порожнє тіло), `set-currency`
  - **Фікс:** видалені. `set-currency` знайшовся вже під час прогону — тепер є перевірка резолву всіх роутів рефлексією

## Артефакти

- **Файли:**
  - `app/Providers/AuthServiceProvider.php` — `CLIENT_API_ABILITIES`
  - `app/Scopes/TicketScope.php` — `applyForClient()`
  - `app/Services/Api/v1/AppApi/AppApiProvider.php` — 35 роутів, явні методи
  - `app/Services/Api/v1/AppApi/Http/Controllers/TicketsController.php` — `visibleOrder()`
  - `CHANGES_APP_API.md` — журнал змін модуля
  - видалено 16 файлів у `app/Services/Api/v1/AppApi/`

- **Перевірка резолву всіх роутів:**
  ```php
  foreach (Route::getRoutes() as $r) {
      if (!str_starts_with($r->uri(), 'api/v1/app')) continue;
      [$class, $method] = array_pad(explode('@', $r->getActionName()), 2, null);
      if ($method && !method_exists($class, $method)) echo "БИТИЙ: {$r->uri()}\n";
  }
  ```

- **Baseline для регресії `TicketScope`** (кількість видимих квитків, до = після):
  agent `Api` 66 105, agent `Admin` 126 109, admin 126 109, driver 126 109.

## Backlog, що лишився

- `LiqPay.php` у всіх чотирьох копіях має `use App\Http\Controllers\InvalidArgumentException` — класу немає, будь-який виняток стає фаталом. `get-form-data` падає і в `AppApi`, і в незміненому `SiteApi`
- Невідповідний метод під `/api/*` віддає HTML SPA з кодом 200 замість JSON 405
- `Gate::before` викликає `hasRole('admin')`, а роль у базі — `Admin`; spatie порівнює регістрозалежно, тож bypass не працює

## Пов'язані нотатки

- [[10-Work/Projects/mono-system/project-overview]]
- [[10-Work/Projects/mono-system/docs/INDEX]]
- [[10-Work/Projects/mono-system/docs/app-api]]
- [[10-Work/Projects/mono-system/decisions/2026-08-24-client-ticket-visibility]]
- [[10-Work/Projects/mono-system/docs/bussystem-ticket-sync]] — там теж `TicketScope` як пастка
