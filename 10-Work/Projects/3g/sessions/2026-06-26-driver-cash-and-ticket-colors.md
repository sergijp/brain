---
title: "Проект: 3g — Каса водія + підсвічування квитків"
date: 2026-06-26
tags: [3g, work, session, driver-cabinet, cash]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
Реалізувати підрахунок «каси водія» (готівка, яку водій збирає на своєму відрізку рейсу) у кабінеті водія, з урахуванням статусів, трансферів, типів оплати та станції збору (посадка vs висадка); додати «Загальну виручку» рейсу; візуальне підсвічування цін квитків; масив квитків «оплата по приїзду» на станції висадки.

## Виконано
- **`WidgetsController::calculateDriverCash(Trip, Driver)`** — підрахунок каси водія. Старі обчислення `cash_amounts_all` закоментовано, замінено. Працює для табів «Квитки» (активний) і «Архів».
- **Розділення збору посадка/висадка**:
  - звичайна готівка (`cash`/`NULL`) — по станції ПОСАДКИ (`from_id`), межа сегмента `[from, to)` (to виключна);
  - **оплата по приїзду (`not_paid_yet`)** — по станції ВИСАДКИ (`to_id`), межа `(from, to]` (to ВКЛЮЧНА — кінцева станція дістається останньому водієві).
- **Спільні хелпери** (рефактор, без дублювання): `driverStationSets($trip,$driver)` → `['boarding'=>[from,to), 'arrival'=>(from,to]]`; `cashTicketsQuery($trip)` (спільні фільтри); `sumCashTickets($tickets)` (ефективні ціни + групування по «станції збору»: to_id для not_paid_yet, інакше from_id).
- **`cash_amounts_total` («Загальна виручка»)** — `calculateTotalCash($trip)`: та сама логіка без сегмента водія (весь рейс). Поле у `shortTripManagementWidget`/`getHistoryTrips`/`TripDriverManagementResource`.
- **`tickets_on_arrival`** на кожній станції у `/widgets/short-trip-management` — квитки `not_paid_yet` по `to_id`, у форматі `TripManagementTicket`. ГЕЙТУЄТЬСЯ по сегменту висадки ЗАЛОГІНЕНОГО водія `(from, to]`: бачить лише водій, що ЇДЕ ДО станції; хто лише сідає там — `[]`. Без N+1.
- **Фронтенд — підсвічування ціни + іконки money** у `TripTickets.vue` (ShortTripManagement) і `Tickets.vue` (DriverWidget Tab 2). Через inline `:style` (CSS-конфлікт: `.text-field{color}` і `.ticket-table-col-icon{filter}` перебивали Bootstrap-класи). Ціна — `color`, SVG-іконка — `filter`. Спільний `priceColorState`.
- **`payment_type`** додано у resource `TripManagementTicket` (живить TripTickets) і payload `getTickets()` (живить Tickets.vue).
- **«Виручка» + «Загальна виручка» в одному рядку** (`Tickets.vue`, flex gap), переклад `crud.total_vurychka`.
- **Видалено** тест `tests/Feature/DriverCashTest.php`.

## Колірна логіка ціни/іконки (фінальна)
| checked | payment_type | Колір |
|---|---|---|
| null (не відмічено) | — | звичайний (без override) |
| false (no-show) | — | сірий |
| true | not_paid_yet | червоний |
| true | card / qr_code | сірий |
| true | cash / NULL | зелений |
(checked приходить як 0/1/null — обробка явна.)

## Важливі рішення (ADR)
| Рішення | Обґрунтування |
|---|---|
| Каса за СТАТУСОМ (booked/prebooked), sold виключено | payment_type майже завжди NULL (148675 vs 11 cash); sold = онлайн-оплата |
| NULL = готівка | історичні квитки NULL; інакше каса обнулилась би |
| not_paid_yet лишається в касі, але по ВИСАДЦІ (to_id) | оплата по приїзду — пасажир платить на станції прибуття водієві, що його довіз |
| card/qr виключено з каси + сірий колір | безготівка не в касі водія |
| Посадка `[from,to)`, висадка `(from,to]` | симетрично: без перетину сусідніх водіїв; кінцева станція → останньому водієві |
| Ефективна ціна = ціна parent при `parent_id` | трансфер: повна сума на основному рейсі (перевірено: child 2200 → parent 2900) |
| `whereNull('parent_id')`-guard вимкнено | child враховується з ціною parent |
| tickets_on_arrival гейтується по arrival-сегменту водія | бачить лише водій, що їде ДО станції висадки |
| Крос-рейсове подвоєння parent — ВІДКЛАДЕНО | guard навмисно не ставили |

## Проблеми й як вирішили
- Архів не показував суми (7240) → фільтр `payment_type='cash'` нічого не матчив (усе NULL) → перехід на статус-логіку.
- Кольори не відображались → CSS-конфлікт (`.text-field`/`.ticket-table-col-icon` перебивали класи) → inline `:style`/`filter`.
- Невідмічені квитки ставали сірими → розділили `checked===null` (оригінал) vs `false` (сірий).
- Кілька промахів із компонентом для кольорів → фінально `TripTickets.vue` (дерево DriverWidget→ShortTripManagementWidget→StationManager→TicketsManager→TripTickets) + `Tickets.vue`.
- not_paid_yet рахувались по посадці (мали по висадці) → розділення from/to + межа (from,to].
- not_paid_yet на фінальній станції зависали → межа висадки to-включна.
- Тести не запускались — немає `.env.testing` (тест згодом видалено).

## Артефакти (змінені файли)
- `app/Http/Controllers/Api/WidgetsController.php` — calculateDriverCash, calculateTotalCash, driverStationSets, cashTicketsQuery, sumCashTickets, shortTripManagementWidget (+tickets_on_arrival гейтований, +cash_amounts_total), getHistoryTrips, getTickets (+payment_type)
- `app/Http/Resources/System/Trip/Management/TripManagementTicket.php` — +payment_type
- `app/Http/Resources/System/Trip/Management/TripManagementStation.php` — +tickets_on_arrival
- `app/Http/Resources/System/Trip/Management/TripDriverManagementResource.php` — +cash_amounts_total
- `lang/uk/crud.php` — +crud.total_vurychka
- `resources/js/crud/base/operations/trip-management/tickets/TripTickets.vue` — кольори ціни+іконки
- `resources/js/crud/base/operations/trip-management/tickets/Tickets.vue` — кольори + Виручка/Загальна виручка в один рядок
- `resources/js/crud/base/operations/trip-management/trips/TripHistory.vue` — +Загальна виручка
- ВИДАЛЕНО: `tests/Feature/DriverCashTest.php`
- Гілка: `driver`. НЕ закомічено. **Потрібен `npm run build`**.

## Незавершене / наступні кроки
- `npm run build` (фронтенд-зміни не в прод-асетах).
- Крос-рейсове подвоєння parent-квитка (guard).
- Коміт на гілці `driver`.

## Пов'язані нотатки
- [[project_qr_single_ticket_payment]]
- [[project_qr_button_operation]]
- [[project_sms_templates_refactor]]
