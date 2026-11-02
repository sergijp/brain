---
title: "Проект: profumo-site — створення CLAUDE.md"
date: 2026-10-15
tags: [profumo-site, work, session]
category: session
project: profumo-site
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
Проаналізувати кодову базу і створити `CLAUDE.md` для майбутніх сесій Claude Code.

## Виконано
- Проаналізовано структуру Laravel 9 + Vue 2 (Vite) вітрини → створено `CLAUDE.md` у корені репо.

## Важливі рішення (ADR)
| Рішення | Причина |
|---|---|
| Явно зафіксовано, що схема БД живе в `../profumo-admin` | у цьому репо лише стандартні міграції Laravel |

## Проблеми й як вирішили
- Немає.

## Артефакти
- `profumo-site/CLAUDE.md`

## Ключові факти про архітектуру
- Моделі — `app/Entities/System/**`, auth-модель `Member`.
- Переклади контенту — трейт `ModelHasTexts` (поліморфні `texts`).
- Settings з БД → `config('settings.*')` на boot.
- Доставка/оплата — класи з колонки `class` у БД, роути реєструються в `AppServiceProvider`.
- Кілька незалежних Vue 2 root-ів на Blade-сторінках, спільний Vuex, `GET /api/bootstrap`.
- Catch-all роут `{page}/{subs?}` — нові web-роути вище нього.

## Пов'язані нотатки
- [[profumo-admin]]
