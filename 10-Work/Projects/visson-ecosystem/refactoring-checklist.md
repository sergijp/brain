---
title: "Visson — Checklist рефакторингу (консолідований)"
date: 2026-04-19
tags: [work, visson, refactoring, checklist, action-list]
category: work
project: visson-ecosystem
status: active
pinecone_indexed: false
---

# 🛠 Visson — Checklist рефакторингу

> Консолідований список дій з поглибленого аудиту 9 активних проектів (2026-04-19).
> Упорядкований за фазами і пріоритетами. Кожен пункт має `файл:рядок` або перелік проектів.

---

## 🔥 ФАЗА 0 — Quick Wins (1 тиждень, low-risk)

> Мета: прибрати найболючіше за 5–15 хв на проект, без архітектурних змін.

### 0.1 Санітизація `dd()` / `error_log()` у production

- [ ] `app/Crud/Operations/CopyOperation.php:53–54` — замінити `dd($e)` ×2 на `Log::error()` у **8 проектах** (air-trans, grosser, buktreck, 3g, mono-system, vts, bsystem, padmin). Виняток: bustick-admin (вже очищено).
- [ ] `3g/app/Http/Controllers/TripsCrudController.php:1540` — `dd()` у 4 catch-блоках. Замінити на `Log::error()`.
- [ ] `padmin/app/Http/Controllers/Api/Auth/LoginController.php` — прибрати `dd(1)` (блокує автентифікацію!).
- [ ] `vts/app/Entities/Tenant/Order.php:122` — `error_log()` → `Log::`.
- [ ] `vts/app/Services/Api/v1/Busfor/Http/Controllers/AuthController.php:59` — `error_log()` → `Log::`.
- [ ] `bustick-admin/...` — перевірити 19 файлів з `dd()/var_dump()/die()` (вже сканувалось, уточнити список).
- [ ] Додати **pre-commit hook** на заборону `dd|dump|var_dump|error_log|die\(` у `app/**/*.php`.

### 0.2 Docker PHP 7.2 → 8.2 (9 проектів)

- [ ] `docker/web/Dockerfile:1` — `php:8.2-apache` замість 7.2 у **всіх 9 активних**. Composer уже вимагає `^8.1/8.2`, контейнер фактично несумісний.

### 0.3 Видалення dead tenant-коду (8 проектів, виняток — vts)

> composer.json НЕ містить `stancl/tenancy` — це manual stub без реалізації. Правило користувача: тенантів немає.

- [ ] `app/Entities/Tenant/*` — видалити у всіх крім vts.
- [ ] `app/Listeners/Tenant/*` — видалити.
- [ ] `database/tenant/` — видалити міграції.
- [ ] Окремо рекорди: padmin (57 файлів), bustick-admin (18 моделей + 6 Listeners), bsystem (tenancy/tenancy v1 у 274 файлах — потребує окремого треку).

### 0.4 `env()` виніс у `config/`

- [ ] `3g/app/Http/Controllers/TripsCrudController.php` — 20+ `env()` → `config('services.sms.*')` тощо.
- [ ] `vts` — 43 `env()` у app/ (рекорд) → `config/services.php`.
- [ ] `mono-system/app/` — 28 `env()`.
- [ ] `buktreck/app/Http/Controllers/Api/Auth/LoginController.php` — env() у controller.
- [ ] `grosser/app/Http/Resources/OrderProductResource.php`, `ApiService.php`, `LoginController.php` — env() leak.
- [ ] `bustick-admin/app/Listeners/Tenant/ConfigureTenantConnection.php:21–22` — `env('DB_USERNAME')`/`DB_PASSWORD` (найкритичніше — Listener читає env прямо).
- [ ] Решта проектів — 13–45 місць кожен.
- [ ] Додати CI-перевірку: `grep -rn "env(" app/` має повертати 0.

### 0.5 N+1 у Blade (mono-system)

- [ ] `mono-system/resources/views/print-ticket/index.blade.php:5–16` — `$ticket->trip->stations->where(...)->first()` у циклі. Винести `$ticket->load('trip.stations')` у контролері. Друк 100 квитків: 200+ запитів → 2.

---

## 📦 ФАЗА 1 — Перший composer-пакет (2 тижні)

### 1.1 `visson/liqpay-service`

- [ ] Порівняти md5 `app/Http/Controllers/LiqPay.php` у 9 проектах (очікується 100% ідентичність, ~264 рядки).
- [ ] Створити репо `VissOn/liqpay-service` з `src/LiqPayService.php`, `config/liqpay.php`, ServiceProvider.
- [ ] Тести (очікуваний callback, signature validation).
- [ ] Опублікувати як приватний пакет (Packagist Private або Satis).
- [ ] Підключити у **air-trans** (еталон) — видалити локальний `LiqPay.php`, `composer require visson/liqpay-service`.
- [ ] Розкатати послідовно: grosser → buktreck → mono-system → 3g → vts → bsystem → bustick-admin → padmin.

### 1.2 `visson/core-middleware`

- [ ] Порівняти md5 11 middleware між 5 проектами (підтверджено 100%).
- [ ] Список: `AuthCheck`, `Locale`, `ApiResponse`, `Cors`, тощо (уточнити з аудиту).
- [ ] Репо + ServiceProvider з `Route::aliasMiddleware(...)`.
- [ ] Розкатати аналогічно LiqPay.

---

## 🧹 ФАЗА 2 — Core cleanup (3 тижні)

### 2.1 Константи → PHP 8.1 Enums

- [ ] Проінвентаризувати `const STATUS_*/TYPE_*/CURRENCY_*/ROLE_*` у 9 проектах (є 26 файлів з `enum` проти тисяч констант).
- [ ] Почати з `visson/system-entities` — спільні Enums (TripStatus, TicketStatus, PaymentStatus, Currency).
- [ ] Поступовий переклад одного домена за раз.

### 2.2 Індекси БД (319 міграцій — 0 індексів)

- [ ] Створити міграцію `add_indexes_to_critical_tables` у кожному проекті:
  - `trips` — `[route_id, departure_at, status]`
  - `tickets` — `[trip_id, status]`, `[user_id, created_at]`
  - `orders` — `[user_id, status]`, `[created_at]`
  - FK колонки — обов'язково індекси.
- [ ] Запустити `EXPLAIN` на топ-5 повільних queries перед/після.

### 2.3 `visson/crud-kit`

- [ ] Витягти `app/Crud/Operations/*` (6 Operations: Copy, Export, Import, Filter, BulkEdit, …) у пакет.
- [ ] Витягти 5 Helper-трейтів.

### 2.4 `visson/helpers` + `visson/excel-exports`

- [ ] Витягти 2 ServiceProviders.
- [ ] Витягти Excel-експорти (maatwebsite patterns).

### 2.5 `@visson/ui-kit` (NPM)

- [ ] Витягти спільні Vue-компоненти (DataTable, Modal, форми Backpack).
- [ ] Починати одразу з Vue 3 + TypeScript (forward-compatible).

---

## 🏗 ФАЗА 3 — Per-project refactoring (6–10 тижнів)

### 3.1 God-файли (top-10)

| # | Файл | Проект | Дія |
|---|---|---|---|
| 1 | `ApplicationsCrudController.php` (2071) | buktreck | Розбити `setupListOperation` (680+), `setupCreateOperation` (450+), `setupUpdateOperation` на Actions + FieldDefinitions трейт (дублюють 48 полів тричі) |
| 2 | `resources/js/store/booking.js` (1732) | vts | Розпилити Vuex store → Pinia по доменах (bookings / search / cart / user) |
| 3 | `TripsCrudController.php` (1709) | 3g | Services: TripSearchService, TripImportService, TripSmsService |
| 4 | `TripsCrudController.php` (1256) | bsystem | Аналогічно після L7→L11 upgrade |
| 5 | `Trip.php` model (1188) | mono-system | Витягти QueryScopes, Observers, розділити на Trip + TripSchedule + TripFinance |
| 6 | `WidgetsController.php` (1179) | bsystem/3g | Actions per widget type |
| 7 | `TripsCrudController.php` (1151) | mono-system | (як у 3g) |
| 8 | `Trip.php` (1120) | vts | (як у mono-system) |
| 9 | `TripsCrudController.php` (1112) | bustick-admin | (як у 3g), після upgrade |
| 10 | `Trip.php` (1085) | 3g | (як у mono-system) |

### 3.2 Controllers >500 рядків (17 штук)

- [ ] Інвентаризувати повний список (є у звіті).
- [ ] Кожен → Service + Actions + Queries.

### 3.3 Busfor API (vts-специфіка)

- [ ] Витягти `vts/app/Services/Api/v1/Busfor/` (50+ маршрутів) → `visson/busfor-client` пакет.

### 3.4 Tests: від 0 до >30 на проект

- [ ] Видалити `ExampleTest`.
- [ ] Feature-тести для критичних flows: booking, payment, auth.
- [ ] Почати з air-trans (еталон), розкатати.

---

## 🚀 ФАЗА 4 — Legacy treks (паралельно)

### 4.1 bsystem — окремий upgrade-трек (3–4 тижні)

- [ ] L7 → L8 → L9 → L10 → L11 (обов'язково по одному major).
- [ ] PHP 7.2 → 8.2 (через 8.0, 8.1).
- [ ] 117 файлів у 6 API v1 модулях — тестові caveats.
- [ ] tenancy/tenancy v1 (274 файли) — окремо вирішити: видалити чи залишити.

### 4.2 padmin → merge у grosser

- [ ] Сценарій #2 (рекомендований): ~3–4 тижні.
- [ ] Перенести унікальну eCommerce-логіку padmin у grosser (L11, готова база).
- [ ] Архівувати `profumo-admin` репо.

### 4.3 bustick-admin — рішення власника

- [ ] Заморозити (sunset) АБО реактивувати (L9→L11, Vue 2→3, 8–12 тижнів).
- [ ] CopyOperation вже очищено (єдиний!), Vite 4 є — стартова позиція непогана.

### 4.4 8 legacy (gt-admin-new, bustrek, gt17, gt17admin, ats, v-admin-vue2, v-admin, santaopt)

- [ ] Підтвердити рішення: **заморозити** (ADR 2026-04-19).
- [ ] Відмітити у git: branch `archived`, README з датою заморозки.

---

## 🧪 ФАЗА 5 — Frontend modernization (паралельно, 4–6 тижнів)

### 5.1 Vue 2 → Vue 3 + Pinia + TypeScript

- [ ] bustick-admin (149+ компонентів) — першочергово, Vite 4 вже є.
- [ ] padmin (149 компонентів) — або merge у grosser.
- [ ] Vuex 3 → Pinia (3 stores у air-trans, 6 у bustick-admin, до 10 у vts).
- [ ] `@vitejs/plugin-vue2` → `@vitejs/plugin-vue`.

### 5.2 TypeScript для нових компонентів

- [ ] Налаштувати `tsconfig.json` + `vue-tsc` у `@visson/ui-kit`.
- [ ] Усі нові компоненти — `.vue` з `<script setup lang="ts">`.

---

## 📊 KPI та цільові метрики

| Метрика | Поточне | Ціль | Дедлайн |
|---|---:|---:|---|
| `dd()` / `var_dump()` у app/ | **24+** | 0 | Фаза 0 |
| `env()` поза config/ | 13–45/проект | 0 | Фаза 0–1 |
| Dead tenant-файлів | 200+ | 0 (крім vts) | Фаза 0 |
| Docker PHP version | 7.2 | 8.2+ | Фаза 0 |
| Індексів БД | 0 | 50+ | Фаза 2 |
| Controllers >500 рядків | 17 | 0 | Фаза 3 |
| Composer-пакетів visson/* | 0 | 5 | Фаза 2 |
| Feature-тестів (avg/проект) | ~0 | 30+ | Фаза 3 |
| TypeScript файлів | 0 | частково | Фаза 5 |
| Vue 3 + Pinia | 0/9 | 7/9 | Фаза 5 |

---

## 🎯 Швидкі рекомендації власнику

1. **Починай з Фази 0** — це 5–8 робочих днів на весь ecosystem, ризик мінімальний.
2. **`visson/liqpay-service` перший** — 100% ідентичний код, ідеальний тренажер для composer-процесу.
3. **air-trans як еталон** — все робимо спочатку там, потім розкатуємо.
4. **bsystem, padmin, bustick-admin** — рішення окремо, не змішувати з мейнстрімом.
5. **Не робити Фазу 3 без Фази 2** — god-файли легше різати, коли є `visson/crud-kit`.

---

## 🔗 Пов'язані нотатки

- [[project-overview|🗺 MOC: Visson Ecosystem]]
- [[sessions/2026-04-19-visson-audit|📋 Сесія аудиту 19.04.2026]]
- Звіт: `~/Source/outputs/Visson-Refactoring-Report-v2.docx`

## 📌 Відкриті питання

- [ ] Хто owner кожного legacy-проекту? Чи є заперечення проти заморозки?
- [ ] padmin merge у grosser — клієнт підтверджує?
- [ ] bustick-admin — заморозити чи реактивувати?
- [ ] bsystem upgrade чи fork-legacy?
