---
title: "bustrek — Startrek buses temporary points"
date: 2026-04-19
tags: [work, project, visson, legacy, bustrek]
category: work
project: bustrek
status: archived
stack: [legacy]
pinecone_indexed: false
---

# bustrek — Startrek buses temporary points

**Пріоритет:** LOW / довідник  
**Група:** В — legacy  
**Домен:** Buses reservation / booking (Backpack)

## 🗺 Огляд

4 139 файлів — найбільша legacy-копія. Стек: Laravel 7 + Backpack CRUD + Vue mix з jQuery. Активно точкові правки 02/2026. Джерело для міграцій (див. Busfor інтеграцію).

## 🛠 Стек

- **Laravel:** `^7.0`
- **PHP:** `^7.2.5`

## 📦 Репозиторій

- **Remote:** `git@github.com:VissOn/startrek-buses-point.git`
- **Branch:** `transfer`
- **Last commit:** 2026-02-13

## 📊 Розмір

- **Файлів:** 4 139
- **Міграцій:** 34
- **Найбільші контролери:**
  - `BusforService.php` — 708 рядків
  - `ReservationController.php` — 701 рядків

## 🎯 Дії

- [ ] Використовувати як довідник для Busfor-інтеграції у vts
- [ ] Не тягти у visson/core — несумісний стек (Backpack)
- [ ] Розглянути заморозку після міграції потрібної логіки у mono-system

## 🔗 Пов'язані нотатки

- [[visson-ecosystem/project-overview|🗺 MOC: Visson Ecosystem]]
