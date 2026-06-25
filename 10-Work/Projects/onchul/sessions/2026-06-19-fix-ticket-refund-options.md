---
title: "Проект: VTS (onchul) — Виправлення баґу з refund-options"
date: 2026-06-19
tags: [onchul, work, session, ticket-refund, bug-fix]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
Розслідувати і виправити баг з повернення квитків через ендпоінт `/refund-options` — система повертала 0% замість розрахованого відсотку за квитки без затвердженого платежу.

## Виконано

| Задача | Результат |
|--------|-----------|
| Діагностика першопричини (debugger) | ✅ Знайдена помилка в `TicketsController:119` — неправильна логіка перевірки `payment_status` |
| Виправлення баґу | ✅ Розділено логіку: окремі методи для публічного профілю й адмін-панелі |
| Оновлення маршрутів | ✅ Додано маршрут GET `/system/tickets/{id}/refund-options` |
| Оновлення api-bridge | ✅ Додано новий namespace `ApiBridge.tickets.getRefundOptions()` |
| Оновлення Vue компоненти | ✅ `TicketCancel.vue` переведена на новий ендпоінт |

## Важливі рішення (ADR)

| Рішення | Чому | Альтернативи |
|---------|------|--------------|
| Розділення методу на два | Профіль (public сайт) має інші вимоги до перевірок, ніж admin CRUD. Профіль логічно перевіряє `payment_status` (касові/агентські платежі нема в системі). Admin-CRUD має дозволяти повернення всім | Один метод з параметром `$skipPaymentCheck` — гірше, більш магічне, складніше для тестування |
| Розташування методу в `TicketsCrudController` | CRUD методи мають бути у CRUD контролері, доступні через CRUD маршрути | Додавати в `Profile/TicketsController` — це контролер профілю, не системного управління |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| **First-symptom:** адміни бачать 0% для всіх квитків без `payment_status='approved'` | Знайдено: метод у `Profile/TicketsController:119` перевіряє `payment_status != 'approved'` → повертає 0% при NULL |
| **Root cause:** касові/агентські платежі мають `payment_status=null` або не встановлено | Логіка для профілю була правильна (касові платежі справді недозволені). Але адміни мали бачити справжній відсоток, оскільки вони керують системою |
| **Secondary issue:** `return_percent` — транзієнтна властивість в `TicketObserver` | Не є критичною для цього баґу, але відмічено для моніторингу розходжень між API й БД |

## Артефакти

### Змінені файли

- **`app/Http/Controllers/Api/Crud/TicketsCrudController.php`**
  - Новий метод `getRefundOptions()` на `line 366`
  - Логіка розрахунку без перевірки `payment_status`
  - Повертає JSON: `{ percent, remaining_days, trip_departure, rules }`

- **`routes/api.php`**
  - Новий маршрут: `GET /system/tickets/{id}/refund-options`
  - Middleware: `can:tickets-read` (Spatie permission)

- **`resources/js/api-bridge.js`**
  - Новий namespace `ApiBridge.tickets.getRefundOptions(ticketId)`
  - HTTP GET до `/api/system/tickets/{id}/refund-options`

- **`resources/js/crud/base/operations/ticket-cancel/TicketCancel.vue`**
  - Старий виклик: `ApiBridge.profile.orders.getRefundOptions()`
  - Новий виклик: `ApiBridge.tickets.getRefundOptions(this.ticket.id)`

### Не змінено, але впливає

- `TicketObserver.php` — утримує `return_percent` як транзієнтну властивість (перевірити на розходження при наступному рефакторингу)

## Пов'язані нотатки

- [[VTS Система прав/ролей]] — Spatie Permission, 5 ролей, права з lang/uk
- [[VTS CRUD система]] — generic CRUD контролери, маршрути, middleware
- [[VTS API Архітектура]] — api-bridge, zwei entry points (app.js / app-frontend.js)
