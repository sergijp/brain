---
title: "Проект: buktrek — фікс падіння пошуку в круді applications (Carbon)"
date: 2026-09-22
tags: [buktrek, work, session, crud, search, bugfix]
category: session
project: buktrek
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Пошук у круді `applications` падав, коли в рядок пошуку вводили номер авто або номер причепа. На проді:

```
Carbon\Exceptions\InvalidFormatException
Could not parse 'SM03ASP': Failed to parse time string (SM03ASP) at position 0 (S)
```

## Виконано

| Задача | Результат |
|---|---|
| Знайти причину | `ModelsHelper::applySearchQuery()` (`app/Crud/Helpers/CrudPanel/ModelsHelper.php:58`) проганяє рядок пошуку через `searchLogic` **усіх** колонок. Датові колонки `loading_date`, `date_unloading`, `cmr_date` викликали `Carbon::parse($search)` без перевірки → виняток валив увесь запит |
| Перевірити пошук по transport/trailer | `searchLogic` по `transport.number` / `trailer.number` був коректний (`ApplicationsCrudController.php:534-572`) — просто до нього не доходило виконання |
| Фікс | Три датові `searchLogic` замінені на `self::dateSearchLogic($column)`; доданий приватний `parseSearchDate()` — whitelist форматів `Y-m-d`, `d.m.Y`, `d/m/Y`, `d-m-Y`, `d.m.y` через `Carbon::createFromFormat('!'.$format)` у try/catch + перевірка зворотним форматуванням |
| Перевірка | `php -l` чистий; tinker на локальній БД: «CE 1415 AM» → 1 заявка без винятку, «22.09.2026» → умова `loading_date = 2026-09-22`, «SM03ASP»/«AA1234BB» → лише умова по `transport.number` |

## Важливі рішення

| Рішення | Чому |
|---|---|
| Whitelist форматів замість `try/catch` навколо `Carbon::parse` | `parse` на числовому рядку («12») не падає, а трактує його як час і підставляє **сьогоднішню** дату — тобто пошук по числу домішував усі сьогоднішні заявки. Whitelist знімає і краш, і хибні збіги |
| Перевірка зворотним форматуванням (`$date->format($format) === $search`) | `createFromFormat` мовчки нормалізує переповнення: «32.13.2020» ставало валідною датою |
| Фікс локально в `ApplicationsCrudController`, а не глобальний `try/catch` у `ModelsHelper` | Ловити виняток у загальному місці маскувало б реальні помилки інших `searchLogic` |
| Pint не проганяти по файлу | `./vendor/bin/pint` переформатував увесь файл (~200 рядків діфа, `'%' . $s` → `'%'.$s`). Відкотив, лишив тільки змістовну правку |

## Проблеми й як вирішили

- **`Carbon::createFromFormat` кидає виняток, а не повертає `false`** (на відміну від `DateTime::createFromFormat`) — обгорнуто в `try/catch (\Throwable)` з `continue`.
- **`Carbon::getLastErrors()` ненадійний** у PHP 8.2 (може повертати `false`) — відмовився на користь перевірки зворотним форматуванням.

## Артефакти

- `app/Http/Controllers/Api/Crud/Content/ApplicationsCrudController.php` — рядки 323, 373, 717 (виклики) + приватні `dateSearchLogic()` / `parseSearchDate()` у кінці класу
- Trello: картка «Applications: пошук падає на не-датових запитах (Carbon InvalidFormatException)» → Done

## Пов'язані нотатки

- [[project-overview]]
