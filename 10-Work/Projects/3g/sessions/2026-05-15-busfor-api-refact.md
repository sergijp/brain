---
title: "3g: Busfor API — масштабний рефакторинг (Б+В+Г)"
date: 2026-05-15
tags: [3g, work, session, busfor, api, refactoring]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

# 3g: Busfor API — масштабний рефакторинг (Б+В+Г)

**Гілка:** `busfor-api-refact`
**Стек:** Laravel 10, PHP 8.1
**Scope:** `app/Services/Api/v1/Busfor/`

## Мета сесії

Виконати рефакторинг Busfor API за аудит-чеклістом: виправити контрактні баги (Фаза Б), усунути вразливості безпеки (Фаза В), додати транзакційність (Фаза Г).

## Виконано

### Фаза Б — Контрактні баги (всі 12)

- `/cancel` і `/buy` — повертати `orderId` замість `id`
- `/retinfo` — `to.id` зберігає `id`, а не `title`; `percId`/`ruleId` — integer (не string)
- `/trips` — `lang` тепер nullable
- `returnInfoTicket` — guard 422 якщо ні `ticket` ні `buyid`
- Масштабний nullsafe-фікс по всіх Resources та Controllers:
  - `RetinfoResource`, `TripListResource`, `TripInfoResource`
  - `RouteStationsResource`, `RouteResource`
  - `OrderController`, `TripController`, `TicketsController`

### Фаза В — Безпека

- **В-2:** Видалено Guzzle HTTP self-call з `AuthController`. Створено `IssueBusforToken` service — використовує `Auth::attempt()` + Passport `createToken()` напряму.
- **В-4:** `error_log()` → `Log::channel('busfor')->warning/error()`, ловить `\Throwable`. Додано канал `busfor` у `config/logging.php` → `storage/logs/busfor.log`.
- **В-5:** `$router->any()` → семантичні HTTP-методи (GET/POST/PUT/DELETE) у `BusforApiProvider.php`.
- **В-6:** Namespace fix у `Middleware/ExternalAuthToken.php` (був `External\Middleware`, має бути `Busfor\Middleware`) + `app/Http/Kernel.php`.

### Фаза Г — Транзакції

- **Г-5:** `DB::transaction()` у `OrderController::reject()` та `sell()`. Виявлено: `TicketObserver::updating()` блокує bulk update — замінено `->update()` на `->each(fn($t) => $t->update(...))`. Логування помилки у `busfor` канал + 500-відповідь.
- **Г-6:** `DB::transaction()` у `TicketsController::returnTicket()` (включно з `calculateAmount()`).

### Додатково

- Уніфікований формат помилок валідації у всіх 11 Form Requests (`failedValidation` → `{"error": {"code": "E_PARAMS_VALIDATE", "message": "Wrong params", "errors": {...}}}`)
- Новий `LoginRequest.php` (замість `$request->validate()` в контролері)
- Новий `StationsRequest.php` (для `StationController`)
- `OrderController`: `Order::find($order->id)` → `$order->refresh()`, `$order->load(['tickets.parentTicket', 'tickets.childTicket'])`, N+1 фікс через `with([...])`, Carbon null guard + `(int)` cast для `auto_cancel_book_time`
- `BusforApiProvider`: виправлено typo `pointConnectSucces` → `pointConnectSuccess`, роут увімкнено

## Важливі рішення (ADR)

| Рішення | Чому |
|---------|------|
| `IssueBusforToken` замість Guzzle self-call | Loopback HTTP = зайві затримки + залежність від запущеного сервера |
| `->each()` замість bulk `->update()` | `TicketObserver::updating()` не спрацьовує на bulk — критично для бізнес-логіки |
| Орієнтуємось на код, не на spec.pdf | Код у продакшні — джерело правди для статусів і форматів |
| Кеш (Фаза Е) пропускаємо повністю | Рішення користувача — не в скопі рефакторингу |

## Відкладено (не в скопі)

- В-1: `env()` → `config()` (config:cache сумісність)
- В-3: throttle:120,1 на роут-групу
- Г-1..Г-4: DB індекси
- Д: Конкурентне бронювання (lockForUpdate vs Redis lock) — потрібне продуктове рішення
- Е: Кеш (CACHE_DRIVER=file→redis) — пропускаємо повністю
- И: Документація (OpenAPI, Postman, PDF)
- Ж: Архітектурний рефакторинг (умовна фаза)

## Артефакти

### Нові файли

| Файл | Призначення |
|------|-------------|
| `IssueBusforToken.php` | Service для видачі токена без Guzzle |
| `Requests/LoginRequest.php` | Form Request для `/login` |
| `Requests/StationsRequest.php` | Form Request для `StationController` |

### Змінені файли

- `Http/Controllers/OrderController.php`
- `Http/Controllers/AuthController.php`
- `Http/Controllers/TicketsController.php`
- `Http/Controllers/TripController.php`
- `Http/Controllers/StationController.php`
- `Resources/RetinfoResource.php`
- `Resources/TripListResource.php`
- `Resources/TripInfoResource.php`
- `Resources/RouteStationsResource.php`
- `Resources/RouteResource.php`
- `BusforApiProvider.php`
- `app/Http/Kernel.php`
- `config/logging.php`
- `app/Services/Api/v1/Busfor/checklist.md`
- Всі наявні Requests (11 файлів) — уніфікований `failedValidation`

## Пов'язані нотатки

- [[2026-04-28-busfor-api-audit]] — початковий аудит, список 12 контрактних розбіжностей