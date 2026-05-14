---
title: "ADR: Global Scope vs Local Scope для Route Access Control"
date: 2026-05-14
tags: [3g, adr, architecture, scope, laravel]
category: decision
project: 3g
status: accepted
---

## Контекст

Потрібно обмежити доступ restricted users до Trip моделі по route_id. Розглядались два підходи.

## Рішення

**Global scope `RouteAccessScope` на `Trip` моделі.**

## Причина

Local scope вимагав ручного `->accessibleBy(auth()->user())` в кожному місці де є `Trip::query()`. Легко пропустити нові endpoints (Busfor API, звіти, віджети). Global scope працює автоматично скрізь.

## Ризики та мітигація

- `request()->user()` в Jobs/CLI → null-check на початку scope → no-op → безпечно
- `CreateTicketJob` встановлює user через `request()->setUserResolver()` → `withoutGlobalScope` в job
- Майбутній Octane → потенційна проблема (відкладено)

## Наслідки

- `RouteAccessService` зареєстрований як singleton
- Мемоізація `getAllowedRouteIds()` через `private array $cache`
- `canAccessRoute()` в BookingService прибрано як зайве
