---
title: "Проект: mono-system — перевірка мерджу master → transfer_v2"
date: 2026-10-07
tags: [mono-system, work, session]
category: session
project: mono-system
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
Перевірити конфлікти мерджу `master` → `transfer_v2` (частину користувач розвʼязав вручну) так, щоб не зламати логіку пересадок v2 і не втратити зміни master.

## Виконано
- `app/Entities/Tenant/Ticket.php` (лишався `UU`): у робочій копії була версія **merge-base**, тобто втрачено ~950 рядків transfer_v2 і правки master. Відновлено з нашого боку (stage :2) і перенесено зміни master:
  - `getTripRouteNumberAttribute()` і `getIsTripCancelledAttribute()` поверх нашого `resolveTripWithTrashed()`; master-версію `tripWithTrashed(): ?Trip` не брали, бо в нас це вже relation `BelongsTo`, eager-load якої використовується;
  - перевірки `isset(time['HH'], time['mm'])` / `time_arrival` у `departure` / `arrival`.
- `Busfor/OrderController::create`: після ручного мерджу лишились **дві** джоби автоскасування (стара `TicketsCanceledReservation::dispatch` і `scheduleAutoCancel`), причому `scheduleAutoCancel` спрацьовував навіть для `can_book`. Тепер лишився один виклик `scheduleAutoCancel()` під `if (!$canBook)`.
- `AppServiceProvider` і `routes/api.php` перевірено: нічого не втрачено.
- Автоматично змерджені партнерські API (Retinfo/TicketReturn/TicketsController) використовують `is_trip_cancelled` / `trip_route_number`. Без відновлення Ticket.php вони б мовчки віддавали `raceNum` = null.

## Проблеми й як вирішили
| Проблема | Рішення |
|---|---|
| Ticket.php = merge-base | відновлено ours + акцесори master |
| подвійне автоскасування в Busfor | один `scheduleAutoCancel` під `!$canBook` |
| тести Transfers падають (392) | не через мердж: локальна БД без міграцій transfer_v2 (Pending) |

## Повторна збірка (після 16:59)
- Ticket.php ще раз перезаписався змішаною версією (1221 рядок, без `journeyHead`, `shortLink`, `canBeReturnedAt`, `qrPayload` тощо), імовірно, з відкритого merge-вікна IDE. Унікальних рядків (ручних правок) у ній не було. Файл зібрано заново (ours + 24 рядки master) і застейджено разом із Busfor OrderController; unmerged = 0.
- Перевірка «нічого не загубилось»: для кожного файлу, зміненого будь-якою гілкою, рядки, додані гілкою, шукались у результаті. Втрати лише свідомі (Ticket.php, Busfor). Файли, видалені в transfer_v2 (`f18cb01b`, tenancy тощо), master не змінював.
- Міграції на локальну БД користувач накочувати не дозволив, тож тести не запускались.

## Артефакти
- Бекап робочої копії до правки: scratchpad `Ticket.working-before-fix.php`
- Smoke у tinker: `trip_name`, `trip_route_number`, `is_trip_cancelled`, `departure`/`arrival` на квитку 147732 — ок.

## Пов'язані нотатки
- [[2026-08-03-transfers-v2-sales-fixes]]
- [[2026-07-30-bussystem-sync-hardening]]
