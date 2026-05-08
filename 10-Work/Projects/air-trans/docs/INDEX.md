---
title: "air-trans — Архітектурні документи"
date: 2026-05-08
tags: [air-trans, architecture, index]
category: docs
project: air-trans
status: active
aliases: ["air-trans-docs", "air-trans-architecture"]
pinecone_indexed: false
---

# air-trans — Архітектурні документи

Точка входу до системної документації проекту. Кожен топік — окремий файл у цій теці.

## Активні документи

- [[driver-trip-date-system]] — DTD-модель: ідентичність `(trip,date,bus)`, observers, soft-deletes, матриця видалень.
- [[trips-dispatcher-controller]] — Диспетчерський екран: TICKET_EAGER, контракти `is_planned`, типи DATE/DATETIME.

## Граф залежностей

```
project-overview
   ├─ driver-trip-date-system  ← ядро DTD/Ticket
   └─ trips-dispatcher-controller  ← споживач DTD
```

## Пов'язані

- [[project-overview]]
- Tier-2 pointer'и: `~/.claude/projects/-Users-serhiin-Data-Source-air-trans/memory/`
- Сесії: `~/MyVault/10-Work/Projects/air-trans/sessions/`
