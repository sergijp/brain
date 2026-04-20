---
title: "grosser — Visson портал (e-commerce)"
date: 2026-04-19
tags: [work, project, visson, laravel, grosser]
category: work
project: grosser
status: active
stack: ['Laravel 11', 'Vue 3', 'Vite', 'MySQL', 'Docker']
pinecone_indexed: false
---

# grosser — Visson портал (e-commerce)

**Пріоритет:** 🔥 HIGH  
**Група:** A — активне ядро  
**Домен:** E-commerce / продукти / каталог

## 🗺 Огляд

Laravel 11 + e-commerce домен. Після air-trans — другий кандидат на міграцію (тиждень 7–8).

## 🛠 Технічний стек

- **Laravel:** `^11.0`
- **PHP:** `^8.2`
- **Стек:** Laravel 11, Vue 3, Vite, MySQL, Docker
- **Composer (top):** cviebrock/eloquent-sluggable, guzzlehttp/guzzle, intervention/image, kalnoy/nestedset, lcobucci/jwt
- **NPM (top):** @vitejs/plugin-vue, @vuelidate/core, @vuelidate/validators, bootstrap, click-outside-vue3
- **Docker:** так

## 📦 Репозиторій

- **Remote:** `git@github.com:VissOn/grosser.git`
- **Branch:** `main`
- **Last commit:** 2026-02-18

## 📊 Розмір

- **Файлів:** 1 218
- **Міграцій:** 50
- **Найбільші контролери:**
  - `ProductCrudController.php` — **317** рядків
  - `LiqPay.php` — **264** рядків

## 🎯 Рекомендовані дії

- [ ] Міграція на visson/* (Фаза 3, тиждень 7)
- [ ] Індекси на products(active, sort), orders(status, created_at)
- [ ] Lazy-load Vue routes

## 🔧 Рефакторинг (2026-04-19)

> Нагадування: мульти-тенантності немає і не планується. Tenant-заглушки у коді = dead code, видалити.

### 🔴 P1 — критично

- [ ] **`docker/web/Dockerfile:1` — PHP 7.2** vs `composer.json` `^8.2`. Контейнер не піднімає актуальний код. → `FROM php:8.3-apache`.
- [ ] **`app/Http/Controllers/LiqPay.php:30` (264 рядки)** — клас `LiqPay` у Controllers, не наслідує Controller. Старий стиль (`const CURRENCY_EUR`, приватні `$_keys`). → `app/Services/Payment/LiqPayService.php` + DI.
- [ ] **`env()` поза `config/` (3+ місця)**:
  - `app/Http/Resources/Profile/OrderProductResource.php` — `env('APP_URL')` ×3
  - `app/Http/Controllers/Api/Auth/LoginController.php` — `env('CLIENT_ID')`, `env('CLIENT_SECRET')`
  - `app/Services/ApiService.php` — `env('API_TOKEN')`, `env('API_LINK')`
  → винести у `config/services.php`. `config:cache` зараз ламає все.
- [ ] **`app/Entities/System/Directories/Route.php:70–468` — god-model 468 рядків**. 12+ scopes, 15+ relations, business logic (`createTrip`, `checkParentTrip`). Dead code L247–260 (закоментовані scopes). → Actions (`CreateTripAction`), QueryBuilders, Events.
- [ ] **`app/Entities/System/Catalog/Product.php:50–325` — god-model 325 рядків**. 8 traits. Currency-логіка (`getPriceConverted`, `getPriceOldConverted`, `getPriceCrossed`) + запити (`getAvailableAttributes`). → ValueObject `Price`, `PriceConverter` service.

### 🟡 P2 — важливо

- [ ] **`app/Crud/Operations/CopyOperation.php:53–54` — `dd($e)`, `dd($e->getMessage())` у production**. Білий екран при будь-якій помилці копіювання. → `Log::error` + graceful fallback.
- [ ] **CRUD Controllers роздуті (>200 рядків)**:
  - `Api/Crud/Catalog/ProductCrudController.php` — 317
  - `Api/Crud/Shop/OrderCrudController.php` — 214
  - `Api/Crud/WebsiteInfoCrudController.php` — 211
  Причина: немає Service/Action шару.
- [ ] **Service-шар майже відсутній** — лише `ApiService`, `CheckoutService`. 62 CRUD-файли тримають логіку in-place. → додати `Payment/`, `Export/`, `Notification/`, `Import/` Services.
- [ ] **Vue 3 + Vuex 4** замість Pinia. 6 stores. → Pinia + TypeScript для нових.
- [ ] **Старі string-константи замість Enums**:
  - `Route.php:76–100` — `const TYPE_*`, `CURRENCY_*`, `ROUND_PRICE_*`
  - `LiqPay.php:32–36` — `const CURRENCY_*`
  → PHP 8.1+ Enums з castable.
- [ ] **Міграції без індексів на FK** — 50 файлів, індекси лише у spatie/permission. → додати `$table->index('*_id')` на всі foreign_id.
- [ ] **2 Mailable, жодного Export/Notification класу, жодних queues** для листів. → `ShouldQueue` + Redis connection.

### 🟢 P3 — nice to have

- [ ] **`routes/api.php` (138 рядків) без версіонування** — `prefix('api/v1')`.
- [ ] **Blade (44+ файлів) без lazy-loading patterns** — переглянути цикли з relations.
- [ ] **Tests — 2 `ExampleTest.php` заглушки**, 273 файли `app/` без покриття. → integration-тести для `Crud`, `Payment`, `Checkout`.
- [ ] **Tenant-заглушки (`database/tenant/`, `Listeners/ConfigureTenantConnection`)** — тенантів немає. **Видалити dead tenant-код** щоб не плутав.

### ❓ Відкриті питання

- [ ] **`Listeners/ConfigureTenantConnection`** — інфраструктура реально використовується чи dead code з шаблону?
- [ ] **`app/Services/ApiService.php`** — клієнт до якого зовнішнього API? → перейменувати на `XxxApiClient`.

### 📊 Target-метрики

- Найбільший контролер **< 200** рядків (зараз 317)
- Найбільша модель **< 200** рядків (зараз 468)
- `Services/` — **≥ 6** класів (зараз 2)
- 0 `dd()` / `env()` поза `config/` / tenant-коду
- Тестів: **> 20 Feature + Unit**

## 🔗 Пов'язані нотатки

- [[visson-ecosystem/project-overview|🗺 MOC: Visson Ecosystem]]
- [[visson-ecosystem/sessions/2026-04-19-visson-audit|📋 Аудит 19.04.2026]]
- [[air-trans/project-overview|air-trans]]
- [[buktreck/project-overview|buktreck]]
- [[3g/project-overview|3g]]
- [[mono-system/project-overview|mono-system]]
- [[vts/project-overview|vts]]

## 📌 Відкриті питання

- [ ] 
