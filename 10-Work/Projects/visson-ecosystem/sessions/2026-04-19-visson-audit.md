---
title: "Проект: Visson — Сесія Аудит і план рефакторингу"
date: 2026-04-19
tags: [work, session, code, visson, refactoring, audit]
category: work
project: visson-ecosystem
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії

Проаналізувати 30+ проектів у `~/Source`, які базуються на спільній самописній системі, і запропонувати план оптимізації та рефакторингу без введення мульти-тенантності.

## ✅ Виконано

- Інвентаризовано 30 тек (14 активних, 7 legacy, 10 стабів/інше) → [[../project-overview|MOC]]
- Доведено дублювання коду (md5 cmp): 11 middleware, 6 CRUD Operations, 5 Helper-трейтів, 2 ServiceProviders — 100% ідентичні між 5 проектами
- Виявлено 17 контролерів >500 рядків; топ — `buktreck/ApplicationsCrudController.php` (2 071), `3g/TripsCrudController.php` (1 709)
- Виявлено 0 власних індексів у 319 міграціях
- Знайдено N+1 у `mono-system/resources/views/print-ticket/index.blade.php:5`
- Сформульовано архітектуру: 5 composer-пакетів + 1 NPM (`visson/core-middleware`, `visson/crud-kit`, `visson/system-entities`, `visson/helpers`, `visson/excel-exports`, `@visson/ui-kit`)
- Створено 5-фазну дорожню карту на 14 тижнів
- Згенеровано звіт `.docx` (14 сторінок) у `~/Source/outputs/Visson-Refactoring-Report.docx`
- Створено Obsidian-нотатки по кожному проекту (поточна сесія)
- **Пройдено поглиблений refactor-аудит 9 активних** — air-trans, grosser, buktreck, 3g, mono-system, vts, bsystem, bustick-admin, padmin. У кожному `project-overview.md` записана секція `🔧 Рефакторинг (2026-04-19)` з P1/P2/P3 знахідками з `файл:рядок`.

## 🔍 Поглиблений аудит — ключові знахідки

### Наскрізні патерни Visson-core (8/9 проектів)

- **`app/Crud/Operations/CopyOperation.php:53–54`** — `dd($e)` ×2 у production. Виняток: `bustick-admin` (вже очищено).
- **`app/Http/Controllers/LiqPay.php`** (~264 рядки) — у Controllers замість Services, усі 9 проектів.
- **`docker/*/Dockerfile`** — PHP 7.2 при composer `^8.1/8.2`, усі 9.
- **`app/Entities/Tenant/*`** + `Listeners/Tenant/*` — dead tenancy convention без `stancl/tenancy` у composer.json. Виняток: `vts`.
- **`env()` поза `config/`** — 13–45 місць на проект. Рекорд: `vts` (43), `3g` (20+ у одному контролері).
- **Vuex замість Pinia, 0 TypeScript** — усі 9.
- **Tests — тільки `ExampleTest`** — усі 9.
- **`const STATUS_*/TYPE_*/CURRENCY_*`** замість Enums — усі 9.

### Топ god-файлів через всі активні

| Rank | Файл | Рядків | Проект |
|---|---|---|---|
| 1 | `ApplicationsCrudController.php` | **2 071** | buktreck |
| 2 | `resources/js/store/booking.js` | **1 732** | vts (!frontend!) |
| 3 | `TripsCrudController.php` | 1 709 | 3g |
| 4 | `TripsCrudController.php` | 1 256 | bsystem |
| 5 | `Trip.php` (model) | 1 188 | mono-system |
| 6 | `WidgetsController.php` | 1 179 | bsystem / 3g |
| 7 | `TripsCrudController.php` | 1 151 | mono-system |
| 8 | `Trip.php` | 1 120 | vts |
| 9 | `TripsCrudController.php` | 1 112 | bustick-admin |
| 10 | `Trip.php` | 1 085 | 3g |

### Ранжування за "станом здоров'я"

1. 🥇 **air-trans** — еталон (найменший controller 467)
2. 🥈 **vts** — єдиний без tenant-stubs, 7 Observers/Scopes, 14 Jobs, 54 FK-індекси
3. 🥉 **grosser** — L11 ok
4. **buktreck** — ⚠ god-controller 2071
5. **mono-system** — ⚠ god-model 1188 + N+1
6. **3g** — ⚠ dd()+env розсип
7. **bustick-admin** — заморожений 2 роки, але Vite вже є
8. **padmin** — WIP 35–40%, рекомендація merge→grosser
9. **bsystem** — L7 EOL, окремий upgrade-трек 3–4 тижні

### Специфічні знахідки по проектах

- **air-trans**: `ModuleManager.php` 624 рядки — неясно фіча чи tech debt. `saveTicket()` потенційно дублює `TicketsCrudController`.
- **grosser**: `Entities/System/Directories/Route.php` 468 рядків god-model, `Product.php` 325, лише 2 Services.
- **buktreck**: `ApplicationsCrudController.php` 2071 — `setupListOperation` (680+), `setupCreateOperation` (450+), `setupUpdateOperation` дублюють 48 полів тричі. `Application` model 416 з 16 STATUS-констант.
- **3g**: `TripsCrudController.php:1540` — `dd()` у 4 catch-блоках production. SMS-логіка дубльована у `sendAllSms` vs `sendSmsMessage`.
- **mono-system**: N+1 у `print-ticket/index.blade.php:5–16` — `$ticket->trip->stations->where(...)->first()`. `Trip` 1188 рядків 110+ методів.
- **vts**: **Busfor API інтеграція** (`Services/Api/v1/Busfor/` — 50+ маршрутів) — кандидат на `visson/busfor-client`. `error_log()` у `Order.php:122`.
- **bsystem**: L7/PHP 7.2 EOL. 117 файлів доменної логіки у 6 API v1 модулях (GlobalApi, PrivatBank, ...). Tenancy/tenancy v1 в 274 файлах. Tests — 4.
- **bustick-admin**: `CopyOperation` вже очищено (єдиний!), Vite 4. 18 tenant-моделей без `stancl/tenancy`.
- **padmin**: `dd(1)` у `LoginController` блокує auth. 3 payment methods з `// TODO`. 57 tenant-stubs. Доцільно merge→grosser.

## 🔑 Нові/оновлені рішення (ADR) — 2026-04-19 (продовження)

| Дата | Рішення | Причина |
|------|---------|---------|
| 2026-04-19 | `LiqPay.php` → перший composer-пакет `visson/liqpay-service` | Ідентичний у 9 проектах, класичний кандидат на виділення |
| 2026-04-19 | Видалити dead tenant-код у 8 проектах (окрім vts) | За правилом користувача тенантів немає; залишати плутає |
| 2026-04-19 | `padmin` → merge у `grosser` замість реанімації | Обидва e-commerce; padmin 2 роки без активності; grosser уже L11 |
| 2026-04-19 | Busfor-інтеграція vts → `visson/busfor-client` | Унікальна для vts, але може знадобитися в майбутньому для інших |
| 2026-04-19 | `CopyOperation.php` — одна заміна `dd()` у core-шаблоні, потім розкатати у 8 проектів | 100% ідентичний блок коду |

## 🚀 Оновлені quick wins для Фази 1

1. `CopyOperation.php` — `dd()` → `Log::error()` у 8 проектах (10 хв роботи на проект).
2. Docker PHP 7.2 → 8.2 у 9 проектах (Dockerfile майже ідентичний).
3. `LiqPay.php` — порівняти md5, якщо ідентичний → `visson/liqpay-service` одразу.
4. `env()` винесення з `TripsCrudController.php` (3g) і `AuthCheck` middleware (vts).
5. Видалити dead tenant-код (`Entities/Tenant/*`, `Listeners/Tenant/*`) у 8 проектах.

## 🔑 Важливі рішення (ADR)

| Дата | Рішення | Причина | Альтернатива |
|------|---------|---------|--------------|
| 2026-04-19 | Приватні composer-пакети, НЕ моно-репо | 14 незалежних git-репо вже існують; команда звикла; semver дає контроль за темпом оновлень | Nx-моно-репо (великий одноразовий переїзд) |
| 2026-04-19 | `air-trans` — еталон | Laravel 11, найсвіжіший, активна розробка | `buktreck` (теж L11, але гігантський ApplicationsCrudController) |
| 2026-04-19 | Без мульти-тенантності | Свідоме рішення користувача; складність не виправдана для 14 незалежних клієнтів | Tenancy for Laravel — відкладено на "колись" |
| 2026-04-19 | Legacy L7/8 (gt17, gt17admin, ats, santaopt, v-admin*) — заморозити | Різниця стеків L7 vs L11 + Backpack CRUD не сумісні з ядром | Апгрейд — надто довго, бізнес-цінність низька |
| 2026-04-19 | bsystem — окремий трек | L7 + активна розробка → окреме рішення: апгрейд vs форк-легасі | Тягти в Фазу 2 разом з L11 — ризик поламати прод |

## 🐛 Проблеми знайдені

### P1: 0 індексів БД у 319 міграціях
- **Де:** database/migrations у всіх проектах
- **Наслідок:** Table scans на trips, tickets, orders
- **Вирішення:** Нові міграції з `$table->index([...])` у Фазі 1

### P2: N+1 у Blade print-ticket
- **Де:** `mono-system/resources/views/print-ticket/index.blade.php:5`
- **Наслідок:** Друк 100 квитків = 200+ запитів
- **Вирішення:** `$ticket->load('trip.stations')` у контролері

### P3: Контролери-монстри
- **Де:** `buktreck/ApplicationsCrudController.php` (2 071), `3g/TripsCrudController.php` (1 709), `santaopt/ViberController.php` (1 897)
- **Вирішення:** Розбивка на Service + Action-класи у Фазі 5

### P4: `dd()` і `error_log()` у production (знайдено в аудиті 9 проектів)
- **Де:** `CopyOperation.php:53–54` у 8 проектах; `TripsCrudController.php:1540` (3g — 4 catch-блоки); `LoginController.php` у padmin (`dd(1)`), bustick-admin; `error_log()` у vts `Order.php:122` і `Services/Api/v1/Busfor/Http/Controllers/AuthController.php:59`
- **Вирішення:** `Log::error()` + pre-commit hook для заборони `dd|var_dump|error_log`

### P5: Dead tenant-код без реальної tenancy-бібліотеки
- **Де:** 8 з 9 активних проектів (виняток — vts). `app/Entities/Tenant/*`, `app/Listeners/Tenant/*`, `database/tenant/`. У padmin — 57 файлів, у bustick-admin — 18+6
- **Вирішення:** Видалити повсюди (правило користувача: тенантів немає)

### P6: `env()` поза `config/` у production коді
- **Де:** у кожному з 9 проектів (13–45 місць). Рекорд: vts (43), 3g (20+ у одному `TripsCrudController.php`)
- **Наслідок:** `config:cache` ламає застосунок
- **Вирішення:** Винести у `config/services.php` і читати через `config()`

## 📎 Артефакти

- Звіт: `~/Source/outputs/Visson-Refactoring-Report.docx` (395 параграфів, 14 сторінок, валідовано)
- MOC: [[../project-overview|Visson Ecosystem MOC]]
- Нотатки по проектах: 22 файли у `10-Work/Projects/`

## 🔗 Пов'язані нотатки

- [[../project-overview|Visson Ecosystem MOC]]
- [[../../../../CLAUDE-RULES|CLAUDE-RULES]]
