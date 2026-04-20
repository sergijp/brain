---
title: "bustick-admin — Visson адмінка (Bustick)"
date: 2026-04-19
tags: [work, project, visson, laravel, bustick-admin]
category: work
project: bustick-admin
status: active
stack: ['Laravel 9', 'Vue 2', 'Vite', 'MySQL', 'Docker']
pinecone_indexed: false
---

# bustick-admin — Visson адмінка (Bustick)

**Пріоритет:** MEDIUM  
**Група:** Б — адмін-панелі  
**Домен:** Bus ticketing / logistics admin

## 🗺 Огляд

README згадує tenancy — ймовірно заготовка під мульти-тенантність, але не впроваджена. Vue 2 → потребує апгрейд. Останній commit 04/2024 — фактично заморожений, але не legacy.

## 🛠 Технічний стек

- **Laravel:** `^9.19`
- **PHP:** `^8.0.2`
- **Стек:** Laravel 9, Vue 2, Vite, MySQL, Docker
- **Composer (top):** cviebrock/eloquent-sluggable, guzzlehttp/guzzle, intervention/image, lcobucci/jwt, maatwebsite/excel
- **NPM (top):** @vitejs/plugin-vue2, apexcharts, bootstrap, chart.js, laravel-echo
- **Docker:** так

## 📦 Репозиторій

- **Remote:** `git@github.com:VissOn/bustick-admin.git`
- **Branch:** `main`
- **Last commit:** 2024-04-22

## 📊 Розмір

- **Файлів:** 887
- **Міграцій:** 47
- **Найбільші контролери:**
  - `TripsCrudController.php` — **1112** рядків ⚠️
  - `RoutesCrudController.php` — **714** рядків ⚠️

## 🎯 Рекомендовані дії

- [ ] Оцінити: заморозити чи реактивувати
- [ ] Якщо жити — апгрейд L9→L11 + Vue 2→3
- [ ] Міграція на visson/* у Фазі 3 (тиждень 13–14)

## 🔧 Рефакторинг (2026-04-19)

> Нагадування: мульти-тенантності немає і не планується. Tenancy-заглушки (18 моделей + 6 Listeners) — **dead code без реальної tenancy-бібліотеки в composer**. Видалити.

**Топ-5:** `TripsCrudController` (1112), `Trip` model (894), `RoutesCrudController` (714), `Ticket` model (631), `TicketsCrudController` (482).

### 🔴 P1 — критично

- [ ] **`docker/web/Dockerfile:1` — PHP 7.2** vs composer `^8.0.2`. Контейнер несумісний. → `php:8.2-apache`.
- [ ] **`app/Http/Controllers/LiqPay.php` (264 рядки)** — типовий Visson-патерн. → `app/Services/Payment/LiqPayService.php`.
- [ ] **`env()` leak у `app/Listeners/Tenant/ConfigureTenantConnection.php:21–22`** — `env('DB_USERNAME')`, `env('DB_PASSWORD')` прямо в Listener. Усього **16 місць** `env()` поза config.
- [ ] **Dead tenancy — видалити повністю**:
  - `app/Entities/Tenant/*` — 18 моделей
  - `app/Listeners/Tenant/` — 6 Listeners (`ConfigureTenantConnection`, `ConfigureDatabase`, …)
  - `database/tenant/` — окремі міграції
  - **composer.json БЕЗ `stancl/tenancy`** — це manual stub без реальної реалізації.

### 🟡 P2 — важливо

- [ ] **God-controllers (>400)**: `TripsCrudController` 1112, `RoutesCrudController` 714, `TicketsCrudController` 482, `BookingController` ~418. → Services + Queries + Actions.
- [ ] **God-models у `Entities/Tenant/`**: `Trip.php` 894, `Ticket.php` 631. → split + Enums.
- [ ] **5782 `const ... =` string-константи** на весь проект (26 файлів з `enum`). → поступовий переклад STATUS/TYPE констант на PHP 8.1 enums.
- [ ] **Vuex 3 → Pinia** (разом з Vue 2 → Vue 3). 6 stores: `booking`, `auth`, `activities`, `index`, `noty`, `LocaleManager`.
- [ ] **Vue 2.6.11 (EOL з грудня 2023)** → Vue 3. `@vitejs/plugin-vue2` → `@vitejs/plugin-vue`. Vite config уже готовий — міграція легше ніж у L7-проекту.
- [ ] **19 файлів з `dd()`/`var_dump()`/`die()`** — санітизація + pre-commit hook.
- [ ] **0 реальних тестів** (2× `ExampleTest`) при 177 API-маршрутах → integration-тести перед upgrade.

### 🟢 P3 — nice to have

- [ ] **TypeScript відсутній** — додати при Vue 3 міграції.
- [ ] **WebSocket/Echo + `socket.io-client`** — перевірити реальне використання.
- [ ] **`192 рядки у routes` (15 web, 177 api)** — без версіонування. → `prefix('api/v1')`.
- [ ] **Backpack version** — перевірити сумісність при upgrade.

### ✅ Сильні сторони

- **Vite 4** замість Webpack Mix (єдиний з legacy-тандему що вже на Vite).
- **`CopyOperation.php`** вже очищений від `dd()` (один з небагатьох!).
- **Spatie/permission** + Activity log — RBAC та аудит реалізовані.
- **47 міграцій** — малий розмір (швидше мігрувати).

### 📅 Upgrade path

| Фаза | Час | Головне |
|---|---|---|
| **Підготовка** | 2–3 тижні | Docker PHP 8.2, env→config, LiqPay→Service, **видалити dead tenancy (18+6 файлів)**, почати тести |
| **L9 → L10** | 1–2 тижні | PHP 8.1, Symfony 6, Flysystem 3, нативні типи |
| **L10 → L11** | 1–2 тижні | PHP 8.2, `bootstrap/app.php`, видалення Kernels |
| **Vue 2 → Vue 3 + Pinia** | 3–4 тижні | Composition API, `@vitejs/plugin-vue`, 6 stores → Pinia (паралельно) |

**Загалом:** 8–12 тижнів з тестами, 6–8 без (ризиковано).

### ❓ Відкриті питання

- [ ] **Останній commit 2024-04-22** — проект заморожений 2 роки. Реанімуємо чи архівуємо?
- [ ] **Tenancy-заглушка (18+6 файлів)** — dead code чи планувалось? Якщо dead → видаляємо.
- [ ] **`bus_transfer` branch у bsystem + bustick-admin** — один домен чи два різні? Оверлап функціональності?
- [ ] **WebSocket через Echo/socket.io** — production-фіча чи експеримент?

### 📊 Target-метрики

- Laravel **11.x**, PHP **8.2+**, Vue **3 + Pinia + Vite**
- `TripsCrudController` **< 300** (зараз 1112)
- Tests — **>30 Feature** (зараз 0)
- 0 dead-tenancy файлів (видалити 18+6)
- 0 `env()` поза config
- TypeScript — для нових компонентів

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
