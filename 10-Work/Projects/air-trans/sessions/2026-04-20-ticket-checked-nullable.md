---
title: "Проект: air-trans — Виправлення nullable checked у квитках"
date: 2026-04-20
tags: [work, session, air-trans]
category: work
project: air-trans
status: completed
pinecone_indexed: false
---

## Мета сесії
Поле `checked` у квитках стало nullable (3 стани замість 2). Потрібно врахувати це при зміні статусу в селекті диспетчера.

## Виконано

| Задача | Результат |
|--------|-----------|
| Null-guard у `getCanTicketStatusesAttribute()` | Якщо `ticket_statuses = null` — повертає всі статуси замість краш |
| Синхронізація `checked` в `updateTicket()` | При зміні `ticket_statuses` через селект оновлює `checked` |
| Виправлення `checkedTicket()` | `null` → `STATUS_TICKET_IN_PROGRESS` замість `STATUS_TICKET_NOT_CHECKED` |
| Переклад `ticket_in_progress` | Додано до `lang/uk/crud.php` |

## Важливі рішення (ADR)

| Рішення | Обґрунтування |
|---------|---------------|
| 3 стани `checked`: `true/false/null` | `null` = в процесі, `true` = явився, `false` = не явився |
| Синхронізація двостороння | `updateTicket` + `checkedTicket` обидва синхронізують обидва поля |
| `match()` замість `if/else` | Явна обробка всіх трьох станів, не покладатись на falsy |

## Проблеми й як вирішили

- **Краш при `ticket_statuses = null`** → null-guard у `getCanTicketStatusesAttribute()`
- **`checkedTicket(null)` → `not_checked`** → `match(true)` з явним `=== null` гілкою

## Артефакти

- `app/Entities/System/Directories/Ticket.php` — `getCanTicketStatusesAttribute()`
- `app/Http/Controllers/Api/Crud/Directories/TicketsCrudController.php` — `updateTicket()`, `checkedTicket()`
- `lang/uk/crud.php` — `ticket_in_progress`

## Пов'язані нотатки
- [[soft-deletes-architecture]]