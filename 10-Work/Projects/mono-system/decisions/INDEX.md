---
title: "mono-system — Architectural Decision Records"
date: 2026-07-29
tags: [mono-system, adr, index]
category: docs
project: mono-system
status: active
aliases: ["mono-system-adr", "mono-system-decisions"]
pinecone_indexed: false
---

# mono-system — ADR Index

Архітектурні рішення по mono-system. Формат — `YYYY-MM-DD-<short-slug>.md` за шаблоном `~/MyVault/templates/Project-Decision-ADR.md`.

## Активні рішення

| Дата | Slug | Суть |
|------|------|------|
| 2026-07-29 | [[2026-07-29-one-order-per-journey]] | Подорож з пересадками = один ордер, плечі через `parent_id` у межах ордера |

## Як заводити ADR

1. Скопіюй `~/MyVault/templates/Project-Decision-ADR.md` сюди як `YYYY-MM-DD-<slug>.md`.
2. Заповни контекст, рішення, альтернативи, наслідки.
3. Додай рядок у цей INDEX.
4. У session-нотатці, де прийнято рішення, постав wiki-link на ADR замість inline-таблиці.

## Пов'язані

- [[../docs/INDEX]]
- Шаблон: `~/MyVault/templates/Project-Decision-ADR.md`
