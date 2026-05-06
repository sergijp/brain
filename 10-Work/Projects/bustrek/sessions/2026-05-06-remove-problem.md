---
title: "Проект: buktrek — Зняття прапора проблеми з заявки"
date: 2026-05-06
tags: [work, session, bustrek]
category: work
project: bustrek
status: completed
pinecone_indexed: false
---

## Мета сесії

Реалізувати функцію зняття статусу "проблема" з заявки. Фронтенд (`api-bridge.js`) вже мав метод `removeProblemFromApplication`, але бекенд-роут і метод були відсутні.

## Виконано

| Задача | Результат |
|--------|-----------|
| Додати роут | `POST /application/{id}/remove-problem` у `routes/api.php`, middleware `can:applications-edit` |
| Додати метод контролера | `ApplicationsCrudController::removeProblem(int $id)` — скидає `is_problem = false`, `note` не змінює |
| Уникнути дублювання | Метод НЕ додавався до `AppApi/Services/ApplicationService.php` (той сервіс лише для мобільного AppApi) |

## Важливі рішення (ADR)

| Рішення | Обґрунтування |
|---------|---------------|
| Логіка inline у контролері, а не у сервісі | `ApplicationService` використовується тільки `MemberController` (AppApi). Аналогічно до `toggleArchive`. |
| `note` залишається незмінним | Бізнес-вимога: зняти прапор проблеми, але повідомлення зберегти |

## Артефакти

- `routes/api.php` — новий роут ~рядок 103
- `app/Http/Controllers/Api/Crud/Content/ApplicationsCrudController.php` — метод `removeProblem`
- `resources/js/api-bridge.js` — метод `removeProblemFromApplication` (вже існував)

## Пов'язані нотатки

- [[2026-04-21-application-steps-module-planning]]