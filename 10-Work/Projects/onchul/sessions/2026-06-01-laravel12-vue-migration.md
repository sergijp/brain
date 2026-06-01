---
title: "Проект: Onchul — Міграція Laravel 10→12 та оновлення Vue/Vite"
date: 2026-06-01
tags: [onchul, work, session, laravel, upgrade, migration]
category: session
project: onchul
status: completed
aliases: [onchul-laravel12-migration]
pinecone_indexed: false
---

# Onchul — Міграція Laravel 10→12 та оновлення Vue/Vite

## Мета сесії

Підняти backend з Laravel 10 до Laravel 12 (latest), PHP мінімум з 8.1 до 8.2, оновити всі сумісні пакети. Frontend — оновити залежності до latest у межах поточних мажорів (Vue 3.x, Vite 5.x) без мажорних стрибків.

## Виконано

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Laravel 10 → 11 → 12 (ітеративно) | ✅ Laravel 12.61.0 |
| 2 | PHP мінімум 8.1 → 8.2 | ✅ |
| 3 | `laravel/passport` 11 → 13 | ✅ |
| 4 | `laravel/sanctum` 3.3 → 4.3 | ✅ |
| 5 | `spatie/laravel-permission` 5 → 6 | ✅ |
| 6 | `predis/predis` 1.1 → 2.4 | ✅ |
| 7 | `nesbot/carbon` 2 → 3 | ✅ |
| 8 | `phpunit/phpunit` 10 → 11 | ✅ |
| 9 | `cviebrock/eloquent-sluggable` 10 → 12 | ✅ |
| 10 | `diglactic/laravel-breadcrumbs` 8 → 10 | ✅ |
| 11 | `lcobucci/jwt` 4 → 5 | ✅ |
| 12 | `staudenmeir/eloquent-eager-limit` видалено | ✅ (несумісний з L11+, не використовувався) |
| 13 | Vue 3.4 → 3.5.35 | ✅ |
| 14 | Vite 5.1 → 5.4.21 | ✅ |
| 15 | Vue Router 4.3 → 4.6.4 | ✅ |
| 16 | Права `oauth-public.key` 644 → 600 | ✅ |
| 17 | Carbon 3 — `(int)` касти для `['HH']`/`['mm']` | ✅ 10 файлів виправлено |

## Важливі рішення

| # | Питання | Рішення | Чому |
|---|---------|---------|------|
| 1 | Зберігати old-style skeleton чи мігрувати на новий? | Зберегти `app/Http/Kernel.php`, старий `bootstrap/app.php` | 44 middleware + 9 кастомних провайдерів — ризик великий, L12 підтримує обидва підходи |
| 2 | Technical debt (jQuery, socket.io 2.4, beta-пакети) | Відкласти в опціональну Фазу 5 | Не блокує апгрейд, окремий scope |
| 3 | `staudenmeir/eloquent-eager-limit` | Видалити пакет + прибрати трейт | Трейт використовувався лише в `WidgetPage` без жодного `->limit()` у відносинах |
| 4 | L12.0.0 vs latest | Фіксувати на `v12.61.0` (потім `^12.0`) | L12.0.0 мав баг з legacy Console Kernel (`$this->laravel` = null) — виправлено в пізніших патчах |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| `Passport::ignoreMigrations()` не існує в Passport 12 | Прибрали виклик з `AppServiceProvider` — OAuth-міграції вже опубліковані в проєкт |
| `diglactic/laravel-breadcrumbs ^8.1` не підтримує L11 | Апгрейд до `^10.0` |
| `staudenmeir/eloquent-eager-limit ^1.8` підтримує лише до L10 | Видалення пакету + трейту з `WidgetPage` |
| `cviebrock/eloquent-sluggable ^11.0` не підтримує L12 | Апгрейд до `^12.0` |
| `phpunit ^10` несумісний з L12 | Апгрейд до `^11.0` |
| `nunomaduro/collision ^8.0-8.5` конфліктує з L12 | Апгрейд до `^8.6` |
| L12.0.0 — `$this->laravel` null у `Command::run()` | Оновлення до `v12.61.0` (bug у початковому релізі) |
| Carbon 3: `setUnit()` відхиляє `string` | `(int)` касти у `Trip.php`, `Route.php`, `Ticket.php`, `TripStation.php`, `TripsService.php`, обидва `OrderController` — всі місця де `['HH']`/`['mm']` з JSON-полів |

## Артефакти

- `migrate.md` — план міграції у корені проєкту
- `composer.json` — оновлені версії всіх backend залежностей
- `package.json` + `package-lock.json` — оновлені npm залежності
- Змінені PHP файли:
  - `app/Providers/AppServiceProvider.php`
  - `app/Providers/AuthServiceProvider.php`
  - `app/Entities/System/Content/WidgetPage.php`
  - `app/Entities/System/Trip.php`
  - `app/Entities/System/Route.php`
  - `app/Entities/System/Ticket.php`
  - `app/Entities/System/TripStation.php`
  - `app/Services/TripsService.php`
  - `app/Http/Controllers/Api/OrderController.php`
  - `app/Services/Api/v1/Busfor/Http/Controllers/OrderController.php`

## Стан після сесії

- `php artisan about` → Laravel 12.61.0 ✅
- `npm run build` → обидві entry points без помилок ✅
- PHPUnit: 1 fail (pre-existing, Passport OAuth тест без запущеного сервера) ✅

## Що залишилось (Фаза 5 — опціональна)

- jQuery в `app-frontend.js`
- `socket.io-client 2.4` → 4.x
- `vue-select`, `vue3-timepicker` beta → стабільні
- Array-синтаксис маршрутів (`['uses'=>'Controller@method']`)
- `vue-template-compiler` (Vue 2, зайвий)

## Пов'язані нотатки

- [[onchul]]
