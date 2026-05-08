---
title: "buktrek — Visson мульти-тенант logistics SaaS"
date: 2026-05-08
tags: [buktrek, work, project, visson, laravel, multi-tenancy]
category: project
project: buktrek
status: active
stack: ['Laravel 11', 'Vue 3', 'Vite 6', 'MySQL 5.7', 'Redis', 'Passport', 'Horizon', 'Reverb']
aliases: ["buktrek-overview", "buktrek-project", "VissOn"]
pinecone_indexed: false
---

# buktrek (VissOn) — multi-tenant logistics SaaS

**Пріоритет:** активний  
**Домен:** Carrier/Load/Application management для перевізників

> **Не плутати з [[bustrek/project-overview|bustrek]]** — це окремий проект.

## 🛠 Технічний стек

- **Backend:** PHP 8.2+, Laravel 11, MySQL 5.7, Redis, Laravel Passport (OAuth2), Laravel Horizon, Laravel Reverb (WebSockets)
- **Frontend:** Vue 3, Vite 6, Vuex 4, Vue Router 4, Bootstrap 5.3, Socket.io
- **Multi-tenancy:** пакет `tenancy/tenancy` — System DB + per-tenant DB

## 🏗 Архітектурні документи

Точка входу — [[docs/INDEX]]. Активні топіки:

- [[docs/multi-tenancy]] — System DB vs Tenant DB, `OnTenant` trait, теки міграцій
- [[docs/application-flow]] — Application → Steps → Files → RemoveProblem
- [[docs/mobile-api]] — `app/Services/AppApi/` структура, Passport-токени
- [[docs/db-conventions]] — Індекси, FileUploadService, Carrier↔Member email

## 📦 Домен

**Сутності:** Carriers, Transports, Trailers, Drivers, Loads, Applications (заявки), Contracts (PDF)

**Multi-tenant поділ:**
- System DB → глобальний конфіг, websites
- Tenant DB → carrier/load/application data per website

## 🔐 Auth

Mobile clients — Laravel Passport (OAuth2), маршрути префіксу `/app/*`. Деталі — [[docs/mobile-api]].

## Пов'язані

- [[docs/INDEX]] — карта арх-документації
- Сесії: `~/MyVault/10-Work/Projects/buktrek/sessions/`
- Auto-memory pointer'и: `~/.claude/projects/-Users-serhiin-Data-Source-buktrek/memory/`
