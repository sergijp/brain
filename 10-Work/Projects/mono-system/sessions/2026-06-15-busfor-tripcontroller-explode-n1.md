---
title: "Проект: mono-system — Busfor TripController: фікс explode TypeError + N+1"
date: 2026-06-15
tags: [mono-system, work, session, busfor, laravel, performance, bugfix]
category: session
project: mono-system
status: completed
aliases: []
pinecone_indexed: false
---

# Busfor TripController — explode TypeError + N+1 оптимізація

## Мета сесії
- Production-помилка: `explode(): Argument #2 ($string) must be of type string, array given` у `TripController.php:140`.
- Після фіксу — метод `pointConnectSucces()` дуже довго відпрацьовував.

## Виконано

### 1. Фікс TypeError (explode на масиві)
- **Файл:** `app/Services/Api/v1/Busfor/Http/Controllers/TripController.php`
- **Причина:** `getDaysBySettingsRoute()` має поліморфний return:
  - **рядок** (`"1,2,3..."`, `"P"`, `"U"`) — для `TYPE_EVERY_DAY` / `TYPE_EVEN` / `TYPE_ODD` / `TYPE_CHOOSE`;
  - **масив** (`['day_start','day_end','depth','type'=>'OD']`) — коли `setting_type` truthy, але без явного типу (діапазон дат);
  - **null** — інакше.
- Рядок 140 беззастережно викликав `explode(',', ...)` → падіння на OD-маршрутах.
- **Рішення:** `'days' => is_string($days) ? explode(',', $days) : $days`.

### 2. Фікс N+1 (продуктивність)
- Метод робив лазі-завантаження на кожному кроці:
  - `$route->prices()->get()` — запит на кожен маршрут;
  - `$station->from` / `$station->to` — лазі-load на кожну ціну;
  - `$station->route` — лазі-load маршруту на кожну ціну (хоча це той самий `$route`);
  - `getDaysBySettingsRoute()` — виклик на кожну станцію (результат однаковий у межах маршруту).
- **Рішення:**
  - Constrained eager load: `->with(['prices' => fn($q) => $q->...->with(['from','to'])])`.
  - Використано наявний `$route` замість `$station->route`.
  - `$days` обчислюється один раз на маршрут.
- **Результат:** з ~`1 + N×(1 + 3×M)` запитів → ~4 запити загалом.

## Важливі рішення (ADR)
| Рішення | Чому |
|---|---|
| `is_string()` guard перед `explode` | `getDaysBySettingsRoute` повертає string\|array\|null; OD-маршрути дають масив |
| Constrained eager load замість лазі | Усунення N+1, фільтри перенесено в замикання `with` |
| Обчислення `$days` один раз/маршрут | Дні однакові в межах маршруту — зайві виклики прибрано |

## Проблеми й як вирішили
- **OD-маршрути:** поле `days` тепер повертає об'єкт (`day_start`/`day_end`/`depth`/`type`), а не масив днів. ⚠️ Питання контракту Busfor-API лишається відкритим — технічно падіння усунуто, але семантику поля варто узгодити.

## Артефакти
- `app/Services/Api/v1/Busfor/Http/Controllers/TripController.php` — метод `pointConnectSucces()` (рядки ~118–150).

## Пов'язані нотатки
- [[project-overview]]
