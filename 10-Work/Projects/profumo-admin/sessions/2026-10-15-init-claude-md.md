---
title: "Проект: profumo-admin — створення CLAUDE.md"
date: 2026-10-15
tags: [profumo-admin, work, session]
category: session
project: profumo-admin
status: completed
aliases: []
pinecone_indexed: false
---

# profumo-admin — створення CLAUDE.md

## Мета сесії
Проаналізувати кодову базу й створити `CLAUDE.md` для майбутніх сесій Claude Code.

## Виконано
- Проаналізовано стек: Laravel 9 API (Passport, spatie permission/activitylog) + Vue 2.7 SPA на Vite.
- Задокументовано власний CRUD-фреймворк: макрос `Route::crud`, operation-трейти, життєвий цикл `CrudController`, `crudInfo` як контракт з фронтом, Get/Store preprocessors за конвенцією імен, translatable-поля.
- Зафіксовано, що multi-tenant режим вимкнений (README успадкований від Bustrek).
- Створено `CLAUDE.md` у корені репо.

## Важливі рішення (ADR)
| Рішення | Причина |
|---|---|
| Tenancy описано як вимкнену, без інструкцій вмикати частково | пакет відсутній у composer.json, listeners закоментовані |

## Проблеми й як вирішили
- README описує інший проект (Bustrek) — у CLAUDE.md позначено це явно.

## Артефакти
- `~/Data/Source/profumo-admin/CLAUDE.md`

## Пов'язані нотатки
- [[profumo-site]]
