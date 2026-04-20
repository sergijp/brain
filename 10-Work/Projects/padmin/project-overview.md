---
title: "padmin — Profumo / Bustrek адмін-панель"
date: 2026-04-19
tags: [work, project, visson, laravel, padmin]
category: work
project: padmin
status: active
stack: ['Laravel 9', 'Vue 2', 'Vite', 'MySQL', 'Docker']
pinecone_indexed: false
---

# padmin — Profumo / Bustrek адмін-панель

**Пріоритет:** MEDIUM  
**Група:** Б — адмін-панелі  
**Домен:** E-commerce admin (parfumo/products/orders)

## 🗺 Огляд

Останній commit "wip" у 03/2024 — незавершена робота. Vue 2. README згадує tenancy.

## 🛠 Технічний стек

- **Laravel:** `^9.19`
- **PHP:** `^8.0.2`
- **Стек:** Laravel 9, Vue 2, Vite, MySQL, Docker
- **Composer (top):** cviebrock/eloquent-sluggable, doctrine/dbal, guzzlehttp/guzzle, intervention/image, kalnoy/nestedset
- **NPM (top):** @vitejs/plugin-vue2, apexcharts, bootstrap, chart.js, laravel-echo
- **Docker:** так

## 📦 Репозиторій

- **Remote:** `git@github.com:VissOn/profumo-admin.git`
- **Branch:** `master`
- **Last commit:** 2024-03-12 (wip)

## 📊 Розмір

- **Файлів:** 1 060
- **Міграцій:** 74
- **Найбільші контролери:**
  - `ProductCrudController.php` — **394** рядків
  - `OrderCrudController.php` — **371** рядків

## 🎯 Рекомендовані дії

- [ ] Прибрати WIP-стан: або закрити, або доробити
- [ ] Апгрейд стеку до L11 + Vue 3
- [ ] Міграція на visson/* (Фаза 3, тиждень 13–14)

## 🔧 Рефакторинг (2026-04-19) — WIP АНАЛІЗ

> Нагадування: мульти-тенантності немає і не планується. Tenant-скелети — dead code, видалити.

**Домен:** eCommerce + B2B маркетплейс з логістикою (StationProduct, SubProduct), payment methods, Activity log, Spatie permissions, Passport OAuth, мультимовність.

### 📊 Готовність по секціях

| Секція | % | Коментар |
|---|---|---|
| Backend models | **85%** | 55 повних, scopes, relations |
| Backend controllers | **80%** | 32 CRUD з повною логікою (250–390 LoC) |
| Frontend | **60%** | 149 компонентів, але Vue 2 + Vuex |
| Tests | **0%** | Тільки `ExampleTest` |
| Docs | **40%** | README для tenancy, без архітектури |

**Загальна оцінка:** ~35–40% технічно / ~65% функціонально.

### 🔴 P1 — критично

- [ ] **`docker/web/Dockerfile` — PHP 7.2** vs composer `^8.0.2`. Не стартує. → `php:8.2-apache`.
- [ ] **`app/Crud/Operations/CopyOperation.php:53–54`** — `dd($e)` × 2 (стандартний Visson-core).
- [ ] **`app/Http/Controllers/Api/Auth/LoginController.php` — `dd(1)` блокує автентифікацію** (!). Або забута debug, або ознака недокінченого OAuth-flow.
- [ ] **Tenancy-скелети — 57 файлів без реалізації**:
  - `app/Entities/Tenant/Activity.php`, `Setting.php` — тільки `// TODO`
  - `app/Listeners/Tenant/*` — не підписані
  - Без `stancl/tenancy` у composer
  → видалити (тенантів немає).
- [ ] **Payment methods — 3 класи з `// TODO`**:
  - `SelfPickUp.php`, `BankTransfer.php`, `CacheOnDelivery.php`
  Для eCommerce — **blocker**, жоден метод оплати не функціонує.

### 🟡 P2 — важливо

- [ ] **God-controllers**: `ProductCrudController` (394), `OrderCrudController` (371). → Services/Actions.
- [ ] **`OrderCrudController.php:40–80`** — закоментовані фільтри (dead code).
- [ ] **13 `env()` поза config** (порівняно мало, але має бути 0).
- [ ] **Vue 2.7 + Vuex → Vue 3 + Pinia** (149 компонентів — суттєвий обсяг).
- [ ] **0 тестів** — `phpunit.xml` є, файли порожні.
- [ ] **12 `TODO` у `Entities/Tenant/`** — ключовий маркер незавершеності.
- [ ] **Passport OAuth + Spatie/permission + Activity log** — потребують integration-тестів до upgrade.

### 🟢 P3 — nice to have

- [ ] **README** — додати: архітектура, API, deployment.
- [ ] **Payment methods** — винести у `app/Services/Payment/Methods/*`.
- [ ] **Vite 4** уже є — перевага перед Webpack-проектами.

### ⚠️ Стратегічна рекомендація: **сценарій #2 — злити в grosser**

| # | Сценарій | Час | Коли вибрати |
|---|---|---|---|
| **1** | 🚫 Заморозити / архівувати | 0 | Якщо немає replacement-плану і власника |
| **2** | 🔄 **Злити в grosser** | ~3–4 тижні | **Рекомендовано.** Обидва eCommerce, grosser уже L11 |
| **3** | 🔥 Реанімувати | ~8 тижнів | Тільки якщо замовник наполягає і є owner |

### ❓ Критичні відкриті питання

- [ ] **padmin vs grosser** — оверлап доменів (обидва eCommerce). Якщо так — злиття.
- [ ] **`dd(1)` у `LoginController`** — забута debug чи маркер незавершеного OAuth?
- [ ] **Tenancy-stubs (57 файлів)** — планувалась B2B SaaS чи помилковий шаблон?
- [ ] **413 commits / останній 2024-03-12** — хто веде проект? Активний owner?

### 📊 Target-метрики (якщо реанімувати)

- Laravel **11.x**, PHP **8.2+**, Vue **3 + Pinia**
- Tests — **>30** (зараз 0)
- 0 `dd()` / `env()` поза config
- 0 TODO у `Entities/Tenant/` (видалити або завершити)
- 3 payment methods — реально працюючі

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
