---
title: "onchul — Рейси: підрахунок місць (booked+prebooked, free без returned/annulled)"
date: 2026-06-22
tags: [onchul, work, session, trips, tickets]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
З'ясувати яким чином підраховуються місця у списку рейсів та виправити логіку підрахунку вільних місць та бронювань.

## Виконано

| Задача | Результат |
|--------|-----------|
| Дослідження підрахунку місць у 4 колонках списку рейсів | ✅ Встановлено, які статуси враховуються в кожній колонці |
| Включити `prebooked` статус до лічильника бронювань | ✅ Змінено метод `getBookedAttribute()` |
| Виправити логіку вільних місць (`full_free`) | ✅ Змінено метод `getFullFreeAttribute()` |

## Важливі рішення (ADR)

| Рішення | Чому | Альтернативи |
|---------|------|--------------|
| `prebooked` входить до "бронь" | Попереднє бронювання — це активна бронь, не вільне місце | Вважати `prebooked` окремо |
| `returned` і `annulled` не займають місце | Квиток, який повернули або аннулювали, звільняє місце назад | Вважати їх "займаючими" |
| Використати `whereNotIn` на Collection | `ticket_stats()->get()` повертає Collection, не Query Builder | Змінити на query builder (складніше) |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Вільні місця надмірно зменшувались на `returned` і `annulled` квитки | Замінити `where('status', '!=', cancelled)` на `whereNotIn('status', [cancelled, returned, annulled])` |
| `prebooked` квитки не враховувались у лічильнику бронювань | Змінити `whereIn` на включення обох статусів: `[BOOKED, PREBOOKED]` |

## Артефакти

- **Файл:** `app/Entities/System/Trip.php`
  - Метод `getFullFreeAttribute()` (~рядок 483) — виправлена логіка вільних місць
  - Метод `getBookedAttribute()` (~рядок 595) — додано `prebooked` статус
- **Колонки списку рейсів:**
  - `full_free` — усі місця мінус квитки зі статусом ≠ `[cancelled, returned, annulled]`
  - `sold` — тільки `sold` (`Trip::getSoldAttribute()`)
  - `booked` — `booked` і `prebooked` (`Trip::getBookedAttribute()`)
  - `book_payment` — тільки `book_with_payment_at_boarding` (`Trip::getBookPaymentAttribute()`)

## Пов'язані нотатки
- [[onchul-trips]] — загальна архітектура рейсів
- [[onchul-ticket-statuses]] — статуси квитків у системі
