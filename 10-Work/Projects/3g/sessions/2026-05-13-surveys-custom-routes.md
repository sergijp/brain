---
title: "Проект: 3g — Surveys кастомні роути для Vue компонентів"
date: 2026-05-13
tags: [3g, work, session, surveys, crud, routes]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

# Surveys — кастомні роути і методи

## Мета сесії

Додати кастомні роути і методи до `SurveysCrudController` для використання з кастомними Vue компонентами замість стандартних CRUD операцій create/edit/update.

## Виконано

| Задача | Результат |
|---|---|
| Кастомні роути у `routes/api.php` | 3 нових роути у `/system` prefix group |
| Методи у `SurveysCrudController` | `storeCustom`, `editCustom`, `updateCustom` |
| Pint | 1 style issue fixed (array_indentation) |

## Важливі рішення (ADR)

| # | Рішення | Альтернатива | Чому |
|---|---|---|---|
| 1 | Кастомні роути у `routes/api.php` (не `setupRoutes()`) | Custom Operation Trait | У проєкті немає `setupRoutes()` в контролері — роути реєструються в `api.php` (як toggleActive) |
| 2 | Методи прямо в `SurveysCrudController` | Окремий API контролер | Мінімальний вплив; патерн існуючого `toggleActive` |

## Артефакти

### Нові роути (routes/api.php, /system group)

```php
POST /system/surveys/store-custom   → storeCustom   (can:surveys-create)   name: surveys.store-custom
GET  /system/surveys/{id}/edit      → editCustom    (can:surveys-edit)     name: surveys.edit-custom
PUT  /system/surveys/{id}/update-custom → updateCustom (can:surveys-update) name: surveys.update-custom
```

### Нові методи (SurveysCrudController.php)

```php
storeCustom(CreateSurveyRequest): JsonResponse   // Survey::create(), 201
editCustom(int $id): JsonResponse                // Survey::findOrFail(), 200
updateCustom(UpdateSurveyRequest, int $id): JsonResponse // findOrFail + update, 200
```

### Вхідні дані

**storeCustom:** `title` (required), `questions` (required), `active` (bool, optional)

**updateCustom:** `title` (required), `questions[].question` + `questions[].answers[]` (мін. 2), `active` (bool, optional)

## Пов'язані нотатки

- [[2026-05-11-survey-module]] — базова реалізація модуля Surveys