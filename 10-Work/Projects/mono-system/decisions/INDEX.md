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
| 2026-08-24 | [[2026-08-24-client-ticket-visibility]] | Свій квиток для клієнта = він оформив ордер АБО він пасажир на ордері, оформленому не клієнтом |
| 2026-09-17 | [[2026-09-17-ticket-short-links]] | Посилання на квиток для пасажира — короткий код `/t/{code}` з терміном дії до прибуття, а не прямий PDF у `/storage` |
| 2026-09-17 | [[2026-09-17-transfer-hub-access]] | Пересадку можна відкрити поіменному списку користувачів; дефолт — бачать усі, закритий хаб для стороннього виглядає як «не хаб» |
| 2026-09-21 | [[2026-09-21-app-api-additive-contract]] | Контракт застосунку розширюється адитивно в наявних `/api/v1/app/*`, без v2; дедлайн броні — лише для броней, оформлених клієнтом |

## Як заводити ADR

1. Скопіюй `~/MyVault/templates/Project-Decision-ADR.md` сюди як `YYYY-MM-DD-<slug>.md`.
2. Заповни контекст, рішення, альтернативи, наслідки.
3. Додай рядок у цей INDEX.
4. У session-нотатці, де прийнято рішення, постав wiki-link на ADR замість inline-таблиці.

## Пов'язані

- [[../docs/INDEX]]
- Шаблон: `~/MyVault/templates/Project-Decision-ADR.md`
