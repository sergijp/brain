---
title: "gt-admin-new — Visson адмін (нова версія)"
date: 2026-04-19
tags: [work, project, visson, legacy, gt-admin-new]
category: work
project: gt-admin-new
status: archived
stack: [legacy]
pinecone_indexed: false
---

# gt-admin-new — Visson адмін (нова версія)

**Пріоритет:** LOW / заморозити  
**Група:** В — legacy  
**Домен:** E-commerce / orders / shop admin

## 🗺 Огляд

Рік без commits. Гілка `template_import` → незавершений імпорт шаблонів. Кандидат на заморозку.

## 🛠 Стек

- **Laravel:** `^9.19`
- **PHP:** `^8.0.2`

## 📦 Репозиторій

- **Remote:** `git@github.com:VissOn/gt-admin-new.git`
- **Branch:** `template_import`
- **Last commit:** 2024-04-22

## 📊 Розмір

- **Файлів:** 1 176
- **Міграцій:** 125
- **Найбільші контролери:**
  - `OrderCrudController.php` — 921 рядків
  - `OrderROCrudController.php` — 476 рядків

## 🎯 Дії

- [ ] Заморозити до read-only
- [ ] Логіку Order*Controller зберегти як довідник

## 🔗 Пов'язані нотатки

- [[visson-ecosystem/project-overview|🗺 MOC: Visson Ecosystem]]
