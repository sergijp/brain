---
title: "mono-system — MONOBUS автобусні перевезення"
date: 2026-04-19
tags: [work, project, visson, laravel, mono-system]
category: work
project: mono-system
status: active
stack: ['Laravel 10', 'Vue 3', 'Vite', 'MySQL', 'CKEditor 5', 'Docker']
pinecone_indexed: false
---

# mono-system — MONOBUS автобусні перевезення

**Пріоритет:** 🔥 HIGH  
**Група:** A — активне ядро  
**Домен:** Bus logistics / trips / routes

## 🗺 Огляд

N+1 у `resources/views/print-ticket/index.blade.php:5` — `$ticket->trip->stations->where(...)->first()` без eager load. 450 MB node_modules, найбільший у групі. Апгрейд L10→L11 перед міграцією.

## 🛠 Технічний стек

- **Laravel:** `^10.10`
- **PHP:** `^8.1`
- **Стек:** Laravel 10, Vue 3, Vite, MySQL, CKEditor 5, Docker
- **Composer (top):** cviebrock/eloquent-sluggable, guzzlehttp/guzzle, intervention/image, kalnoy/nestedset, lcobucci/jwt
- **NPM (top):** @ckeditor/ckeditor5-vue, @vitejs/plugin-vue, @vuelidate/core, @vuelidate/validators, @vuepic/vue-datepicker
- **Docker:** так

## 📦 Репозиторій

- **Remote:** `git@github.com:VissOn/mono-system.git`
- **Branch:** `master`
- **Last commit:** 2026-02-02

## 📊 Розмір

- **Файлів:** 1 454
- **Міграцій:** 123
- **Найбільші контролери:**
  - `TripsCrudController.php` — **1151** рядків ⚠️
  - `RoutesCrudController.php` — **749** рядків ⚠️

## 🎯 Рекомендовані дії

- [ ] ВИПРАВИТИ N+1 у print-ticket Blade — передавати `$ticket->load('trip.stations')` з контролера
- [ ] АПГРЕЙД Laravel 10 → 11
- [ ] Розбити TripsCrudController
- [ ] Lazy-load routes + manualChunks для CKEditor
- [ ] v-admin-vue2 функціонал поглинути сюди (див. v-admin-vue2)

## 🔧 Рефакторинг (2026-04-19)

> Нагадування: мульти-тенантності немає і не планується. `app/Entities/Tenant/*` — це лише нейм-конвенція (треба підтвердити та прибрати "Tenant" з шляху).

**Топ файли:** `Trip` model (1188), `TripsCrudController` (1151), `RoutesCrudController` (749), `Ticket` model (689), `DriversCrudController` (551), `TripsDispatcherCrudController` (522), `TicketsCrudController` (492).

### 🔴 P1 — критично

- [ ] **`docker/web/Dockerfile:1` — PHP 7.2** vs composer `^8.1`. → `php:8.2-apache`.
- [ ] **`app/Crud/Operations/CopyOperation.php:53–54` — `dd($e)` + `dd($e->getMessage())` у production** (типовий Visson-core патерн). → `Log::error` + graceful fallback.
- [ ] **N+1 у `resources/views/print-ticket/index.blade.php:5–16`**:
  - L5–6: `$ticket->trip->stations->where(...)->first()` — 2+ запити на record у циклі.
  - L8–16: додаткові method-calls без кешування.
  → eager-load у `TicketController::print()`: `Ticket::with(['trip.stations','client','route'])`.
- [ ] **`app/Http/Controllers/LiqPay.php`** — платіжка в Controllers. → `app/Services/Payment/LiqPayService.php`.
- [ ] **God-models**:
  - `app/Entities/Tenant/Trip.php` — **1188 рядків, 110+ методів**. → `TripService`, `TripQuery`, Value Objects, Actions.
  - `app/Entities/Tenant/Ticket.php` — **689 рядків, 82 методи**. → аналогічно.
- [ ] **God-controllers (>500)**: `TripsCrudController` 1151, `RoutesCrudController` 749, `DriversCrudController` 551, `TripsDispatcherCrudController` 522. → Services + Actions + FieldConfigs.

### 🟡 P2 — важливо

- [ ] **`env()` у 28 файлах `app/`** — масштабне порушення 12-factor, `config:cache` ламається. → `config/services.php`, `config/app.php`.
- [ ] **Dead code у `TripsCrudController.php` L700, L730, L1024** — закоментовані `with()`. → видалити.
- [ ] **`Trip.php:110–113` — `const STATUS_*`** → `enum TripStatus: string`.
- [ ] **Vue 3 + Vuex 4** замість Pinia. Немає TypeScript.
- [ ] **Tests — 3 `ExampleTest.php`**, 534 `app/` файли без покриття. → Feature-тести на `TripsCrudController`, `print-ticket`, `LiqPay`.
- [ ] **0 Actions, 0 Notifications, 0 Exports класів** — логіка в контролерах і моделях. → ввести `app/Actions/`, `app/Notifications/`, `app/Exports/`.
- [ ] **450 MB `node_modules`** — найбільший у екосистемі. Перевірити зайві залежності. → `npm dedupe` + аудит `@ckeditor/*`.

### 🟢 P3 — nice to have

- [ ] **123 міграції з індексами на FK** — перевірити дублі (unique vs index).
- [ ] **`Entities/Tenant/*`** — перейменувати в `Entities/Core/` або `Entities/`. Назва плутає з tenancy.
- [ ] **34 Jobs** — queue використовується. Перевірити Redis-connection + `failed_jobs` моніторинг.
- [ ] **16 Mailable** — ввести `AbstractMonoMail` зі спільним layout.

### ❓ Відкриті питання

- [ ] **`Entities/Tenant/*`** — dead tenancy convention чи реально використовується? Від цього залежить область рефакторингу.
- [ ] **`app/Services/` (4 файли)** — які саме? Чи є вже `AlphaSmsService`/`LiqPayService` (тоді `LiqPay.php` у Controllers — дубль)?

### 📊 Target-метрики

- `Trip` model **< 300** (зараз 1188 — **-75%**)
- `TripsCrudController` **< 300** (зараз 1151)
- 0 `dd()` / 0 `env()` поза config
- N+1 видалити з усіх `print-*` і `report-*` Blade
- Тестів: **>25**

## 🔗 Пов'язані нотатки

- [[visson-ecosystem/project-overview|🗺 MOC: Visson Ecosystem]]
- [[visson-ecosystem/sessions/2026-04-19-visson-audit|📋 Аудит 19.04.2026]]
- [[air-trans/project-overview|air-trans]]
- [[grosser/project-overview|grosser]]
- [[buktreck/project-overview|buktreck]]
- [[3g/project-overview|3g]]
- [[vts/project-overview|vts]]

## 📌 Відкриті питання

- [ ] 
