---
title: "Проект: profumo-admin — статуси замовлення «Повернено» і «Передзамовлення»"
date: 2026-10-15
tags: [profumo-admin, profumo-site, work, session]
category: session
project: profumo-admin
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
Проаналізувати проект (гілка `sprint_3`), розібратись зі статусами замовлення, додати `returned` і `preorder` в адмінці та на вітрині без поломок.

## Виконано
- Аналіз master і `sprint_3` → [[project-analysis]] (security, schema drift, статуси).
- Адмінка: `config/crud.php` (status_order), `Order` константи + accessor на 6 статусів, `lang/uk/statuses.php`, `lang/uk/crud.php` (order-status), `ActivitiesField.vue`, `CheckTTNsJob` — `returned` виключено з трекінгу НП.
- Вітрина: `Order` константи + accessor, `lang/uk/statuses.php`, `OrderResource` fallback `?? trans()` (раніше невідомий статус = 500 у кабінеті), кольори іконок у `my-account.scss`.

## Важливі рішення (ADR)
| Рішення | Причина |
|---|---|
| Значення `returned`, `preorder` | у стилі наявних англ. ключів |
| `returned` фінальний → не трекати НП | інакше SMS по поверненому замовленню |
| `preorder` — накладений платіж як для неоплаченого | НП вважає оплаченим лише `payed`; не змінювали |
| `CheckTTNsJob` вітрини не чіпали | там `Order::ORDER_DONE_STATUS` не існує → job падає; полагодити = подвійні SMS (працює копія в адмінці) |

## Проблеми й як вирішили
- `OrderResource` вітрини падав би на новому статусі → fallback.
- Не запускалося: на машині немає php/node. Потрібна перевірка на dev.

## Артефакти
- profumo-admin: 6 файлів, не закомічено (гілка sprint_3).
- profumo-site: 4 файли, не закомічено (гілка sprint_3). Потрібна збірка SCSS (vite build).

## Пов'язані нотатки
- [[project-analysis]]
- [[profumo-site]]

## Дод.: завдання 1 з таблиці клієнта — плашка акції Sale/New
Джерело задач: Google Sheet 1WMM8ko1… (6 пунктів: 1 плашка акції, 2 товар в дорозі + розділення замовлення, 3 фільтр замовлень за статусом, 4 BI-аналітика, 5–6 статуси — зроблено).
- Адмінка: міграція `2026_10_15_120000_add_label_to_promotions_table` (`promotions.label` string default `sale`), `Promotions` LABEL_SALE/LABEL_NEW + fillable, `config/crud.php` `promotion_labels`, селект «Плашка на товарах» у `PromotionsCrudController` (вкладка Основне), lang `crud.promotion_label*`.
- Сайт: `Promotions` константи + fillable; `intro-product.blade.php` — New лише якщо всі акції товару `new`, інакше Sale.
- Не чіпали: бейдж «Акція» на сторінці товару (`product-single`).

## Дод.: завдання 3 — фільтр замовлень за статусом
- `OrderCrudController::setupListOperation` — фільтри `select_from_array` по `status` (crud.status_order) і `shipping_status` (crud.shipping_status), опції будує `filterOptions()`. Зразок — `ProductCommentsCrudController`. Фронт і міграції не потрібні.

## Дод.: завдання 2 — товар «в дорозі» + розділення замовлення
Рішення користувача: одна оплата на обидва замовлення; склад списується в мінус; позначка на рівні товару.
- Адмінка: міграція `2026_10_15_130000_add_in_transit_to_products_and_orders_tables` (`products.in_transit`, `orders.parent_order_id`), чекбокс на вкладці «Розцінки», `Order::parentOrder/childOrders`, колонка «Пов'язане замовлення» у списку.
- Сайт: `CheckoutService::createOrder` — partition кошика, дочірнє замовлення з `parent_order_id`, позиції зі статусом `in_transit`; `CheckoutController::completeOrders` — списання складу + ТТН для всіх пов'язаних (ТТН не для «в дорозі»), callbacks LiqPay/mono платять усі, `checkOrder` видаляє й дочірні; оплата на `total_amount_with_children`.
- Кошик: `CartHelper` не видаляє/не обрізає товари в дорозі; **виправлено баг** — неозгрупований `orWhereHas` видаляв позиції з усіх кошиків; `Cart::addProduct` без ліміту для в дорозі.
- UI: машинка + текст біля «Купити», «товар в дорозі» замість наявності, кнопка показується при 0, JS варіантів, швидкий перегляд, іконка кошика в каталозі.
- Ризик: production-checkout і оплата; не запускалось. Обов'язковий прогін на dev з LiqPay/mono sandbox.

## Дод.: завдання 4 — BI-аналітика
- Бекенд: `Api/System/AnalyticsController@orders` → `GET /api/system/analytics/orders?date_from&date_to` (`can:analytics-read`). Повертає summary (замовлення, виручка, середній чек, виконано/скасовано/повернено) + продажі по товарах (product_id+sub_product_id: к-сть, сума, середня/мін/макс ціна).
- Правила: період по `orders.created_at`; виручка, середній чек і продажі — без `cancelled`/`returned`; позиції `removed` не рахуються; кожне замовлення (і відокремлене «в дорозі») рахується окремо.
- Право: міграція `2026_10_15_140000_add_analytics_permission` створює `analytics-read` і дає ролям superAdmin/admin/owner (якщо існують).
- Фронт: `views/base/Analytics.vue` (пресети періоду, дати, 6 KPI-плиток, таблиця з сортуванням і підсумком), пункт сайдбару `analytics` з іконкою `chart-bar-regular.svg`, breadcrumbs, `base.analytics`.
