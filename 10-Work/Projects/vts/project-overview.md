---
title: "vts — VoltTransServis"
date: 2026-04-19
tags: [work, project, visson, laravel, vts]
category: work
project: vts
status: active
stack: ['Laravel 10', 'Vue 3', 'Vite', 'MySQL', 'Lottie', 'Docker']
pinecone_indexed: false
---

# vts — VoltTransServis

**Пріоритет:** 🔥 HIGH  
**Група:** A — активне ядро  
**Домен:** Transport services / trips / routes

## 🗺 Огляд

Гілка `api-busfor` нещодавно змерджена → інтеграція з busfor. Апгрейд L10→L11. Має Lottie-анімації — перевірити чи використовуються, інакше видалити.

## 🛠 Технічний стек

- **Laravel:** `^10.10`
- **PHP:** `^8.1`
- **Стек:** Laravel 10, Vue 3, Vite, MySQL, Lottie, Docker
- **Composer (top):** cviebrock/eloquent-sluggable, denostr/binotel-api, guzzlehttp/guzzle, intervention/image, kalnoy/nestedset
- **NPM (top):** @ckeditor/ckeditor5-vue, @lottiefiles/dotlottie-vue, @lottiefiles/dotlottie-web, @vitejs/plugin-vue, @vueform/multiselect
- **Docker:** так

## 📦 Репозиторій

- **Remote:** `git@github.com:VissOn/voltransservis-system.git`
- **Branch:** `dev`
- **Last commit:** 2026-04-01 (Merge branch 'api-busfor')

## 📊 Розмір

- **Файлів:** 1 391
- **Міграцій:** 115
- **Найбільші контролери:**
  - `TripsCrudController.php` — **977** рядків ⚠️
  - `RoutesCrudController.php` — **672** рядків

## 🎯 Рекомендовані дії

- [ ] АПГРЕЙД Laravel 10 → 11
- [ ] Перевірити Lottie-залежності на актуальність; видалити невикористані
- [ ] Індекси на trips/routes
- [ ] Міграція на visson/* (Фаза 3, тиждень 9–10)

## 🔧 Рефакторинг (2026-04-19)

> Нагадування: мульти-тенантності немає і не планується. VTS — **єдиний з аудитованих без tenant-заглушок** (найчистіший).

**Унікальне:** інтеграція **Busfor API** (`app/Services/Api/v1/Busfor/`, 50+ маршрутів, `ExternalAuthToken` middleware). VTS — партнер Busfor.

**Топ-5:** `Trip` model (1120), `TripsCrudController` (977), `RoutesCrudController` (672), `Route` model (609), `Ticket` model (562).

### 🔴 P1 — критично

- [ ] **`app/Crud/Operations/CopyOperation.php:53–54`** — `dd($e)` × 2 у production (Visson-core patern).
- [ ] **`error_log()` × 2 у production**:
  - `app/Services/Api/v1/Busfor/Http/Controllers/AuthController.php:59`
  - `app/Entities/System/Order.php:122`
  → `Log::error`. У `Order.php` — критично (потенційно legal/accounting).
- [ ] **`app/Http/Controllers/LiqPay.php` (264 рядки)** — винести у `Services/Payment/`.
- [ ] **`env()` поза config — 43 місця (рекорд серед проектів)**:
  - `app/Http/Middleware/AuthCheck.php:26–53` — env у middleware (виконується на кожному запиті!)
  - `app/Http/Controllers/Api/Auth/LoginController.php:69–70`
  - `app/Crud/Operations/SendTicketSmsOperation.php:54–79` — AlphaSms keys
  → `config/services.php`.
- [ ] **`docker/web/Dockerfile` — PHP 7.2** vs composer `^8.1`. → `php:8.2-apache`.

### 🟡 P2 — важливо

- [ ] **God-models**:
  - `Trip.php` — **1120 рядків, 81 метод**.
  - `Route.php` — **609 рядків, 60+ методів**.
  - `Ticket.php` — **562 рядки, 70+ методів**.
  → Service + Query + Actions, особливо `Trip`.
- [ ] **God-controllers**: `TripsCrudController` 977, `RoutesCrudController` 672, `BookingController` 499, `DriversCrudController` 482, `TicketsCrudController` 394.
- [ ] **`resources/js/store/booking.js` — 1732 рядки** (!). Frontend god-store, сам більший за більшість backend-моделей. → Pinia-stores: `booking-list`, `booking-form`, `booking-payment`, `booking-route-selection`.
- [ ] **Vuex 4 → Pinia**; TypeScript відсутній (310 `.js/.vue`, 0 `.ts`).
- [ ] **~1637 однорядкових `//` коментарів** + закоментовані блоки в Mail-класах.
- [ ] **`const STATUS_*/TYPE_*` у `Trip`/`Route`/`Ticket`** → PHP 8.1 Enums.
- [ ] **Tests — тільки `ExampleTest`**. Критично через Busfor-інтеграцію (external API → регрес при upgrade).

### 🟢 P3 — nice to have

- [ ] **`composer.json: denostr/binotel-api:^0.1.3`** — не використовується в коді. → видалити (зайвий security-surface).
- [ ] **Busfor-інтеграція** → кандидат на composer-пакет `visson/busfor-client` для перевикористання.
- [ ] **Print-ticket: 2 варіанти** (`index.blade.php` + `index-new.blade.php`). N+1 тільки на `contact_phone`. → визначити основний, видалити інший.
- [ ] **9 Mailable**, 0 Notifications, 0 Exports. → `AbstractVtsMail` + Export для звітів.
- [ ] **Lottie** — перевірити чи використовується, інакше видалити.

### ✅ Сильні сторони vts

- **Немає tenant-заглушок** (`database/tenant/`, `ConfigureTenantConnection` — відсутні).
- **7 Observers + 7 Scopes** — добра domain-логіка.
- **Services: `BookingService` (265), `TripsService` (265)** — існують, розумний розмір.
- **14 Jobs** — queue реально використовується.
- **54 FK-індекси у міграціях** — кращий показник серед аудитованих.

### ❓ Відкриті питання

- [ ] **Busfor-інтеграція** — виокремити в `visson/busfor-client` зараз чи після стабілізації?
- [ ] **`index-new.blade.php`** — нова версія print-ticket чи dead A/B?
- [ ] **`denostr/binotel-api`** — видаляємо зараз?

### 📊 Target-метрики

- `Trip` model **< 300** (зараз 1120)
- `booking.js` **< 300** (зараз 1732 — **-82%**)
- 0 `dd()` / `error_log()` / `env()` поза config
- Тестів: **>20**, включно з Busfor-mocks

## 🔗 Пов'язані нотатки

- [[visson-ecosystem/project-overview|🗺 MOC: Visson Ecosystem]]
- [[visson-ecosystem/sessions/2026-04-19-visson-audit|📋 Аудит 19.04.2026]]
- [[air-trans/project-overview|air-trans]]
- [[grosser/project-overview|grosser]]
- [[buktreck/project-overview|buktreck]]
- [[3g/project-overview|3g]]
- [[mono-system/project-overview|mono-system]]

## 📌 Відкриті питання

- [ ] 
