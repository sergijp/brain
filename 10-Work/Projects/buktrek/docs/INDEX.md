---
title: "buktrek — Архітектурні документи"
date: 2026-05-08
tags: [buktrek, architecture, index]
category: docs
project: buktrek
status: active
aliases: ["buktrek-docs", "buktrek-architecture"]
pinecone_indexed: false
---

# buktrek — Архітектурні документи

Точка входу до системної документації проекту Buktrek (VissOn) — multi-tenant logistics SaaS.

## Активні документи

- [[multi-tenancy]] — System DB vs Tenant DB, `OnTenant` trait, теки міграцій, контекстне правило.
- [[application-flow]] — Application → Steps (DB-конструктор) → Files → RemoveProblem.
- [[mobile-api]] — `app/Services/AppApi/` структура, Passport-токени, маршрути `/app/*`.
- [[db-conventions]] — Індекси, `FileUploadService` (транслітерація), Carrier↔Member email uniqueness.

## Граф залежностей

```
project-overview
   ├─ multi-tenancy        ← фундамент усього
   ├─ application-flow     ← головний бізнес-процес (carrier-app)
   ├─ mobile-api           ← AppApi для водіїв
   └─ db-conventions       ← правила для нових міграцій
```

## Пов'язані

- [[project-overview]]
- Tier-2 pointer'и: `~/.claude/projects/-Users-serhiin-Data-Source-buktrek/memory/`
- Сесії: `~/MyVault/10-Work/Projects/buktrek/sessions/`
