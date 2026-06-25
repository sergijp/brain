---
title: "onchul — Reports: додано prebooked та booked статуси"
date: 2026-06-23
tags: [onchul, work, session, bug-fix, reports]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
Перевірити, чи звіти у статусі `prebooked` не потрапляють у ендпоінт `system/reports/preview-generate`.

## Виконано

| Задача | Результат |
|--------|-----------|
| Діагностика root cause багу з preview-generate | ✅ Знайдено: хардкоджений вайтліст статусів без `prebooked` та `booked` |
| Фікс `ReportsController::getTickets()` | ✅ Додано обидва статуси до фільтра |
| Code style check (Pint) | ✅ Без змін |

## Важливі рішення (ADR)

| Рішення | Чому | Альтернативи |
|---------|------|--------------|
| Додано `prebooked` та `booked` до вайтлісту статусів | Статуси були просто забуті при створенні хардкодженого фільтра, а не навмисно виключені | Винести всі статуси у config; генерувати вайтліст динамічно |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Ендпоінт `system/reports/preview-generate` не включав квитки у статусі `prebooked` та `booked` | Дослідив `ReportsController::getTickets()` → знайшов хардкоджений фільтр `->whereIn('status', ['sold', 'returned'])` → додав обидва статуси |

## Артефакти

- Файли: `app/Http/Controllers/Api/System/ReportsController.php` (рядки ~188–193)
- Команди: `./vendor/bin/pint` (без змін)
- Затримані зміни: 2 статуси додано до фільтра в методі `getTickets()`

## Пов'язані нотатки
- [[onchul — Architecture — Reports API]]
- [[onchul — Ticket Statuses]]
