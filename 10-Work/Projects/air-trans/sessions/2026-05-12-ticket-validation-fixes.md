---
title: "Проект: air-trans — Фікси валідації квитків"
date: 2026-05-12
tags: [air-trans, work, session, backend, validation, bug]
category: session
project: air-trans
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Виправити три баги, пов'язані зі створенням та редагуванням квитків: помилка NULL при delivery, хибне переповнення автобуса при редагуванні, неправильний підрахунок місць для дітей до 2 років.

## Виконано

| Задача | Результат |
|--------|-----------|
| `count_adults` NULL для delivery-квитка | Додано мутатор `setCountAdultsAttribute` у `Ticket.php` — `null → 0` |
| Помилка переповнення автобуса при редагуванні | Виправлено `ignoreTicketId` у `TicketsRequest.php` |
| Дитина до 2 років займала місце при перевірці | Виправлено `requestedSeats` у `CheckBusCapacity.php` |
| `TicketResource` — відсутнє поле кількості місць | Додано `seats_count` через `$ticket->seatsCount()` |

## Важливі рішення (ADR)

> [[2026-05-12-ticket-validation-fixes]] — немає окремого ADR, рішення прості та очевидні

| Рішення | Обґрунтування |
|---------|---------------|
| Мутатор замість дефолту в БД | Покриває всі місця збереження без міграції |
| `request()->route('id')` замість `$this->route('id')` | `TicketsRequest` інстанціюється через `new`, а не DI-контейнер |
| `request()->get('type_children')` у правилі | Правило завжди викликається в контексті HTTP-запиту |

## Проблеми й як вирішили

### 1. SQLSTATE NULL для count_adults (delivery)
- **Причина:** `TicketsRequest` дозволяє `nullable` для delivery, але ніде не підставлявся 0
- **Рішення:** Мутатор `setCountAdultsAttribute($value) { return $value ?? 0; }` у моделі

### 2. Помилка «автобус переповнений» при редагуванні
- **Перша спроба:** `$this->route('ticket')` → параметр маршруту `{ticket}` не існує (є `{id}`)
- **Друга спроба:** `$this->route('id')` → `TicketsRequest` створюється через `new`, не DI, тому `$this->route()` = null
- **Фінальне рішення:** `request()->route('id')` — глобальний хелпер має доступ до route-параметрів

### 3. Дитина до 2 років рахувалась як місце
- **Причина:** `requestedSeats = count_adults + count_children` без відрахування small_child
- **Рішення:** Перевірка `type_children` з реквесту, аналогічно до `seatsCount()` у моделі

## Артефакти

| Файл | Зміна |
|------|-------|
| `app/Entities/System/Directories/Ticket.php` | `setCountAdultsAttribute` — null→0 |
| `app/Http/Requests/CRUD/Content/TicketsRequest.php` | `request()->route('id')` як ignoreTicketId |
| `app/Rules/CheckBusCapacity.php` | small_child відраховується з requestedSeats |
| `app/Http/Resources/System/TicketResource.php` | поле `seats_count` |

## Пов'язані нотатки

- [[2026-04-20-ticket-checked-nullable]] — попередній фікс nullable для checked
- [[2026-04-21-trips-dispatcher-refactor]] — архітектура диспетчера