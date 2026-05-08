---
title: "Busfor API — провайдер, аудит, контрактні розбіжності"
date: 2026-05-08
tags: [3g, architecture, integration, busfor, api]
category: docs
project: 3g
status: active
aliases: ["3g-busfor", "3g-busfor-api"]
pinecone_indexed: false
---

# Busfor API — провайдер

`app/Services/Api/v1/Busfor/` — реалізація провайдера для Busfor (агрегатор маршрутів).

## Канонічні артефакти у репо

- **`spec.pdf`** — офіційна специфікація Busfor (62 сторінки)
- **`refact.md`** — загальний код-аудит (36 знахідок: критичні баги, безпека, швидкодія, якість)
- **`docs_refact.md`** — порівняння spec ↔ реалізація з готовими патчами A-J

> При будь-яких задачах щодо Busfor (`AuthController`, `OrderController`, `TripController`, `TicketsController`, `StationController`) **читати ці файли** — там готові патчі та класифіковані знахідки.

## Контролери провайдера

- `AuthController` — `/login`
- `OrderController` — `/cancel`, `/buy`, `/reject`, `/sell`, `/retinfo`, `/status`
- `TripController` — `/trips`, `/route`
- `TicketsController` — `/returnTicket`, `/returnInfoTicket`
- `StationController` — `/stations`, `/stops`

## Контрактні розбіжності зі spec (критичні)

| Endpoint | Spec | Реалізація |
|---|---|---|
| `/login` | поле `user`, помилка `{"message":...}` | поле `login`, помилка `{"error":{...}}` |
| `/cancel`, `/buy` | повертає `orderId` | повертає `id` |
| `/retinfo` | `percId='full'` (string) | integer; у `to.id` для трансферу записується `title` (БАГ) |
| `/status` | `CANCELED` (одне L) | `CANCELLED` |
| `/status` | без `PREBOOKED` | повертається `PREBOOKED` |
| `/trips` | `lang` optional | `required` |
| `/point_connect_success` | endpoint є | роут закоментовано (`BusforApiProvider.php:29`) + опечатка в назві методу `pointConnectSucces` |

## Runtime баги

- `Middleware/ExternalAuthToken.php` — namespace mismatch (файл у `Busfor/Middleware/`, namespace `App\Services\Api\v1\External\Middleware`).
- `Resources/TripListResource.php:43` — `$trip->back_route` (undefined; має бути `$this->back_route`).
- `Resources/TripListResource.php:62` — undefined `$transfer` коли не трансфер.
- `Controllers/OrderController.php:99` — `$seat['parent_ticket_id']` (`$seat` undefined; має бути `$ticket`).
- `Controllers/TicketsController.php:99-120` — `returnInfoTicket` без `ticket`/`buyid` повертає перший Order у БД (БАГ).

## Швидкодія

- N+1 у Resources (`TripListResource` робить `Station::find()` × 2 на рейс).
- `->get()->count() > 0` замість `->exists()` у `TripInfoResource`/`TripListResource`/`RetinfoResource`.
- Bulk update + транзакції відсутні у `OrderController::reject/sell` та `TicketsController::returnTicket`.
- `getAllStations` без кешу/пагінації.

## Скасована претензія (помилкова)

`dates: [[...]]` у `/route` — **відповідає специфікації**, не баг.

## Розширення поза spec

Треба або задокументувати, або прибрати:
- Уся логіка трансферних рейсів (`is_transfer`, `bus_transfer`, `wait_time_minutes`...).
- Поля `discount`, `gender`, `transfer_number`, `prebooking` у `/reservate`.
- Endpoint-и `/ping`, `/stops`.

## Пов'язані

- [[INDEX]]
- [[infobus-sync]] — інша зовнішня інтеграція з аналогічним типом проблем
- [[legacy-controllers]] — `TicketsCrudController` (внутрішній CRUD) — окремо
- Tier-2 pointer: `~/.claude/projects/-Users-serhiin-Data-Source-3g/memory/project_busfor_api_audit.md`
