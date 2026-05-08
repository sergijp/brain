---
title: "3g — 3G-SITE клієнтський портал"
date: 2026-04-19
tags: [3g, work, project, visson, laravel]
category: project
project: 3g
status: active
stack: ['Laravel 10', 'Vue 3', 'Vite', 'MySQL', 'Docker', 'Binotel']
aliases: ["3g-overview", "3g-project"]
pinecone_indexed: false
---

# 3g — 3G-SITE клієнтський портал

**Пріоритет:** 🔥 HIGH  
**Група:** A — активне ядро  
**Домен:** Transport routes / trips / logistics

## 🗺 Огляд

⚠️ TripsCrudController.php = 1 709 рядків, 36 методів. WidgetsController.php = 1 154. Два з найбільших файлів усієї екосистеми. Апгрейд L10→L11 перед міграцією на пакети.

## 🛠 Технічний стек

- **Laravel:** `^10.10`
- **PHP:** `^8.1`
- **Стек:** Laravel 10, Vue 3, Vite, MySQL, Docker, Binotel
- **Composer (top):** cviebrock/eloquent-sluggable, denostr/binotel-api, guzzlehttp/guzzle, intervention/image, kalnoy/nestedset
- **NPM (top):** @adesin-fr/vue-ganttastic, @ckeditor/ckeditor5-vue, @vitejs/plugin-vue, @vueform/multiselect, @vuelidate/core
- **Docker:** так

## 📦 Репозиторій

- **Remote:** `git@github.com:VissOn/3g-site.git`
- **Branch:** `dev-demo`
- **Last commit:** 2026-03-30

## 📊 Розмір

- **Файлів:** 1 529
- **Міграцій:** 116
- **Найбільші контролери:**
  - `TripsCrudController.php` — **1709** рядків ⚠️
  - `WidgetsController.php` — **1154** рядків ⚠️

## 🎯 Рекомендовані дії

- [ ] АПГРЕЙД Laravel 10 → 11 (паралельно з міграцією на пакети)
- [ ] Розбити TripsCrudController на TripsController + TripService + 10–15 Actions
- [ ] Розбити WidgetsController на окремі Report-класи
- [ ] Eager loading у TripsCrudController рядки 265, 325, 974–978
- [ ] Індекси: trips(created_at, status), tickets(trip_id, status)

## 🔧 Рефакторинг (2026-04-19)

> Нагадування: мульти-тенантності немає і не планується. Tenant-інфра в коді — dead code, видалити.

**Топ-5:** `TripsCrudController` (1709), `WidgetsController` (1154), `Trip` model (1085), `RoutesCrudController` (713), `Ticket` model (673).

### 🔴 P1 — критично

- [ ] **`TripsCrudController.php` (1709 рядків)**:
  - `dd($e->getMessage())` у catch-блоках **у production** (район L1540): `cancelTrip`, `tripUpdate`, `closeTrip`, `uncloseTrip`. → `Log::error` + graceful response.
  - **Дубль SMS-логіки**: `sendAllSms()` L261–319 vs `sendSmsMessage()` L321–376 — ~55 рядків майже ідентичних. → один `SendTripSmsAction` з параметрами.
  - `reportDriver()` L1059–1210 (152 рядки) + dead duplicate discount-блок L1103–1115 vs активний L1116–1138. → `DriverDiscountReportService`.
  - **`env()` поза config — 20+ вхождень**: L268, L329, L316–317, L1358, L1361, L1427–1428 (AlphaSms, PortMone keys). → `config/services.php`.
  - Закоментований блок L590–616 (26 рядків — старе `bus_id`/`carrier_id`). → видалити.
- [ ] **`app/Http/Controllers/LiqPay.php`** (7.3K) — платіжний клас у Controllers. → `app/Services/Payment/LiqPayService.php`.
- [ ] **`app/Http/Controllers/WidgetsController.php` (1154 рядки)** — god-controller віджетів/звітів. → розбити за типом віджета в `Services/Widgets/*` або `Actions/Reports/*`.
- [ ] **`docker/**/Dockerfile` — PHP 7.2** vs composer `^8.1`. → `php:8.2-apache` (і апгрейд PHP на 8.2+).
- [ ] **`Crud/Operations/CopyOperation.php`** — 2× `dd()` (типовий патерн Visson-core, повторюється з air-trans/grosser/buktreck). → `Log::error`.

### 🟡 P2 — важливо

- [ ] **`Trip.php` (1085 рядків) — god-model**. Константи `STATUS_ACTIVE`, `STATUS_CANCELLED`, `TYPE_DIRECTION_FROM/TO`. → `TripService`, `TripQuery`, `enum TripStatus`, `enum TripDirection`.
- [ ] **`Ticket.php` (673 рядки)** — логіка розподілу дисконтів → `DistributeDiscountAction`.
- [ ] **`Route.php` (546 рядків)** — `TYPE_EVERY_DAY`, `TYPE_EVEN`, `TYPE_ODD` → `enum RouteScheduleType`.
- [ ] **`WalletBalance`** — 8+ констант → Enums.
- [ ] **Vuex → Pinia** + TypeScript (0 `.ts` файлів).
- [ ] **`RoutesCrudController` (713 рядків)** — такий самий патерн роздутого CRUD.
- [ ] **0 реальних тестів** — 2 `ExampleTest` заглушки, 125 міграцій без покриття. → integration-тести для `TripsCrudController`, `LiqPay`, `AlphaSms`.

### 🟢 P3 — nice to have

- [ ] **Dead tenant-код**: `database/tenant/migrations/` (9 файлів), `database/tenant/seeders/`, `ConfigureTenantConnection`. → **видалити**.
- [ ] **`routes/api.php` — 600 рядків без версіонування**. → `prefix('api/v1')` + поділ на файли за доменом.
- [ ] **`app/Services/Api/v1/{Busfor,External,GlobalApi,PrivatBank}/`** — надто глибока вкладеність. → `app/Services/Integrations/{Busfor,PrivatBank,...}`.
- [ ] **FK-cascade** — індекси є, але поведінка (delete/update) не перевірена.

### ❓ Відкриті питання

- [ ] **`WidgetsController` (1154)** — це фіча-панель чи acummulated garbage? Від відповіді — розбиваємо чи викидаємо.
- [ ] **`app/Services/Api/v1/PrivatBank/`** — використовується в проді чи експеримент?

### 📊 Target-метрики

- `TripsCrudController` **< 300 рядків** (зараз 1709 — **-82%**)
- `WidgetsController` **< 300** (зараз 1154)
- `Trip` model **< 250** (зараз 1085)
- 0 `dd()` / `env()` поза config / tenant-коду
- Тестів: **>25**

## 🔗 Пов'язані нотатки

- [[visson-ecosystem/project-overview|🗺 MOC: Visson Ecosystem]]
- [[visson-ecosystem/sessions/2026-04-19-visson-audit|📋 Аудит 19.04.2026]]
- [[air-trans/project-overview|air-trans]]
- [[grosser/project-overview|grosser]]
- [[buktreck/project-overview|buktreck]]
- [[mono-system/project-overview|mono-system]]
- [[vts/project-overview|vts]]

## 📌 Відкриті питання

- [ ] 
