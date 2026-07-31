---
title: "Проект: onchul — Квитки: зовнішній номер, зміна користувача, пошук по телефону, фікс відомості"
date: 2026-07-21
tags: [onchul, tickets, work, session]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Серія доробок та багфіксів навколо системи квитків VTS:
- Запровадження зовнішнього номера квитка (external_number)
- Фіча зміни користувача при редагуванні квитка
- Багфікс пошуку квитків по телефону з `+`
- Багфікс фільтра типу відомості (report_type) в Excel-экспорті

## Виконано

| Задача | Результат |
|--------|-----------|
| Дослідження ланцюга статусів CurrentChangeStatusColumn | ✅ Визначено: config/crud.php → config/rule-statuses.php → акцесор Ticket::getCanStatusesAttribute() → компонент |
| Багфікс пошуку по телефону з `+` | ✅ Нормалізація digits-only у searchLogic TicketsCrudController (регрес-тест вислід, покриття зберігся) |
| Фіча external_number — модель & миграція | ✅ Додано nullable string колонку, не unique, миграція 2026_07_21_120000 |
| Фіча external_number — акцесор display_number | ✅ Новий акцесор Ticket::getDisplayNumberAttribute() = external_number ?: ticket_number; $appends=['display_number'] |
| Фіча external_number — booking chain | ✅ BookingRequest (tickets.*.external_number) → Order::createTickets(); фікс TypeError на getTrip (null-guard) |
| Фіча external_number — SHOW/Excel/PDF | ✅ Усі ресурси переведено на display_number; бухгалтерський експорт з fallback |
| Фіча external_number — фронт | ✅ BookPlacesForm (опційне поле після селекта користувача); transfer-компоненти на display_number |
| Фіча external_number — пошук | ✅ OR-гілка external_number у універсальному пошуку; публічні lookup-и |
| Фіча редагування external_number у формі | ✅ TicketsCrudController::setupUpdateOperation() + UpdateTicketRequest |
| Фіча зміни користувача в edit квитка | ✅ GetOrderMemberField/StoreOrderMemberField (право tickets-can-add-from-another-user); admin-override без перерахунку ціни |
| Фіча зміни користувача — трансферна пара | ✅ Ticket::transferPairLegs() → changeOrderMember обходить transfer pair, міняє member на всіх order-ах |
| Багфікс відомості — фільтр типу | ✅ 3-шаровий фікс: фронт шле report_type → ReportsController читає → TripExport бланкує ціну + сумує total по статусам |
| Тести external_number & зміна користувача | ✅ 56 tests pass (BookingExternalNumberTest, TicketsUpdateExternalNumberTest, TicketsSearchExternalNumberTest, TicketsUpdateOrderMemberTest, BookingGetTripDisplayNumberTest, TicketDisplayNumberTest, BookingServiceOrderMemberTest) |
| Тести відомості report_type | ✅ 12 нових тестів pass (TripExportReportTypeTest + TripsReportExportTest); 0 регресій |

## Важливі рішення (ADR)

| Рішення | Чому | Альтернативи |
|---------|------|--------------|
| external_number: окремий акцесор display_number, НЕ override getNumberAttribute | Щоб не затерти сирий number у генерації/фіскалізації/lookup; обговорювалось з користувачем | Override getNumberAttribute (небезпечно) |
| Пошук по external — окрема SQL OR-гілка | Акцесор у WHERE не працює в Eloquent | Субзапит (складніше) |
| Зміна користувача: admin-override без перерахунку ціни/квот | Бізнес-вимога; scope = весь order + transfer pair | Перерахунок ціни (дорогий, складний) |
| Право tickets-can-add-from-another-user enforced у Store-preprocessor, не в Request::authorize() | UpdateTicketRequest::authorize() — мертвий код у CRUD-фреймворку | Request::authorize() (не резолвиться) |
| Фікс відомості: preview = єдине джерело істини, export дзеркалить його | Уникати дублювання логіки; тести покривають обидва | Логіка в export (розбіжність) |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| getTrip TypeError: getTicketNumberAttribute() повертає null при partial-select | Null-guard: `(string)($this->api_ticket_id ?? $this->number ?? '')` з `: string` |
| Пошук по телефону `+7123456789` не знаходив `7123456789` | preg_replace('/\D/','',$value) нормалізація у searchLogic |
| Фільтр типу відомості ігнорувався в Excel-export | TripExport читає $reportType, бланкує ціну для non-driver, сумує total по статусам |

## Проблеми на дослідження (pre-existing, НЕ виправлені)

| Проблема | Статус | Примітка |
|----------|--------|---------|
| BookingService::resolveOrderUser() — `-1` → Member::findOrFail(-1) дасть 404 | pre-existing | booking-flow, не з цієї сесії |
| Ticket::getNameTripAttribute() — `: string` може повернути null | pre-existing | TypeError при серіалізації квитка без trip |
| config/rule-statuses.php — сторонні зміни | pre-existing | не з цієї сесії, комміт 8d4b37a |
| UpdateTicketRequest::authorize() — мертвий код | pre-existing | CRUD-фреймворк не резолвить authorize(); гейти мають йти до Store-preprocessor |
| tests/Unit/Quota/QuotaRuleTest.php — 5 failures | pre-existing | Посилаються на TripsService::filterPlacesByQuota() — методу немає в кодовій базі; не чіпався в сесії, падає ідентично на незміненому дереві |

## Артефакти

### Файли, змінені/створені

**Модель & миграція:**
- `database/migrations/2026_07_21_120000_add_external_number_to_tickets_table.php`
- `app/Entities/System/Ticket.php` (акцесор display_number, transferPairLegs, changeOrderMember)

**Backend контролери & сервіси:**
- `app/Http/Controllers/Api/Crud/TicketsCrudController.php` (searchLogic, setupUpdateOperation)
- `app/Http/Controllers/Api/System/BookingController.php` (getTrip фікс)
- `app/Http/Controllers/Api/Profile/TicketsController.php` (display_number)
- `app/Http/Controllers/Api/TicketsController.php` (display_number)
- `app/Http/Controllers/Frontend/ProcessedController.php` (display_number)
- `app/Http/Controllers/Api/System/ReportsController.php` (report_type читання)
- `app/Services/BookingService.php` (memberSelectOptions, resolveMemberSelection, changeOrderMember, createTickets external_number)

**CRUD PreProcessors (нові файли):**
- `app/Crud/PreProcessors/Get/GetOrderMemberField.php` (вивід member_id order)
- `app/Crud/PreProcessors/Store/StoreOrderMemberField.php` (enforcing право tickets-can-add-from-another-user)

**Request & Resource:**
- `app/Http/Requests/CRUD/UpdateTicketRequest.php` (external_number validation)
- `app/Http/Requests/Booking/BookingRequest.php` (tickets.*.external_number)
- `app/Http/Resources/System/TicketResource.php` (display_number)
- `app/Http/Resources/System/TicketProfileResource.php` (display_number)
- `app/Http/Resources/System/NewTicketsResource.php` (display_number)
- `app/Http/Resources/OrderCreatedResource.php` (display_number)
- `app/Http/Resources/TripPlaceTicketsResource.php` (display_number)
- `app/Http/Resources/System/Trip/Report/TripReportTicketsResource.php` (display_number)

**Excel експорти:**
- `app/EXCELExports/Reports/TripExport.php` (report_type: бланк ціни + фільтр total по статусам)
- `app/EXCELExports/Reports/TicketsExport.php` (display_number)
- `app/EXCELExports/Reports/TicketsAccountantExport.php` (display_number з fallback)
- `app/EXCELExports/Reports/TicketsDriverExport.php` (display_number)

**Order model:**
- `app/Entities/System/Order.php` (createTickets: external_number pass-through)

**Конфіг & мови:**
- `config/rule-statuses.php` (сторонні зміни, не з цієї сесії)
- `lang/uk/crud.php`, `lang/uk/fields.php`, `lang/uk/validation.php` (labels + validation messages)
- `lang/en/crud.php`, `lang/en/fields.php`, `lang/en/validation.php` (labels + validation messages)

**Frontend компоненти:**
- `resources/js/components/booking/Trip/BookPlacesForm.vue` (external_number поле, селект користувача)
- `resources/js/crud/base/columns/TicketTransferNumberColumn.vue` (display_number)
- `resources/js/crud/base/fields/TicketTransferInfoField.vue` (display_number)
- `resources/js/crud/base/operations/trip-report/TripReportManager.vue` (report_type селект, preview фікс)
- `resources/js/crud/base/operations/list/buttons/ListButtons.vue` (уточнення UI)
- `resources/js/crud/config/fields.js` (конфіг external_number field)
- `resources/sass/admin-booking.scss`, `resources/sass/media.scss` (стилі)
- `resources/js/crud/base/fields/route_bus_places_old/BookedTicketsModal.vue` (display_number)

**Тести:**
- `tests/Feature/Booking/BookingExternalNumberTest.php`
- `tests/Feature/Booking/BookingGetTripDisplayNumberTest.php`
- `tests/Feature/Crud/TicketsSearchExternalNumberTest.php`
- `tests/Feature/Crud/TicketsUpdateExternalNumberTest.php`
- `tests/Feature/Crud/TicketsUpdateOrderMemberTest.php`
- `tests/Unit/Entities/TicketDisplayNumberTest.php`
- `tests/Unit/Services/BookingServiceOrderMemberTest.php`
- `tests/Unit/EXCELExports/Reports/TripExportReportTypeTest.php`
- `tests/Feature/Reports/TripsReportExportTest.php`

**Інше:**
- `public/images/comment.svg` (нова іконка)

### Команди виконаних операцій

```bash
# Міграція
php artisan migrate

# Тести ( 56 pass + 12 pass = 68 нових тестів)
./vendor/bin/phpunit tests/Feature/Booking/
./vendor/bin/phpunit tests/Feature/Crud/
./vendor/bin/phpunit tests/Unit/Entities/
./vendor/bin/phpunit tests/Unit/Services/
./vendor/bin/phpunit tests/Unit/EXCELExports/
./vendor/bin/phpunit tests/Feature/Reports/

# Форматування
./vendor/bin/pint
```

## Стан коммітів

**Статус:** 2 коміти (нічого незакомічено на момент запису):
- `97426cb` (2026-07-21) — Фікс відомості (TripExport + ReportsController + TripReportManager)
- `8d4b37a` (2026-07-21) — Основна фіча (external_number + зміна користувача + телефон-фікс + дисплей-номер усюди)

**Тестовий статус:** ✅ 68 нових тестів pass, 0 регресій на коммітованих змінах.

**Рекомендація:** Коміти вже розкладені логічно (відомість окремо); потребує review & merge до master.

## Пов'язані нотатки

- [[project_permissions_system]] — права, Spatie roles (tickets-can-add-from-another-user)
- [[project_quotas]] — квоти місць, route_quotas/trip_quotas (member_id, no user_id)
- [[project_trip_report_merge]] — попередня фіча відомостей (2026-07-03); follow-up: баг валюти в TripExport
- [[project_transfer_3g_alignment]] — трансфери, feeder/child, transferPairLegs
- [[project_echeck_fiscalization]] — фіскалізація e-check, ticket_number в чеку (важливо не затерти)
- [[feedback_crud_dynamic_accessors]] — generic CRUD кличе аксесори; display_number один з них

