---
title: "profumo-admin — аналіз проекту і відомі проблеми"
date: 2026-10-15
tags: [profumo-admin, architecture, audit]
category: docs
project: profumo-admin
status: active
aliases: ["profumo-admin-analysis"]
pinecone_indexed: false
last_verified: 2026-10-15
---

# profumo-admin — аналіз і відомі проблеми

## Контекст
Адмінка інтернет-магазину парфумерії/косметики. Laravel 9 API (Passport, spatie permission/activitylog) + Vue 2.7 SPA (Vite). Репо `git@github.com:VissOn/profumo-admin.git`, остання активність 2024-09 (усі коміти "wip"). Вітрина [[profumo-site]] ходить у **ту саму БД**; міграції живуть тільки тут.

Код успадкований від квиткового проекту Bustrek — багато мертвого коду (Trip/Ticket mails, booking store, passports/stations поля, channels.php), який посилається на неіснуючі класи.

## Ключові контракти
1. **CRUD-фреймворк**: `Route::crud` макрос → static `setup*Routes` трейтів `app/Crud/Operations` → `crudInfo` (`/system/{crud}/crud/info/{op}`) → фронт рендерить generic форми. Тип поля → Vue-компонент (`crud/config/fields.js`) + `Get/Store{Type}Field` preprocessors за конвенцією імен.
2. **Новий CRUD** = entity + controller + `routes/api.php` + `api-bridge.js` + `crud-routes.js` + `config/breadcrumbs.js` (інакше throw) + panel-card у `views/base/*.vue` + permissions + lang.
3. **Auth-модель — `Member`** (адміни й покупці разом, ролі spatie). `users` таблиці немає.
4. Поля фронту — не v-model, а `getValue()/setValue()` через refs (`FieldMixin`).
5. Переклади фронту — `window._translations`, кеш 24 год поза `local`.

## Доменна модель (коротко)
- Product: price, price_old, quantity (склад), brand_id, main_category_id, gallery (JSON). Переклади — `product_texts` (поліморфний `ModelHasTexts`).
- SubProduct — варіант/об'єм: text, price/old_price (рядки!), `count` = boolean «є в наявності».
- Category — nestedset; атрибути успадковуються від предка.
- Discount — лише групування для лендингу, без % ; реальна знижка — `orders.discount` (%).
- Order: статуси вручну в адмінці; листів про замовлення немає.
- Імпорт: CSV → `ImportProductsJob` → `SplitFileJob` upsert by `article` (без unique index → дублікати); скрапери Notino/MakeUp → `SaveProducts` (match by slug, ніколи не оновлює).

## Відомі проблеми (станом на 2026-10-15, перевірено читанням коду, не запуском)

### Критичні (безпека)
- `app/PaymentMethods/CardPayment.php:31` — **private_key LiqPay у payload до браузера**; callback не перевіряє status, `!==` замість `hash_equals`. Зараз не підключено (`registerRoutes` ніде не викликається), але небезпечно при оживленні.
- `Api/System/FilesController`, `ImagesController`, `ActivitiesController` — `new $request->model` без `can:`; аплоад з клієнтським розширенням (можна `.php`); delete будь-якого шляху на public disk; `ImportCrudController` — path traversal через `filename`.
- `app/Crud/Operations/ListOperation.php:34` — закоментовано `can:{crud}-read` → будь-який Member з токеном (у т.ч. покупець) читає users/roles/orders/settings через `/search`. Також без `can:` усі `crud/info/*`, `/system/users`, `/system/import/*`, files/images.
- `routes/api.php` — публічний `Route::any('test', … dd(2))`.

### Високі
- Напівживий Tenancy: `IdentifyTenants` у `web` групі, `tenants.identify` у `BroadcastServiceProvider` → `/broadcasting/auth` падає (пакета немає). `/customer/registration` фатал (`Tenancy::setTenant`).
- `resources/js/store/index.js:187` — `alert("SOCKET's WORKS")`.
- `per_page` default 1 без верхньої межі; sort по будь-якій колонці від клієнта.
- CORS `*`.

### Розбіжність схеми й коду
- `currencies.exchange` vs `currency->factor` у `Product.php:61,202-226` — ціни з валютою = 0/SQL error.
- `Brand::products()` через `main_category_id` замість `brand_id` (`Brand.php:56`).
- `product_texts` без `subtitle/subcontent/alt_image`, які пише код; `pages` без `template/gallery`; немає міграцій `users`, `files`, `parsing_files`.
- `OrderCrudController` при статусі payed видаляє **всіх** ProductMember продукту.
- Статуси замовлення розходяться між `config/crud.php` і константами `Order`.
- Ймовірно прод-БД правили вручну → перед правками звіряти з реальною схемою.

### Інфраструктура
- Немає `composer.lock` / `package-lock.json` → перше встановлення тягне нові версії.
- Тестів немає (тільки Example), CI немає, scheduler порожній.
- На машині розробника (macOS) немає php/node/docker у PATH — запускати потрібно деінде.

## Пов'язані
- [[profumo-site]]
- [[2026-10-15-init-claude-md]]

## Гілка `sprint_3` (перевірено 2026-10-15)
- 171 коміт поверх `master` (2024-09 → 2025-12), 189 файлів, +8158/−1934. Містить у собі `sprint_3_back`, `sprint_3_front`, `nova-poshta`, `new_tasks` — це найповніша гілка. Синхронна з `origin/sprint_3`.
- Нове: Нова Пошта (ТТН, PDF маркування, трекінг `CheckTTNsJob` щогодини), SMS AlphaSms (`OrderObserver`, кнопка SendSms), лист нового замовлення, promotion_products з %, request-cooperation, benefit-links, шаблони імпорту, статуси order_products, soft deletes на products/sub_products/orders, `sub_products.count` → `active` + `quantity`, timezone Europe/Kyiv, статус замовлення `cancelled`.
- 30 нових міграцій. `2024_19_11_231415_create_templates_import_table` — невалідна дата в імені (сортується після 2024_12_*).
- **Не виправлено** з master: `can:read` у ListOperation, `new $request->model` у Files/Images, LiqPay private_key, `currency->factor`, `Brand::products()`, Tenancy-middleware, видалення ProductMember.
- **Нові критичні**:
  - `routes/api.php` `Route::any('test')` без auth тепер запускає `CheckTTNsJob::dispatchSync` → запит до НП по всіх замовленнях і **SMS клієнтам** (платно, спам) + оновлення статусів.
  - `/api/v1/general/save-images` — публічне завантаження файлу з клієнтським розширенням у public disk.
  - `use App\Jobs\СreateTTNJob` з кириличною «С» у `routes/api.php`.

## Статуси замовлення (sprint_3, перевірено 2026-10-15)
Довідника в БД немає — значення це рядки в колонках, список для адмінки в `config/crud.php`, підписи в `lang/uk/statuses.php`, частина дублюється константами `Order`/`OrderProduct` і хардкодом в accessor-ах. Вітрина (profumo-site) має власну копію моделі `Order` з іншим набором констант.

| Вимір | Колонка | Значення | Список (адмінка) | Хто змінює |
|---|---|---|---|---|
| Статус замовлення | `orders.status` | new, payed, done, cancelled | `crud.status_order` | вітрина: new при checkout, payed після оплати (LiqPay/mono); адмін вручну |
| Статус доставки | `orders.shipping_status` | forming, shipped («Готове до відправки»), done | `crud.shipping_status` | вітрина: forming; авто → shipped коли всі позиції `in_stock` (`StoreOrderProductDetailsField`); адмін вручну |
| Статус позиції | `order_products.status` | ordered, in_transit, in_stock, dispatched, removed | `crud.status_order_product` | ordered при створенні; далі адмін |
| Оплата | `orders.payment_status` | default pending; статус від LiqPay | — | тільки callback оплати |
| Нова Пошта | `orders.status_code_np` | код НП (1 = ТТН створено) | — | Create/Update/DeleteTTN, CheckTTNsJob щогодини |

Реакції: `OrderObserver` — лист при зміні `status`; SMS на кожен update, якщо `shipping_status === 'done'` (не лише при переході → повторні SMS). Зміна статусу позиції → лист. CheckTTNsJob → SMS при зміні коду НП, текст з `settings.np_poshta`.

Розбіжності: accessor `Order::getOrderStatusesAttribute` в адмінці лише new/payed; на вітрині 4 значення + невикористані `created`, `delete`. Підпис `shipping.done` = «Замовлена виконане» (помилка). Ключі статусів позицій лежать у `statuses.order.*` разом зі статусами замовлення.
