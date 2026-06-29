---
title: "Проєкт: 3G — QR-кнопка квитка винесена у CRUD-операцію + робочий payment-url"
date: 2026-06-25
tags: [3g, work, session, crud, operations, portmone, qr, payments]
category: session
project: 3g
status: completed
aliases: ["QR button to operation 3G", "TicketPaymentUrlOperation"]
pinecone_indexed: false
---

# QR-кнопка квитка → CRUD-операція + робочий payment-url

**Гілка:** `qr_driver_ticket`. Усі зміни **незакомічені**.

## Мета сесії
Винести існуючу QR-кнопку зі списку квитків (адмінка) з прямого `addButton` у контролері в окрему **CRUD-операцію** (трейт). Потім — зробити робочий ендпоінт, який модалка вже викликає, щоб він повертав `{ url, qr_code }`. Жодних змін UX/модалки понад потрібне.

## Контекст (досліджено)
- Кнопка `payment-url` рендериться компонентом `resources/js/crud/base/buttons/TicketPaymentURLButton.vue` (taби «Посилання» + «QR»), реєструвалась через `TicketsCrudController` (`addButton('entry','payment-url',[],10)`) і `ButtonManager.vue`.
- Модалка робить `api.get('/system/{crud}/{id}/payment-url')` (рядок ~118) і очікує JSON `{ url, qr_code }`.
- **Ключове відкриття:** на `HEAD` роуту `GET .../payment-url` **не існувало взагалі** — кнопка била в 404, модалка ніколи не заповнювалась даними. Реально робочий QR був лише в кабінеті водія через `WidgetsController::getPortmoneUrl/getTicketPortmoneUrl` (POST, повертають лише `{qrcode}` по order_id) — див. [[2026-06-25-qr-oplata-okremogo-kvytka]].

## Виконано

### Крок 1 — button → operation (структурний рефактор)
- Створено трейт `app/Crud/Operations/TicketPaymentUrlOperation.php`. `setupTicketPaymentUrlOperationDefaults()` додає ту саму entry-кнопку `addButton('entry','payment-url',[],10)`.
- `TicketsCrudController` — підключено `use TicketPaymentUrlOperation;`, прибрано прямий `addButton` із `setupListOperation()`.
- Фронт/lang/routes — НЕ чіпались. `route:list` лишився ідентичним (трейт спершу роутів не реєстрував).

### Крок 2 — робочий ендпоінт payment-url → `{ url, qr_code }` (на квиток)
- У трейті додано:
  - `setupTicketPaymentUrlOperationRoutes($segment,$routeName,$controller)` → `GET {segment}/{id}/payment-url`, name `tickets.payment-url`, meta `operation=payment-url`, `crud=$routeName`, `uses=@ticketPaymentUrl`. Саме **GET** (бо фронт робить `api.get`).
  - `ticketPaymentUrl(int $id): JsonResponse` → повертає `{ url, qr_code }`. `url` — Portmone-посилання на оплату квитка; `qr_code` — `base64_encode(QrCode::format('png')->size(399)->color(40,40,40)->generate($url))`.
- Логіка **інлайн**, відтворена ТОЧНО за `WidgetsController::getTicketPortmoneUrl` (рядки ~1230-1285), **без редагування Widgets**:
  - billNumber `{order_id}_{uuid}_t{ticket_id}`, amount `$ticket->price`, той самий `$source`/url (`autoinsurance?i=`base64(gzencode(json))), attribute4 з кодом квитка, `env(PORTMONE_PAYEE_ID)`, `route('general.portmone.callback')`.
  - side-effects: `is_qr_sale=true`, `payment_bill_number={...}_t{id}` (`payment_type` per-ticket гілка водія не ставить → і ми ні).
  - пошук `Ticket::withoutGlobalScope(TicketScope::class)->with('order')->find($id)` (анти-N+1).
- Edge-case: квиток не знайдено / без order → `{ url: null, qr_code: null }` (не 500).

## Важливі рішення (ADR-замітки)
- **Тип кнопки лишено `payment-url`** (не змінювали на `payment-qr`) — щоб `ButtonManager.vue` і фронтова модалка працювали без змін.
- **Генерувати на квиток** (не на замовлення) — рішення власника; billNumber/amount = водійський per-ticket метод.
- **WidgetsController не чіпати** — логіку дублюємо інлайн у трейті, щоб не ризикувати кабінетом водія. Свідома мала дуплікація замість рефактора Widgets.
- Модалку/UX не змінювали (повернули після зайвого рефактора — див. нижче).

## Проблеми й як вирішили

| Проблема | Рішення |
|---|---|
| Перший агент самовільно переписав модалку (прибрав таб «Посилання» + «Копіювати», змінив таби на ticket/order, тип кнопки на `payment-qr`) — вихід за межі задачі | Повний `git restore` фронту до HEAD; перероблено вузько — лише button→operation |
| Здавалось, що треба «зберегти стару поведінку payment-url» | З'ясували `route:list`-ом: роуту не існувало, кнопка била в 404 — зберігати не було чого. Реалізували ендпоінт як нову робочу логіку (за згодою власника) |

## Артефакти
- Змінені файли (незакомічено): `app/Crud/Operations/TicketPaymentUrlOperation.php` (новий), `app/Http/Controllers/Api/Crud/TicketsCrudController.php`.
- Новий роут: `GET api/system/tickets/{id}/payment-url → tickets.payment-url › TicketsCrudController@ticketPaymentUrl`.
- Поля `is_qr_sale`/`payment_bill_number`/`payment_type` на `tickets` — у БД **присутні** (migrate:status: Ran, batches 33/35/36).
- Pint PASS; `php -l` чисто.

## Відкриті питання / ризики
- Роут **без permission-middleware** (як інші ticket-операції у зразках) — за потреби додати guard.
- Ендпоінт відкритий для будь-якого статусу квитка (кнопка ховається на фронті лише для ≠ `booked`/`prebooked`) — за потреби серверний guard на статус.
- Дублювання Portmone-білдера між трейтом і `WidgetsController` — кандидат на винесення у спільний сервіс (окрема задача, бо торкнеться Widgets).
- Спадкові ризики Portmone callback (підпис не перевіряється, `$ticket->code` → null) — успадковані, не в цій сесії.

## Ручні кроки (лишились користувачу)
1. `npm run build` — зібрати Vue (якщо ще не зібрано на цій гілці).
2. Перевірити кнопку в браузері: клік → модалка → таб «QR» показує картинку, таб «Посилання» — копіювання url.
3. За бажанням — написати feature-тест на `GET .../payment-url` (статус 200, структура `{url, qr_code}`, side-effects на квитку).
4. Розглянути permission-guard на роут/статус.

## Пов'язані нотатки
- [[2026-06-25-qr-oplata-okremogo-kvytka]] — поквиткова QR-оплата в кабінеті водія (джерело логіки getTicketPortmoneUrl)
- [[2026-06-23-qr-payment-reports]]
- [[2026-05-27-is-qr-sale-ticket-field]]
- [[project-overview]]
