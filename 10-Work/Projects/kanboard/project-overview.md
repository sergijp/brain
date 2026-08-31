---
title: "kanboard — дошки задач для агентів"
date: 2026-08-06
tags: [work, project, kanboard, agents, infrastructure]
category: work
project: kanboard
status: active
stack: [php, sqlite, valet, go]
pinecone_indexed: false
---

# kanboard — дошки задач для агентів

**Пріоритет:** MEDIUM / інфраструктура
**Домен:** Task tracking для Claude Code агентів

## 🗺 Огляд

Локальні канбан-дошки, куди агенти самі заводять задачі, рухають по статусах і пишуть звіт «зроблено / лишилось». Одна дошка на проект, колонки скрізь однакові: **Backlog → In progress → Review → Done**.

Доступ: **http://tasks.loc** (Valet). Агенти працюють через MCP-сервер `kanboard`, зареєстрований глобально — тобто доступний у кожній сесії без налаштувань по проектах.

## 🛠 Стек

- **Kanboard:** 1.2.53 (PHP 8.2, SQLite)
- **Веб:** Laravel Valet, nginx + php-fpm, TLD `.loc`
- **MCP:** `bivex/kanboard-mcp` (Go 1.25), 171 інструмент

## 📦 Шляхи

- **Kanboard:** `~/Data/Source/kanboard/`
- **MCP-бінарник:** `~/Data/Source/kanboard-mcp/kanboard-mcp`
- **База:** `~/Data/Source/kanboard/data/db.sqlite`
- **Правило для агентів:** `~/.claude/CLAUDE.md`, секція «Дошки задач»

## ⚠️ Відомі обмеження

- **Ізоляції по проектах немає** — агент бачить усі дошки, межу тримає лише правило в CLAUDE.md. Посилюється окремим API-токеном на проект, без коду.
- Пароль адміністратора — стандартний `admin/admin`. Сайт лише локальний, але змінити варто.
- UI скромніший за Trello — усвідомлена плата за те, що стек рідний для оточення.

## 🚀 Плани

Перенесення на VPS під Webuzo — Kanboard є в Softaculous, ставиться кнопкою, стек той самий. Міграція = копія папки та бази.

## Пов'язані

- [[decisions/INDEX]]
- [[2026-08-06-lokalni-doshky-zadach-dlya-agentiv]]
