---
title: "Проєкт: 3G — Ознака QR-оплати у відомостях, звітах та Excel"
date: 2026-06-23
tags: [3g, work, session, reports, qr-payment, excel]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

# Ознака QR-оплати у відомостях, звітах та Excel

Гілка git: `driver`

## Мета сесії

Додати наскрізну ознаку «оплачено через QR-code» у звіти/відомості по рейсах та квитках, плюс попередній перегляд звіту в адмінці.

## Контекст QR-оплати (важливо для майбутніх сесій)

- Поле `tickets.is_qr_sale` (boolean, default false), міграція `2026_05_27_120000_add_is_qr_sale_to_tickets_table.php`. Деталі — [[2026-05-27-is-qr-sale-ticket-field]].
- Виставляється у `WidgetsController::getPortmoneUrl()` (`app/Http/Controllers/Api/WidgetsController.php`) для всіх квитків ордера (основний + `parentTicket` + `childTicket`) при генерації QR на оплату через Portmone.
- **Семантика «оплачено через QR»** = `is_qr_sale === true && status === Ticket::$STATUS_SOLD` (status `'sold'`). Саме лише `is_qr_sale=1` означає тільки що генерувався QR, не факт оплати.
- Еталон вже існував у `app/Http/Resources/System/Trip/Management/TripManagementTicket.php` (поле `is_qrcode`).
- Пов'язані квитки parent/child мають gotcha з TicketScope — див. [[2026-05-27-portmone-parent-child-ticket-status-fix]].

## Виконано (задачі → результати)

| Задача | Результат |
|--------|-----------|
| Backend Resource відомості | У `app/Http/Resources/System/Trip/Report/TripReportTicketsResource.php` додано поле `is_qrcode` (роут `GET /trips/{id}/report`, метод `TripsCrudController::report()`). |
| Vue відомість рейсу | `resources/js/crud/base/operations/trip-report/TripReportManager.vue` (Vue 3): блок «Оплачено QR-code» (іконка `/images/qrcode.svg`) ПЕРЕНЕСЕНО під сам статус (стовпець «Статус»). Додано computed `qrSum` і рядок «Всього QR-code» під «Всього». |
| Excel відомості рейсу | `TripExport.php` (роут `/system/reports/trips`): у колонці статусу додано ` (QR)`; внизу рядок «Всього QR-code» (`crud.total_qr`) із сумою лише QR-квитків. |
| Excel звіту по квитках | `TicketsExport.php` (з `/admin/reports`): у колонці статусу додано ` (QR)`. Підсумкові суми (`totalPriceBuy/Book/Sold`) приведено до 2 знаків через `number_format($x, 2, '.', '')`. |
| Новий тип звіту «Тільки QR» | `config/types.php` → `types_report` додано `['value' => 'qr']`. `ReportsController`: константа `$TYPE_QR = 'qr'`, гілка робить те саме що default (TicketsExport) але `getTickets(..., $onlyQr=true)` фільтрує `is_qr_sale=1 AND status='sold'`. Фронт не міняли — селект рендерить опції з API. |
| Попередній перегляд звіту | `ReportForm.vue` + бекенд: кнопка «Попередній перегляд» виводить під формою таблицю квитків, ідентичну Excel, з тією ж фільтрацією. |

## Важливі архітектурні рішення (ADR-рівень)

- **Антидубляж у `ReportsController`:** винесено `reportParams(Request): array` (спільний парсинг фільтрів) і `buildExport(array): FromArray` (єдиний switch по типах: default/qr→TicketsExport, profitability→ProfitabilityExport, drivers→DriversExport). `generate()` робить `Excel::store(buildExport(...))`, `preview()` робить `json(['rows' => buildExport(...)->array()])`.
- **Прев'ю 1:1 з Excel** бо переюзає той самий Export через `->array()` (усі Export реалізують Maatwebsite `FromArray`).
- **Роут:** `POST /system/reports/preview` → `ReportsController@preview`; api-bridge `reports.preview`.

## КРИТИЧНИЙ нюанс — як працюють фронт-переклади (для майбутніх сесій)

Фронт-переклади інжектяться **server-side** через `TranslationServiceProvider` (`welcome.blade.php` → `window._translations`, бібліотека `laravel-vue-i18n`).

- `getTranslations()` читає **PHP-файли** з директорій `lang/{locale}/` (напр. `lang/uk/crud.php`), а **НЕ** `lang/php_uk.json`.
- Ключі помилково додані в `php_*.json` НЕ резолвляться (виводиться сирий ключ).
- **Фікс:** класти ключі у `lang/uk/crud.php`.
- Кеш `translations` на 24 год лише якщо `APP_ENV != local`; тут local — тому кеш не заважав.
- Додані ключі: `crud.checked_ticket.paid_qr` = 'Оплачено QR-code', `crud.total_qr` = 'Всього QR-code', `crud.reports.types.qr` = 'Тільки QR', `crud.preview_button` = 'Попередній перегляд'.

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Переклад не виводився (сирий ключ) | Джерело перекладів — `lang/{locale}/*.php`, не `lang/php_*.json`. Прибрано мертві ключі з `php_*.json` (див. секцію вище). |
| Прев'ю «некоректно виводилось» | Таблиця була вкладена в `.report-form-wrapper` (flex-контейнер з `height: calc(100vh-130px)`, тільки під форму). Винесено результат в окремий блок `.report-result-wrapper` (sibling), стиль як `trip-report-table`. Прибрано `height: calc(100vh-130px)` у `resources/sass/reports.scss`. |
| Sticky-шапка таблиці прев'ю напівпрозора | `rgba(0,0,0,0.05)` → суцільний `#eaecef` + inset box-shadow для рамки. |
| Зазор зверху sticky-шапки | Прибрано `padding-top` у `.report-result-wrapper` (`padding: 0 8px 15px`). |
| Загальна сума з багатьма знаками | `number_format(..., 2, '.', '')`. |

## Артефакти (змінені файли)

**Backend:**
- `app/Http/Resources/System/Trip/Report/TripReportTicketsResource.php`
- `app/EXCELExports/Reports/TripExport.php`
- `app/EXCELExports/Reports/TicketsExport.php`
- `app/Http/Controllers/Api/System/ReportsController.php` (`reportParams`, `buildExport`, `generate` refactor, `preview`)
- `config/types.php`
- `routes/api.php` (`POST /reports/preview`)
- `lang/uk/crud.php` (4 нові ключі)

**Frontend:**
- `resources/js/crud/base/operations/trip-report/TripReportManager.vue`
- `resources/js/components/reports/ReportForm.vue` (кнопка прев'ю, `reportData()`, `preview()`, таблиця результату)
- `resources/js/api-bridge.js` (`reports.preview`)
- `resources/sass/reports.scss` (прибрано `height`)

## Залишкові задачі / нотатки

- Потрібен `npm run dev` / `npm run build` щоб побачити фронт-зміни.
- На проді (`APP_ENV != local`) після деплою — `php artisan config:clear` (config/types.php) і скинути кеш `translations`.
- Опція «Тільки QR» зараз без окремого permission (як default). За потреби можна додати permission як у `profitability`/`drivers`.
- Колонка `Ціна` у рядках квитків не округлена до 2 знаків (округлено лише підсумки) — за бажанням замовника.

## Пов'язані нотатки

- [[2026-05-27-is-qr-sale-ticket-field]] — походження поля `is_qr_sale`, проброс у Trip Management Resource.
- [[2026-05-27-portmone-parent-child-ticket-status-fix]] — TicketScope gotcha з parent/child квитками при Portmone-оплаті.
- [[2026-05-01-sms-templates-refactor]] — суміжний рефакторинг навколо квитків/нотифікацій.
