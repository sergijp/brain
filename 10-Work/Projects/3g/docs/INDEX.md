---
title: "3g — Архітектурні документи"
date: 2026-05-08
tags: [3g, architecture, index]
category: docs
project: 3g
status: active
aliases: ["3g-docs", "3g-architecture"]
pinecone_indexed: false
---

# 3g — Архітектурні документи

Точка входу до системної документації проекту 3G-SITE — клієнтський портал, Laravel 10 + Vue 3.

## Активні документи

- [[app-api]] — API мобільного застосунку пасажира `/api/v1/app`: адаптери над контролерами сайту, токени `ClientApiToken`, 5 middleware.
- [[Modularization-Design]] — Розбиття платформи на CORE + модулі (варіант b, легкий реєстр). Фази 0-6 реалізації.
- [[notifications]] — `SmsTemplate` CRUD + `TicketNotificationService` + AlphaSms (sms/viber) + `ShortLink` + плейсхолдери.
- [[legacy-controllers]] — Стан і план розбиття `TripsCrudController` (1709 ряд.) і `WidgetsController` (1154 ряд.).
- [[busfor-api]] — Аудит провайдера Busfor: контрактні розбіжності зі spec, runtime баги, патчі A-J.
- [[echeck-fiscal]] — Система фіскальних чеків: `ECHECK_DRY_RUN`, SMS-шаблон, 17 тестів.
- [[bus-photo]] — Окреме фото Bus для повідомлень: `StoreImageHelper`, `boot::deleting` хук.
- [[infobus-sync]] — Синхронізація трансферних квитків (часткові фікси у `CreateTicketJob`).
- [[desktop-tauri]] — Research-only: десктоп-обгортка адмінки на Tauri (варіант A, Phase 1-4).

## Граф залежностей

```
project-overview
   ├─ Modularization-Design  ← архітектура (Fase 0-6)
   ├─ notifications          ← SMS/Viber/Telegram інтеграція (модуль Fase-3)
   ├─ legacy-controllers     ← техдовг (паралельний апгрейд L10→L11)
   ├─ busfor-api             ← зовнішня інтеграція (audit, модуль Fase-5)
   ├─ echeck-fiscal          ← фіскалізація (модуль Fase-4)
   ├─ bus-photo              ← окремий photo-флоу для месенджерів
   ├─ infobus-sync           ← трансферні квитки (status: partial, модуль Fase-5)
   └─ desktop-tauri          ← future (research only)
```

## Пов'язані

- [[project-overview]]
- Tier-2 pointer'и: `~/.claude/projects/-Users-serhiin-Data-Source-3g/memory/`
- Сесії: `~/MyVault/10-Work/Projects/3g/sessions/`
