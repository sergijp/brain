---
title: "buktreck — Buktrek / управління перевезеннями"
date: 2026-04-19
tags: [work, project, visson, laravel, buktreck]
category: work
project: buktreck
status: active
stack: ['Laravel 11', 'Vue 3', 'Vite', 'MySQL', 'Docker']
pinecone_indexed: false
---

# buktreck — Buktrek / управління перевезеннями

**Пріоритет:** 🔥 HIGH  
**Група:** A — активне ядро  
**Домен:** Bus logistics / transport management

## 🗺 Огляд

⚠️ КРИТИЧНО: ApplicationsCrudController.php — **2 071 рядок**, найбільший моноліт у вибірці. Потребує розбивки на сервіси/Actions у першу чергу.

## 🛠 Технічний стек

- **Laravel:** `^11.0`
- **PHP:** `^8.2`
- **Стек:** Laravel 11, Vue 3, Vite, MySQL, Docker
- **Composer (top):** cviebrock/eloquent-sluggable, guzzlehttp/guzzle, intervention/image, kalnoy/nestedset, lcobucci/jwt
- **NPM (top):** @vitejs/plugin-vue, @vueform/multiselect, @vuelidate/core, @vuelidate/validators, bootstrap
- **Docker:** так

## 📦 Репозиторій

- **Remote:** `git@github.com:VissOn/buktrack.git`
- **Branch:** `dev`
- **Last commit:** 2026-03-18

## 📊 Розмір

- **Файлів:** 1 275
- **Міграцій:** 78
- **Найбільші контролери:**
  - `ApplicationsCrudController.php` — **2071** рядків ⚠️
  - `CarriersCrudController.php` — **392** рядків

## 🎯 Рекомендовані дії

- [ ] РОЗБИТИ ApplicationsCrudController → ApplicationsController + ApplicationsService + 15–20 Action-класів
- [ ] Міграція на visson/* (Фаза 3, тиждень 7–8)
- [ ] Додати індекси: applications(status, carrier_id, created_at)

## 🔧 Рефакторинг (2026-04-19)

> Нагадування: мульти-тенантності немає і не планується. Tenant-код у проекті — dead, видалити.

**Топ-5 найбільших файлів:** `ApplicationsCrudController` (2071), `Application` model (416), `CarriersCrudController` (392), `DriversCrudController` (377), `AlphaSms` (245).

### 🔴 P1 — критично

- [ ] **`ApplicationsCrudController.php` — 2071 рядок, 27 методів, 7 traits** (!). Розбиття:
  - `setupListOperation()` L80 — **680+ рядків**, 48 інлайн-полів
  - `setupCreateOperation()` L762 — **450+ рядків**, ті самі 48 полів вдруге
  - `setupUpdateOperation()` L1211 — ще раз дублюються
  - `createContract()` L1996, `getConfigData()` L1857, PDF-логіка L2040 — бізнес-логіка в контролері
  → винести у `ApplicationFieldsConfig`, `CreateContractAction`, `ApplicationPdfService`.
- [ ] **`docker/web/Dockerfile:1` — PHP 7.2** vs `composer.json` `^8.2`. → `php:8.3-apache`.
- [ ] **`app/Http/Controllers/LiqPay.php` (264 рядки)** — не контролер, інтеграція. → `app/Services/Payment/LiqPayService.php`.
- [ ] **`dd()` у production (4 місця)**:
  - `Api/Auth/LoginController.php:112` — `dd(1);`
  - `Crud/Operations/CopyOperation.php:53–54` — `dd($e)` ×2
  - `Console/Commands/UpdateUsers.php:55` — `dd($e->getMessage())`
- [ ] **`env()` поза `config/`**:
  - `Api/Auth/LoginController.php:49–50` — `env('CLIENT_ID')`, `env('CLIENT_SECRET')`
  - `Listeners/Tenant/ConfigureTenantConnection.php:22–23` — `env('DB_USERNAME')`, `env('DB_PASSWORD')`
  → `config('oauth.*')`.

### 🟡 P2 — важливо

- [ ] **`app/Entities/System/Content/Application.php` — 416 рядків, 41 метод**, 16 `STATUS_*` констант (L36–51). → `ApplicationService` + `ApplicationStateMachine` + `enum ApplicationStatus: string`.
- [ ] **`config/crud.php` — конфіги статусів/брокерів/типів inline**, 100+ рядків лише для `applications.status` (L9–78+). → клас-конфіг або enum.
- [ ] **Dead code — 6+ `// dd($...)` коментарів** у `ApplicationsCrudController.php` (L1241, 1341, 1519, 1784), коментований config `amount_application` L805–812. → видалити.
- [ ] **`app/Services/AppApi/Controllers/`** — Controllers у `Services/` (`MemberController` 416 рядків, `AuthController` 154). → перенести в `Http/Controllers/AppApi/` або перейменувати.
- [ ] **Vuex 4 → Pinia**, 7 stores. TypeScript відсутній (0 `.ts`).
- [ ] **16 Mailable** — перевірити дублікати, ввести `AbstractBuktreckMail`.
- [ ] **87 міграцій** — додати індекси на FK (pattern проекту: індексів немає).

### 🟢 P3 — nice to have

- [ ] **Tenant-код мертвий**: `config/tenancy.php`, `app/Listeners/Tenant/` (5 файлів), `database/tenant/migrations/` (9 файлів), `database/tenant/seeders/` (4 файли). → **видалити повністю** або в `legacy/`.
- [ ] **Tests — тільки `ExampleTest`** (71 рядок). 0 покриття `Applications`, `LiqPay`, `Auth`.
- [ ] **`app/Services/` — 43 файли плоско**, без групування. → `Payment/`, `Export/`, `Sms/`, `Pdf/`.
- [ ] **`const TYPE_*` у `Member.php:41–46`, `const CURRENCY_*` у `LiqPay.php:32–36`** → Enums.
- [ ] **Routes компактні** — `web.php` 13 рядків, `api.php` 158. OK.

### 📊 Target-метрики

- `ApplicationsCrudController` **< 300 рядків** (зараз 2071 — **-85%**)
- `Application` model **< 200** (зараз 416)
- 0 `dd()` / `env()` поза `config/` / tenant-коду
- Тестів: **>30** (зараз 0 реальних)

## 🔗 Пов'язані нотатки

- [[visson-ecosystem/project-overview|🗺 MOC: Visson Ecosystem]]
- [[visson-ecosystem/sessions/2026-04-19-visson-audit|📋 Аудит 19.04.2026]]
- [[air-trans/project-overview|air-trans]]
- [[grosser/project-overview|grosser]]
- [[3g/project-overview|3g]]
- [[mono-system/project-overview|mono-system]]
- [[vts/project-overview|vts]]

## 📌 Відкриті питання

- [ ] 
