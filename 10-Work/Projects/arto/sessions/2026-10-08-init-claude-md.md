---
title: "Проект: arto — створення CLAUDE.md"
date: 2026-10-08
tags: [arto, work, session]
category: session
project: arto
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
Проаналізувати кодову базу та створити `CLAUDE.md` для майбутніх сесій Claude Code.

## Виконано
- Проаналізовано структуру: Laravel 11 (старий скелет з Kernel), Vue 3 адмін-SPA, Blade публічний сайт → описано в `CLAUDE.md`.
- Задокументовано власний CRUD-фреймворк (`app/Crud`): макрос `$router->crud()`, трейти операцій, lifecycle `setup*Defaults/setup/setup{Op}Operation`, permissions `{crud}-{action}`, Store/Get pre-processors за назвою типу поля.
- Задокументовано зв'язку з фронтом (`crud-routes.js`, `sidebar-router.js`, `crud/base/*`) і DB-driven сторінки (Page → WidgetPage → `WidgetsData`).

## Важливі рішення (ADR)
| Рішення | Причина |
|---|---|
| Окремо попередити про тести | `phpunit.xml` без sqlite, тести з `RefreshDatabase` зітруть БД з `.env` |

## Проблеми й як вирішили
- Немає.

## Артефакти
- `~/Data/Source/arto/CLAUDE.md`

## Пов'язані нотатки
- [[arto]]
