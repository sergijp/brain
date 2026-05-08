---
title: "Infobus Sync — синхронізація квитків (часткові фікси)"
date: 2026-05-08
tags: [3g, architecture, integration, infobus, partial]
category: docs
project: 3g
status: partial
aliases: ["3g-infobus", "3g-infobus-sync"]
pinecone_indexed: false
---

# Infobus Sync — синхронізація квитків

Джоба кожні 10 хв скрапить `dispatcher.bussystem.eu` і додає квитки в систему. На маршрутах з пересадкою (transfer) основний квиток створювався, **трансферний — ні**. Аналіз і часткові фікси проведено, низка змін **відкочена** через регресії.

## Виявлені баги

### 1. Відсутність атомарності — **відкочено**

`book()` не має загальної транзакції. `bookOriginal()` комітить основний квиток; якщо потім `bookTransfer()` фейлиться — основний у БД, трансферного нема.

→ Спроба обгорнути `DB::transaction` зламала звичайне бронювання. Можливо конфлікт з вкладеною транзакцією через `$trip->getConnection()->transaction()`.

### 2. Неправильне місце на трансферному рейсі — **відкочено**

`bookTransfer()` використовує `placeNumber` з головного автобуса. Якщо місце зайняте на трансферному рейсі → `BookedPlacesException`, джоба фейлиться.

### 3. Null pointer у `getTransferStations()` — **відкочено**

`$from->order` / `$to->order` / `$transfer_station_to->order` без null-перевірок.

### 4. Дублікат-перевірка по `name/surname` — **виправлено**

При ретраї джоби основний квиток уже є → знаходиться по `name/surname` → весь блок пропускається → трансферний ніколи не створиться.

→ **Змінено** на `ticket_api + whereNull('parent_id')`.

## Що залишилось у коді (`CreateTicketJob.php`)

- `use Illuminate\Support\Facades\Http` — додано.
- Eager-load: `with(['stations', 'stations.transfer', 'stations.transfer.stations'])`.
- Перевірка дубліката: `ticket_api + whereNull('parent_id')` (замість `name/surname/trip_id`).
- `sendTelegramError()` — Telegram при новому `ErrorTicket`.

## Що відкочено (`BookingService.php`)

Усі зміни в `book()`, `getTransferStations()`, `bookTransfer()` — повернуті до оригіналу.

## Як підходити до наступного фіксу

1. Спочатку розібратись, **чому** `DB::transaction` у `book()` ламає звичайне бронювання — підозра на вкладені транзакції через `$trip->getConnection()->transaction()`.
2. Тільки після цього повертати атомарність + фікс place selection + null-checks.

## Пов'язані

- [[INDEX]]
- [[busfor-api]] — інша зовнішня інтеграція з аналогічним патерном проблем
