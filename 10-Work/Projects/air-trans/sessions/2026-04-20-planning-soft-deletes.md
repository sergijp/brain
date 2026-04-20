---
title: "Проект: air-trans — Soft-deletes у модулі планування"
date: 2026-04-20
tags: [work, session, air-trans, backend, bug, soft-deletes]
category: work
project: air-trans
status: completed
pinecone_indexed: false
---

## Мета сесії

Розширити раніше зроблені виправлення soft-delete багів (водій/автобус/клієнт) на модуль **планування поїздок** (`PlaningTripsOperation`).

## Виконано

| Задача | Результат |
|--------|-----------|
| Аналіз `PlaningTripsOperation.php` | Знайдено 2 класи проблем |
| Виправлення валідації `driver_id`/`bus_id` | `Rule::exists()->whereNull('deleted_at')` у 3 місцях |
| Виправлення `firstOrCreate` → `withTrashed()->firstOrNew` + `restore()` | Запобігає UniqueConstraint violation |
| Виправлення `DriverTripDateRequest.php` | Аналогічна валідація для ручного CRUD |
| Налаштування глобального `SessionStart` хука | Автозавантаження `MEMORY.md` у контекст |

## Важливі рішення (ADR)

| Рішення | Чому |
|---------|------|
| `Rule::exists('drivers','id')->whereNull('deleted_at')` замість `exists:drivers,id` | Laravel рядковий `exists:` не додає soft-delete фільтр автоматично |
| `withTrashed()->firstOrNew` + `restore()` замість `firstOrCreate` | unique індекс `(driver_id, trip_id, date)` — при спробі INSERT дублю soft-deleted запису — DB Exception |
| Пошукові методи не чіпати | `Driver::query()`, `Bus::query()` — Eloquent global scope вже фільтрує soft-deleted |

## Проблеми й як вирішили

- **Проблема:** `planingTripsGenerate` викликав `firstOrCreate` — якщо DTD був soft-deleted з тим самим `(driver_id, trip_id, date)`, Eloquent намагався INSERT новий запис → UniqueConstraint violation
- **Рішення:** паттерн `withTrashed()->firstOrNew` → `if trashed → restore` → `if !exists → fill + save`

## Артефакти

- `app/Crud/Operations/PlaningTripsOperation.php` — валідація + generate метод
- `app/Http/Requests/CRUD/Directories/DriverTripDateRequest.php` — валідація
- `~/.claude/settings.json` — SessionStart хук для auto-memory

## Пов'язані нотатки

- [[soft-deletes-bus-driver-client]] (попередня сесія з основними виправленнями)
