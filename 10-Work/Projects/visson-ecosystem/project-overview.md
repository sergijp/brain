---
title: "Visson Ecosystem — MOC"
date: 2026-04-19
tags: [work, project, moc, visson, laravel, refactoring]
category: work
project: visson-ecosystem
status: active
stack: [Laravel, Vue, MySQL, Redis, Docker]
pinecone_indexed: false
---

# 🗺 Visson Ecosystem — Map of Content

> Аудит і план рефакторингу 30+ проектів у `~/Source`, побудованих на спільному самописному Laravel-ядрі ("Visson core"). Без мульти-тенантності — консолідація через приватні composer/npm пакети.

	**Аудит:** [[visson-ecosystem/sessions/2026-04-19-visson-audit|📋 Повний аудит 19.04.2026]]  
**Звіт:** `~/Source/outputs/Visson-Refactoring-Report.docx` (14 сторінок)

## 🎯 Ключові висновки

- **14 активних проектів** на спільному ядрі (Laravel 7–11 + Vue 2/3)
- **15–20% коду байт-ідентичне** (≈300–400 файлів дублюються між 5 копіями)
- **0 власних індексів БД** у 319 міграціях
- **Контролери до 2 071 рядка** (buktreck ApplicationsCrudController)
- **Немає git submodules / composer path / symlinks** → синхронізація руками
- **Рекомендація:** 5 composer-пакетів + 1 NPM ui-kit, Satis приватний реєстр, air-trans — еталон

## 🔥 Група А — активне ядро

| Проект | L | Файлів | Статус | Нотатка |
|--------|---|--------|--------|---------|
| [[air-trans/project-overview\|air-trans]] | 11.0 | 1 274 | ⭐ ЕТАЛОН | Air cargo / логістика транспорту |
| [[grosser/project-overview\|grosser]] | 11.0 | 1 218 | 🔥 HIGH | E-commerce / продукти / каталог |
| [[buktreck/project-overview\|buktreck]] | 11.0 | 1 275 | 🔥 HIGH | Bus logistics / transport management |
| [[3g/project-overview\|3g]] | 10.10 | 1 529 | 🔥 HIGH | Transport routes / trips / logistics |
| [[mono-system/project-overview\|mono-system]] | 10.10 | 1 454 | 🔥 HIGH | Bus logistics / trips / routes |
| [[vts/project-overview\|vts]] | 10.10 | 1 391 | 🔥 HIGH | Transport services / trips / routes |
| [[bsystem/project-overview\|bsystem]] | 7.0 | 1 258 | ⚠️ RISK L7 | Bus routes / trips / transport |
| [[bustick-admin/project-overview\|bustick-admin]] | 9.19 | 887 | MEDIUM | Bus ticketing / logistics admin |
| [[padmin/project-overview\|padmin]] | 9.19 | 1 060 | MEDIUM | E-commerce admin (parfumo/products/orders) |

## 🗃 Група В — legacy / архів

| Проект | L | Файлів | Last commit | Дія |
|--------|---|--------|-------------|-----|
| [[gt-admin-new/project-overview\|gt-admin-new]] | 9.19 | 1 176 | 2024-04-22 | LOW / заморозити |
| [[bustrek/project-overview\|bustrek]] | 7.0 | 4 139 | 2026-02-13 | LOW / довідник |
| [[gt17/project-overview\|gt17]] | 8.75 | 4 461 | 2023-01-13 | ARCHIVED |
| [[gt17admin/project-overview\|gt17admin]] | 7.0 | 5 377 | 2024-03-13 | ARCHIVED |
| [[ats/project-overview\|ats]] | 7.0 | 1 205 | 2023-03-17 | ARCHIVED |
| [[v-admin-vue2/project-overview\|v-admin-vue2]] | 7.0 | 1 147 | n/a | ARCHIVED / merge into mono-system |
| [[v-admin/project-overview\|v-admin]] | 9.19 | 200 | 2023-01-17 (base) | ARCHIVED |
| [[santaopt/project-overview\|santaopt]] | 7.24 | 111 | 2023-11-01 | OUT-OF-SCOPE |

## 📦 Група Г — стаби / інше

- [[agent/project-overview|agent]] — Інструментарій для Claude Code (roman01la/skills-agents). Не чіпати.
- [[journal/project-overview|journal]] — Docs + mockups для трейдинг-щоденника. Окремо від Visson.
- [[billing/project-overview|billing]] — Папки docs/ і mockups/, немає коду.
- [[trading/project-overview|trading]] — Індикатори SMC. Окремий домен.
- [[node/project-overview|node]] — Старий stub на 5 файлів. Видалити.
- [[abs_calculator/project-overview|abs_calculator]] — Git repo, 0 файлів.
- [[v-admin-api/project-overview|v-admin-api]] — Git repo, 0 файлів.

## 🔧 Поглиблений аудит активних (2026-04-19)

> Пройшлися по всіх 9 активних проектах, зафіксували refactor-знахідки з `файл:рядок`. Повні чек-листи — у кожній `project-overview.md`. Нижче — агрегат.

### 🧩 Типові Visson-core патерни (повторюються у 8/9 проектах)

| Патерн | Де | Виняток |
|---|---|---|
| `app/Crud/Operations/CopyOperation.php:53–54` — `dd($e)` ×2 у production | air-trans, grosser, buktreck, 3g, mono-system, vts, bsystem, padmin | **bustick-admin** (вже очищено) |
| `app/Http/Controllers/LiqPay.php` (~264 рядки) — у Controllers замість Services | усі 9 | — |
| `docker/*/Dockerfile` — PHP 7.2 при composer `^8.1/8.2` | усі 9 | — |
| `app/Entities/Tenant/*` + `Listeners/Tenant/*` — dead tenancy convention (без `stancl/tenancy`) | 8/9 | vts (чистий!) |
| `env()` поза `config/` | 13–45 місць на проект | — |
| `Tests` — лише `ExampleTest` заглушки | усі 9 | — |
| `const STATUS_*/TYPE_*/CURRENCY_*` замість Enums | усі 9 | — |
| Vuex замість Pinia, 0 TypeScript | усі 9 | — |

### 📊 Хіт-парад god-файлів (по всіх активних)

| Файл | Рядків | Проект | Дія |
|---|---|---|---|
| `ApplicationsCrudController.php` | **2 071** | buktreck | ⚠ розбити P1 |
| `TripsCrudController.php` | 1 709 | 3g | ⚠ розбити P1 |
| `resources/js/store/booking.js` | **1 732** | vts | ⚠ фронтенд-god-store P1 |
| `TripsCrudController.php` | 1 256 | bsystem | ⚠ upgrade-blocker |
| `Trip.php` (model) | 1 188 | mono-system | god-model |
| `WidgetsController.php` | 1 179 | bsystem / 3g | god-controller |
| `TripsCrudController.php` | 1 151 | mono-system | god-controller |
| `Trip.php` | 1 120 | vts | god-model |
| `TripsCrudController.php` | 1 112 | bustick-admin | god-controller |
| `Trip.php` | 1 085 | 3g | god-model |

### 🎖 Ранжування за "станом здоров'я"

| Rank | Проект | Оцінка | Коментар |
|---|---|---|---|
| 🥇 | **air-trans** | еталон | Найменший controller (467), чистіший за всіх |
| 🥈 | **vts** | добре | Єдиний БЕЗ tenant-stubs, 7 Observers/Scopes, 14 Jobs, 54 FK-індекси |
| 🥉 | **grosser** | ок | L11, e-commerce зрозумілий |
| 4 | **buktreck** | ⚠ god-controller | 2071 рядків ApplicationsCrudController — блокує |
| 5 | **mono-system** | ⚠ god-model | Trip 1188 + N+1 у print-ticket |
| 6 | **3g** | ⚠ dd() + env-розсип | 20+ env() у одному контролері |
| 7 | **bustick-admin** | заморожений 2 роки | Плюс: Vite, `CopyOperation` почищено |
| 8 | **padmin** | **WIP 35–40%** | Злити в grosser (обидва e-commerce) |
| 9 | **bsystem** | **L7 EOL** | Upgrade-трек окремо, ~3–4 тижні |

### ❓ Наскрізні відкриті питання (перевірити перед Фазою 2)

- [ ] **Tenancy-stubs** — вивчити: видалити повсюди чи реалізувати через Spatie/multitenancy? (Правило: тенантів немає → **видалити**).
- [ ] **`LiqPay.php` у всіх 9 проектах** — скопіпащений чи є розбіжності? Якщо ідентичний → одразу у `visson/liqpay-service` composer-пакет.
- [ ] **padmin ↔ grosser** — оверлап функціональності. Якщо так → merge.
- [ ] **bustick-admin ↔ bsystem** — branch `bus_transfer` у обох. Один домен чи два?
- [ ] **`ModuleManager.php` у air-trans (624 рядки)** — фіча чи tech debt?
- [ ] **`Entities/Tenant/*` convention** — просто нейм-шаблон чи реальне розділення контурів?

### 🎯 Оновлені пріоритети Фази 1 (quick wins на основі аудиту)

1. **Видалити `dd()` з `CopyOperation.php`** у 8 проектах (одна заміна `dd()` → `Log::error()` в Visson-core шаблоні, потім розкатати).
2. **Перенести `LiqPay.php` → `Services/Payment/LiqPayService.php`** у всіх 9 (попередньо порівняти md5 — якщо ідентичні, це буде перший composer-пакет).
3. **Оновити Dockerfile PHP 7.2 → 8.2** у всіх 9 (docker-файли майже ідентичні).
4. **Витягти `env()` у `config/services.php`** — в 3g (20+ вхождень у TripsCrudController) і vts (43 місця!) — пріоритетно.
5. **Видалити dead tenant-код** (`Entities/Tenant/*`, `Listeners/Tenant/*`, `database/tenant/`) у 8 проектах (окрім vts).

## 📋 План рефакторингу (5 фаз, 14 тижнів)

### Фаза 0 — Підготовка (тиждень 1)
- [ ] Satis/Private Packagist розгорнуто
- [ ] GitHub-org `visson-core` + 6 порожніх репо для пакетів
- [ ] Заморозити gt17, gt17admin, ats, santaopt, v-admin*, bustrek (read-only)
- [ ] [[air-trans/project-overview|air-trans]] обрано як еталон

### Фаза 1 — Performance sprint (тиждень 1–2, паралельно) — +30%
- [ ] Індекси у 5 топ-таблицях (trips, tickets, routes, stations, orders)
- [ ] Eager loading у TripsCrudController/WidgetsController/print-ticket Blade
- [ ] `CACHE_DRIVER=redis` + `QUEUE_CONNECTION=redis` у всіх active .env
- [ ] `Mail::send` → `Mail::queue` у всіх контролерах
- [ ] `composer install --optimize-autoloader`, `config:cache`, `route:cache`

### Фаза 2 — Екстракція ядра (тижні 3–6)
- [ ] `visson/core-middleware` v0.1.0 (11 ідентичних middleware)
- [ ] `visson/helpers` (5 трейтів)
- [ ] `visson/crud-kit` (Crud, CrudController, 6 Operations)
- [ ] `visson/system-entities` (Activity, File, Gallery, Language, Text, Website + міграції)
- [ ] `visson/excel-exports` + `visson/auth-providers`
- [ ] Пілотна інтеграція в [[air-trans/project-overview|air-trans]]

### Фаза 3 — Міграція проектів (тижні 7–14)
- [ ] тиждень 7–8: [[grosser/project-overview|grosser]], [[buktreck/project-overview|buktreck]] (L11)
- [ ] тиждень 9–10: [[3g/project-overview|3g]], [[mono-system/project-overview|mono-system]], [[vts/project-overview|vts]] (L10→L11)
- [ ] тиждень 11–12: [[bsystem/project-overview|bsystem]] (L7→L11 або окремий трек)
- [ ] тиждень 13–14: [[bustick-admin/project-overview|bustick-admin]], [[padmin/project-overview|padmin]]

### Фаза 4 — Фронт (тижні 4–10, паралельно)
- [ ] `@visson/ui-kit` (Vue 3 + TS + Storybook)
- [ ] Lazy-load routes у всіх проектах
- [ ] moment → dayjs; видалити bootstrap (Tailwind)
- [ ] manualChunks для CKEditor, ApexCharts, mavon-editor
- [ ] Цільовий bundle: 800 KB → ≤ 300 KB

### Фаза 5 — Глибокі (тижні 10–16)
- [ ] Розбивка TripsCrudController / ApplicationsCrudController / WidgetsController
- [ ] Read-replica БД для звітів
- [ ] HTTP ETag
- [ ] OpenAPI-схема через Scribe

## 📈 KPI

- Після Фази 1: P95 −30%, запити у листингу трипів з 300+ до <20
- Після Фази 2: ≥5 пакетів у реєстрі; air-trans повністю на ядрі
- Після Фази 3–4: 10+ проектів на ядрі; initial JS ≤ 300 KB; FCP ≤ 1 сек

## 🔗 Пов'язане

- [[../../CLAUDE-RULES|CLAUDE-RULES]] — правила ведення vault
- [[../../INDEX|INDEX]] — головна
