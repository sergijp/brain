---
title: "Проект: 3G — Аналіз і часткові фікси SyncInfobusTicketJob"
date: 2026-04-23
tags: [work, session, 3g, infobus, booking]
category: work
project: 3g
status: in-progress
pinecone_indexed: false
---

## Мета сесії

Знайти і виправити баг: при синхронізації квитків з Infobus на маршрутах з пересадкою (transfer) основний квиток створюється, а трансферний — ні.

## Виконано

- Повний аналіз `SyncInfobusTicketJob`, `InfobusService`, `CreateTicketJob`, `BookingService`
- Виявлено 4 баги в логіці трансферних квитків
- Частково виправлено `CreateTicketJob.php`
- Зміни в `BookingService.php` відкочено (зламали звичайне бронювання)

## Важливі рішення (ADR)

| Рішення | Причина | Статус |
|---|---|---|
| Відкотити `DB::transaction` в `book()` | Зламав звичайне бронювання — конфлікт вкладених транзакцій | Відкочено |
| Зміна дублікат-перевірки: name/surname → ticket_api | Коректна робота при ретраях джоби | Залишено |
| Eager-load `stations.transfer.stations` | Уникнення N+1 при завантаженні трансферного рейсу | Залишено |
| Telegram при ErrorTicket | Сповіщення тільки при нових помилках | Залишено |

## Виявлені баги

### Баг 1 — Відсутність атомарності в `book()`
`BookingService::book()` не має загальної транзакції. `bookOriginal()` комітить основний квиток окремо, якщо `bookTransfer()` після цього фейлиться — маємо основний квиток без трансферного. При ретраї джоби — дублікат-перевірка знаходить основний і пропускає все.

### Баг 2 — Неправильне місце на трансферному рейсі
`bookTransfer()` бере `placeNumber` і `placeUuid` з головного автобуса. Якщо це місце зайняте на трансферному рейсі → `BookedPlacesException`.

### Баг 3 — Null pointer в `getTransferStations()`
`$from->order`, `$to->order`, `$transfer_station_to->order` без null-перевірок.

### Баг 4 — Дублікат-перевірка по name/surname (виправлено)
При ретраї — знаходився основний квиток по name/surname, весь блок пропускався.

## Проблеми й як вирішили

- `DB::transaction` в `book()` зламав звичайне бронювання → відкочено, потрібно окремо розібратись з вкладеними транзакціями (`DB::transaction` + `$trip->getConnection()->transaction()`)

## Артефакти

| Файл | Статус |
|---|---|
| `app/Jobs/Tickets/CreateTicketJob.php` | Змінено (ticket_api check, eager-load, Telegram) |
| `app/Services/BookingService.php` | Відкочено до оригіналу |
| `app/Services/InfobusService.php` | Без змін |

## Пов'язані нотатки

- [[3g/project-overview]]