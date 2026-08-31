---
title: "mono-system — Архітектурні документи"
date: 2026-07-29
tags: [mono-system, architecture, index]
category: docs
project: mono-system
status: active
aliases: ["mono-system-docs", "mono-system-architecture"]
pinecone_indexed: false
---

# mono-system — Архітектурні документи

Точка входу до системної документації mono-system — Laravel-система продажу автобусних квитків.

## Активні документи

- [[connection-search]] — Transfers v2: BFS по хабах, денормалізація `departure_at`/`arrival_at`, чотири шляхи розсинхрону, прапорець `transfers_v2_enabled`.
- [[transfers-v2-admin-guide]] — розмітка хабів адміном: де галочка, правило «всі станції міста», команда `transfers:mark-hubs`, чому стиковка може не з'явитись.
- [[bussystem-ticket-sync]] — синк квитків через офіційний `get_tickets`: вікна дат, матриця статусів, каскад скасування на друге плече пересадки, пастки `TicketScope`/`parent_id`, черга `redis-long` і ланцюжок таймаутів.
- [[app-api]] — API мобільного застосунку (`/api/v1/app`): чому клієнт ходить під власним токеном, whitelist у `Gate::before`, правило видимості квитків у `TicketScope`, пастки з `LiqPay` і `profile/*`.

## Граф залежностей

```
project-overview
   ├─ connection-search              ← пошук стиковок (Transfers v2)
   │     ├─ transfers-v2-admin-guide ← що з цим робить адмін
   │     └─ ADR: one-order-per-journey   ← модель зберігання подорожі
   ├─ bussystem-ticket-sync          ← імпорт квитків із зовнішнього API
   │     └─ (спирається на parent_id/childTicket з transfers v2)
   └─ app-api                        ← API мобільного застосунку пасажира
         └─ ADR: client-ticket-visibility  ← хто бачить квиток
```

## Пов'язані

- [[project-overview]]
- [[../decisions/INDEX]]
- Сесії: `~/MyVault/10-Work/Projects/mono-system/sessions/`
- Шаблон арх-документу: `~/MyVault/templates/Project-Architecture-Doc.md`
