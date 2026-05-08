---
title: "Multi-tenancy — System DB vs Tenant DB"
date: 2026-05-08
tags: [buktrek, architecture, multi-tenancy, laravel]
category: docs
project: buktrek
status: active
aliases: ["buktrek-multi-tenancy", "buktrek-tenancy"]
pinecone_indexed: false
---

# Multi-tenancy — System DB vs Tenant DB

Buktrek (VissOn) — multi-tenant logistics SaaS на пакеті `tenancy/tenancy`. Кожен tenant (website) має ізольовані дані.

## Розподіл

| | System DB | Tenant DB (per-website) |
|---|---|---|
| Призначення | Глобальний конфіг, websites, settings, sms_templates | Carrier/Load/Application per-tenant |
| Models у | `app/Entities/System/...` | `app/Entities/Tenant/...` |
| Migrations у | `database/migrations/` | `database/migrations/tenant/` |
| Trait | `SystemConnection` (або стандартний) | `OnTenant` |

## Ключові правила

1. **Завжди визначай контекст** перед створенням моделі/міграції: System чи Tenant.
2. **Tenant model** — додавати `OnTenant` trait, міграція в `database/migrations/tenant/`.
3. **System model** — стандартне підключення або `SystemConnection`.
4. **Якщо сумніваєшся** — перевір existing моделі у тій самій теці.

## Mobile App API (AppApi)

Уся логіка для мобільного застосунку водіїв — у `app/Services/AppApi/`. Це **Tenant-context** (квитки, заявки), auth через Laravel Passport. Структура: `Controllers/`, `Services/`, `Requests/`, `Resources/`, `Middleware/`, `Traits/`, `routes.php`. Маршрути префіксуються `/app`.

Деталі — [[mobile-api]].

## Сесії, де це згадувалось

- `~/MyVault/10-Work/Projects/buktrek/sessions/` — пошук по тегу `multi-tenancy`

## Пов'язані

- [[INDEX]]
- [[application-flow]]
- [[mobile-api]]
- [[db-conventions]]
