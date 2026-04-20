---
title: "bsystem — Bustrek legacy (база Visson L7)"
date: 2026-04-19
tags: [work, project, visson, laravel, bsystem]
category: work
project: bsystem
status: active
stack: ['Laravel 7', 'PHP 7.2', 'Vue 2', 'Webpack', 'MySQL', 'apexcharts', 'Docker', 'TurboSMS']
pinecone_indexed: false
---

# bsystem — Bustrek legacy (база Visson L7)

**Пріоритет:** ⚠️ RISK L7  
**Група:** A — активне ядро (legacy stack)  
**Домен:** Bus routes / trips / transport

## 🗺 Огляд

⚠️ Laravel 7 + PHP 7.2 — КРИТИЧНО застарілий стек (EOL). Але проект активно розробляється (останній commit 02/2026). Рішення потрібне: апгрейд до L11 (2+ тижні) vs форк як окреме legacy і зупинка нових фіч.

## 🛠 Технічний стек

- **Laravel:** `^7.0`
- **PHP:** `^7.2`
- **Стек:** Laravel 7, PHP 7.2, Vue 2, Webpack, MySQL, apexcharts, Docker, TurboSMS
- **Composer (top):** daaner/turbosms, fideloper/proxy, guzzlehttp/guzzle, intervention/image, lcobucci/jwt
- **NPM (top):** apexcharts, bootstrap, chart.js, laravel-echo, moment
- **Docker:** так

## 📦 Репозиторій

- **Remote:** `git@github.com:VissOn/bustrek.git`
- **Branch:** `bus_transfer`
- **Last commit:** 2026-02-02

## 📊 Розмір

- **Файлів:** 1 258
- **Міграцій:** 22
- **Найбільші контролери:**
  - `TripsCrudController.php` — **1204** рядків ⚠️
  - `WidgetsController.php` — **1179** рядків ⚠️

## 🎯 Рекомендовані дії

- [ ] 🚨 ПРИЙНЯТИ РІШЕННЯ: апгрейд L7→L11 vs заморозка
- [ ] Якщо апгрейд: окремий трек, не заходить у Фазу 2 ядра до завершення
- [ ] PHP 7.2 → 8.2 (обов'язково, EOL)
- [ ] Webpack → Vite; Vue 2 → Vue 3
- [ ] Розбити TripsCrudController (1204) і WidgetsController (1179)

## 🔧 Рефакторинг (2026-04-19) — СТРАТЕГІЧНИЙ

> Нагадування: мульти-тенантності немає і не планується. **Tenancy v1 використовується для ідентифікації в 274 файлах — треба підтвердити чи це dead code.**

### ⚠️ Критичний контекст

- Laravel 7 — **EOL з березня 2021** (5 років без security fixes).
- PHP 7.2 — **EOL з травня 2020**.
- Vue 2.6.11 — **EOL з грудня 2023**.
- Але: **останній commit 7 днів тому** — проект активно розробляється на мертвому стеку.
- **117 файлів доменної логіки** (6 API v1 модулів: GlobalApi, App, General, PrivatBank, Reports, DataExchange) — rewrite = роки.
- **4 тести** на 3742 LoC — катастрофічно низько.

### ✅ Рекомендація: UPGRADE → L11 (не rewrite, не freeze)

**Причини:** активна розробка + 117 файлів унікальної домен-логіки + 26 Jobs + event-driven архітектура = upgrade вигідніший.

### 📅 Roadmap (≈3–4 тижні + 1 тиждень QA)

| Крок | Час | Головне |
|---|---|---|
| **Підготовка** | тиждень 1 | Витягти god-controllers у Services, покрити API тестами |
| **L7 → L8** | 2–3 дні | Jobs, factories, guzzle 7, PHP 7.4+ |
| **L8 → L9** | 5–7 днів | Symfony 6, Flysystem 3, tenancy v1 → Spatie/multitenancy, Passport ^10, Spatie/permission ^5, PHP 8.0+ |
| **L9 → L10** | 2–3 дні | PHP 8.1, нативні типи |
| **L10 → L11** | 3–5 днів | PHP 8.2, `bootstrap/app.php`, видалення Kernels |
| **Frontend** | паралельно | Vue 2 → Vue 3 + Vite + Pinia + TypeScript |

### 🚧 Upgrade blockers

- `composer.json:17` — `guzzlehttp/guzzle: ^6.3` → потрібно `^7.0` (L9).
- `composer.json:24` — `lcobucci/jwt: 3.3.3` (pinned) → `^4.0` (breaking API).
- `composer.json:30` — `tenancy/tenancy: ^1.0` → на L7 only, треба мігрувати на Spatie або видалити.
- **Passport v9.3** → `^11` для L10/11.
- **Spatie/permission v3.17** → `^5` для L10/11.
- `app/Http/Kernel.php:33–42` — кастомний `$middlewarePriority` з 6+ токен-middleware.
- `app/Providers/RouteServiceProvider.php:35–63` — кастомний `Route::crud()` макрос на L7 Router API.
- **Vue 2.6.11** — EOL.

### 🔴 P1 — критично (блокує upgrade)

- [ ] **Витягти бізнес-логіку з god-controllers у Services** (pre-upgrade):
  - `app/Http/Controllers/Api/Crud/TripsCrudController.php` — **1256 рядків** (booking-логіка inline)
  - `app/Http/Controllers/WidgetsController.php` — **1179 рядків** (dashboard aggregation)
  - `app/Http/Controllers/Api/Crud/RoutesCrudController.php` — **727 рядків**
  Інакше atomic migration неможлива.
- [ ] **Tenancy v1 → Spatie/multitenancy v4** — або **видалити повністю** (за правилом тенантів немає). Це **найбільший блокер** upgrade.
- [ ] **Покрити API-endpoints тестами** (PHPUnit/Pest). Зараз 4 файли — регрес при upgrade гарантований. → **>50 Feature тестів** перед L7→L8.
- [ ] **`dd()`/`var_dump()` у production — 45 місць** у `app/` (+ 700 у vendor). → pre-commit hook + санітизація.
- [ ] **`env()` — 45 місць поза `config/`**. → `config/services.php`.

### 🟡 P2 — важливо

- [ ] **Passport v9 → `^11`** проактивно.
- [ ] **Spatie/permission v3 → `^5`** (breaking changes у namespace).
- [ ] **Vue 2 → Vue 3 + Pinia + TypeScript + Vite** (паралельний трек, не блокує backend upgrade).
- [ ] **`Entities/Tenant/`** — якщо tenancy не використовується, видалити/перейменувати на `Entities/Core/`.
- [ ] **`app/Http/Controllers/LiqPay.php`** (якщо є) → `Services/Payment/`.
- [ ] **Event-driven архітектура — задокументувати зв'язки** (10 Events / 6 Listeners). Інакше upgrade ламатиме тенях.
- [ ] **`app/Providers/RouteServiceProvider.php` — кастомний `Route::crud()` макрос** — переоформити під L11 Router API.

### 🟢 P3 — nice to have

- [ ] Webpack 4 → Vite.
- [ ] Horizon для моніторингу 26 Jobs.
- [ ] **PrivatBank-інтеграцію** виокремити в `visson/privatbank-client` composer-пакет.
- [ ] `chart.js` + `apexcharts` одночасно — обрати один.

### ❓ Критичні відкриті питання

- [ ] **Tenancy v1 — реально використовується чи dead code?** 274 файли залежностей. Якщо dead — видалити перед upgrade (кардинально спрощує L7→L8).
- [ ] **PrivatBank** — прямий платіжний шлюз — чи можна знести на час upgrade? Ризик для платіжних рейлів.
- [ ] **API v1 (6 модулів, 117 файлів)** — усі 6 реально використовуються зараз, чи щось заморозилося (`DataExchange`, `Reports`)?
- [ ] **Branch `bus_transfer`** — що це? Main гілка? Окрема фіча?

### 📊 Target-метрики (after upgrade)

- Laravel **11.x**, PHP **8.2+**
- Tests — **>50 Feature** (зараз 4)
- God-controllers **< 300 рядків** (зараз 1256, 1179, 727)
- 0 `dd()` / `env()` поза `config/`
- Tenancy v1 — **видалена** або мігрована на Spatie/multitenancy v4
- Vue 3 + Pinia + TypeScript + Vite

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
