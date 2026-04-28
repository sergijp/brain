---
title: "Проект: Buktrek — фікс валідації email перевізника"
date: 2026-04-28
tags: [work, session, buktrek]
category: work
project: buktrek
status: completed
pinecone_indexed: false
---

## Мета сесії
Виправити помилку при збереженні перевізника: помилка "email має бути унікальним" показувалась як toast-повідомлення замість поля форми. Потрібно було вирішити, чи прибрати унікальність взагалі, чи виправити валідацію.

## Виконано
| Задача | Результат |
|--------|-----------|
| Дослідити де накладено uniqueness на email | Email унікальний на рівні `members.email`, не `carriers.email` |
| Виправити валідацію в `CreateCarrierRequest` | Додано `Rule::unique('members', 'email')` — помилка тепер на полі форми |
| Прибрати дублюючу перевірку з контролера | Видалено блок з `status => error` з `beforeCreateAction` |

## Важливі рішення (ADR)
| Рішення | Альтернативи | Причина |
|---------|-------------|---------|
| Залишити email унікальним | Дозволити дублі; окремий логін від email | Один перевізник = один логін; дублі ламають аутентифікацію |
| Валідація через `Rule::unique('members')` | Валідація по `carriers.email` | Реальна uniqueness у таблиці `members`, не `carriers` |

## Проблеми й як вирішили
- **Проблема:** Перевірка унікальності була в `beforeCreateAction` і поверталась як `NotyResource` (toast), а не field error — юзер не розумів яке поле заповнено неправильно
- **Рішення:** Перенесено у `FormRequest` через стандартний Laravel `Rule::unique`

## Артефакти
- `app/Http/Requests/CRUD/Directories/CreateCarrierRequest.php` — додано `Rule::unique('members', 'email')`
- `app/Http/Controllers/Api/Crud/Content/CarriersCrudController.php` — прибрано дублюючу перевірку

## Пов'язані нотатки
- [[bustrek/sessions/2026-04-20-db-index-audit]]