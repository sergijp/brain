---
title: "air-trans — Visson логістика (еталон)"
date: 2026-04-19
tags: [work, project, visson, laravel, air-trans]
category: work
project: air-trans
status: active
stack: ['Laravel 11', 'Vue 3', 'Vite', 'MySQL', 'Redis', 'Docker']
pinecone_indexed: false
---

# air-trans — Visson логістика (еталон)

**Пріоритет:** ⭐ ЕТАЛОН  
**Група:** A — активне ядро  
**Домен:** Air cargo / логістика транспорту

## 🗺 Огляд

Найсвіжіший проект на L11. Обрано як еталон для виділення visson/core-пакетів. Сюди паралельно з екстракцією застосовувати нові індекси та eager loading.

## 🛠 Технічний стек

- **Laravel:** `^11.0`
- **PHP:** `^8.2`
- **Стек:** Laravel 11, Vue 3, Vite, MySQL, Redis, Docker
- **Composer (top):** cviebrock/eloquent-sluggable, guzzlehttp/guzzle, intervention/image, kalnoy/nestedset, lcobucci/jwt
- **NPM (top):** @vitejs/plugin-vue, @vueform/multiselect, @vuelidate/core, @vuelidate/validators, bootstrap
- **Docker:** так

## 📦 Репозиторій

- **Remote:** `git@github.com:VissOn/air-trans-system.git`
- **Branch:** `master`
- **Last commit:** 2026-03-03

## 📊 Розмір

- **Файлів:** 1 274
- **Міграцій:** 58
- **Найбільші контролери:**
  - `TicketsCrudController.php` — **467** рядків
  - `LiqPay.php` — **264** рядків

## 🎯 Рекомендовані дії

- [ ] Обрати як еталон для пакетів visson/*
- [ ] Пілотна інтеграція visson/core-middleware (Фаза 2, тиждень 6)
- [ ] Додати індекси у 5 топ-таблиць; CACHE_DRIVER=redis
- [ ] Mail::send → Mail::queue

## 🔧 Рефакторинг (2026-04-19)

> Нагадування: мульти-тенантності немає і не планується. Refactor-плани нижче це враховують.

### 🔴 P1 — критично

- [ ] **`TicketsCrudController.php` (467 рядків, 37 методів, 8 traits)** — розбити: винести `tripsSearch` (L321), `membersSearch` (L336), `flightsSearch` (L350), `findClient` (L365) в окремий `TicketsSearchController` або `TicketSearchService`. `setupCreateOperation()` (L192–308) витягти у `app/Crud/FieldConfigs/TicketFieldConfig.php`.
- [ ] **`TicketsController.php:51` — `error_log($e->getMessage())`** → `Log::error('Ticket error', ['exception' => $e])`. Заборонити `error_log()` у проекті (PHPStan rule).
- [ ] **`Ticket.php` (163 рядки) — god-model** — витягти `pdf()`, `pdfFile()`, `getPdfLink()` у `app/Services/Tickets/TicketPdfService.php`. Видалити dead code: L91–93, L105–109 (дубль `getCanTicketStatusesAttribute`).
- [ ] **`LiqPay.php` (264 рядки) в `app/Http/Controllers/`** — перенести у `app/Services/Payment/LiqPayService.php`. Контролер залишити тонким (`LiqPayController` з `handleCallback()`).
- [ ] **`TicketsController.php:71` — `AlphaSms::setApiKey(env('ALPHA_SMS_KEY'))`** → винести у `config/services.php` + DI через `AlphaSmsService`. `env()` поза config = зламаний `config:cache`.

### 🟡 P2 — важливо

- [ ] **`setupCreateOperation()` L192–308 (100+ рядків конфігу полів)** — винести у масивний конфіг `TicketFieldConfig::fields()` або YAML.
- [ ] **`setupListOperation()` L142–169** — `searchLogic` дублюється, витягти в trait `HasTicketSearch`.
- [ ] **`setupListOperation()` L171–182** — видалити закоментований код для `to_name` (dead code).
- [ ] **STATUS як string-константи** → PHP 8.1 enums (`TicketStatus`, `PaymentStatus`). Cast через `'status' => TicketStatus::class`.
- [ ] **`beforeCreateAction()` L315–320** — логіку винести в `StoreTicketAction` / `TicketStoreRequest::prepareForValidation()`.
- [ ] **Vuex 3 (5 stores) → Pinia** — `auth.js`, `noty.js`, `booking.js` та ін. Паралельно ввести TypeScript для нових stores.
- [ ] **`resources/js/plugins/axios.js` (2 інстанси api+auth)** — витягти в `@visson/http-client` з уніфікованим error-handling + interceptors.
- [ ] **4 Mailable (`ReturnedTicketsMail`, `TripCancelledAgencyMail`, ...)** — спільний `AbstractTicketMail` з shared layout/build.

### 🟢 P3 — nice to have

- [ ] **`tests/Feature/ExampleTest.php`, `tests/Unit/ExampleTest.php`** — порожні скелети. Написати тести на `TicketsSearchService`, `LiqPayService`, `StoreTicketAction`.
- [ ] **`docker/web/Dockerfile` — PHP 7.2**, але `composer.json: "php": "^8.2"`. Оновити до PHP 8.3-fpm.
- [ ] **26 FormRequest** — перевірити дублі правил валідації, витягти спільне в `BaseTicketRequest`.
- [ ] **1 Export (`TicketsExport`)** — якщо додаватимуться — інтерфейс `Exportable` + фабрика.

### ❓ Відкриті питання

- [ ] **`ModuleManager.php` (624 рядки)** — це фіча (динамічні теми/модулі) чи tech debt? Якщо фіча — винести у `visson/module-manager` пакет; якщо debt — видалити.
- [ ] **Дубль логіки `saveTicket()` vs `TicketsCrudController`?** — перевірити чи не дублюється створення квитка в двох місцях.

### 📊 Метрики після рефакторингу (target)

- Найбільший контролер: **< 200 рядків** (зараз 467)
- Методів на клас: **< 15** (зараз 37 у `TicketsCrudController`)
- Покриття тестами: **> 40%** на `Services/`
- 0 `env()` поза `config/*`
- 0 `error_log()` у кодбазі

## 🔗 Пов'язані нотатки

- [[visson-ecosystem/project-overview|🗺 MOC: Visson Ecosystem]]
- [[visson-ecosystem/sessions/2026-04-19-visson-audit|📋 Аудит 19.04.2026]]
- [[grosser/project-overview|grosser]]
- [[buktreck/project-overview|buktreck]]
- [[3g/project-overview|3g]]
- [[mono-system/project-overview|mono-system]]
- [[vts/project-overview|vts]]

## 📌 Відкриті питання

- [ ] 
