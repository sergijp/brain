---
title: "Проект: Buktrek — sendEmail оновлення статусу брокера"
date: 2026-05-06
tags: [work, session, bustrek]
category: work
project: bustrek
status: completed
pinecone_indexed: false
---

## Мета сесії
Доробити метод `sendEmail` в `ApplicationsCrudController`: якщо в реквесті прийшов `recipient_type = 'broker'`, після відправки листа оновлювати поле `broker` заявки на `sent_broker`.

## Виконано

| Задача | Результат |
|--------|-----------|
| Додати константу `RECIPIENT_TYPE_BROKER` до моделі `Application` | Додано `const RECIPIENT_TYPE_BROKER = 'broker'` |
| Оновити `sendEmail` для зміни статусу брокера | Після відправки перевіряє `recipient_type` та `application_id`, якщо є обидва — оновлює `broker` на `STATUS_BROKER_SENT_BROKER` |

## Важливі рішення (ADR)

| Рішення | Обґрунтування |
|---------|---------------|
| `recipient_type` та `application_id` не обов'язкові | Метод `sendEmail` використовується і для інших отримувачів, не тільки брокера |
| Порівняння через константу `RECIPIENT_TYPE_BROKER` | Уникаємо magic strings у контролері |

## Артефакти

- `app/Entities/System/Content/Application.php` — додано `const RECIPIENT_TYPE_BROKER = 'broker'`
- `app/Http/Controllers/Api/Crud/Content/ApplicationsCrudController.php` — оновлено метод `sendEmail` (рядки ~2015–2032)

## Пов'язані нотатки
- [[2026-05-06-remove-problem]]
