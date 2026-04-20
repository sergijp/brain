---
title: "Проект: Buktrek — Аудит індексів БД"
date: 2026-04-20
tags: [work, session, database, buktrek, mysql]
category: work
project: bustrek
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії
Підключитись до локальної MySQL (Valet) і перевірити стан індексів бази `buktrek`.

## ✅ Виконано
- Знайдено MySQL бінарник Homebrew: `/usr/local/Cellar/mysql@5.7/5.7.44_1/bin/mysql`
- Підключено до бази `buktrek` (host: 127.0.0.1, user: root, пароль порожній)
- Проведено повний аудит індексів: FK, дублікати, таблиці без індексів
- Створено і виконано 3 міграції з відсутніми індексами

## 🔑 Важливі рішення (ADR)
| Рішення | Причина | Альтернатива |
|---------|---------|-------------|
| Додати індекс на `deleted_at` в `applications` | SoftDeletes: `WHERE deleted_at IS NULL` на кожен запит | — |
| Індекс на `status`, `loading_date`, `archive` | Основні поля фільтрації в списках | — |
| Індекс на `number` в transports/trailers | Поле для пошуку по номеру авто | — |

## 🐛 Проблеми й як вирішили
### Проблема: `mysql` не в PATH
- **Контекст**: команда `mysql` не знайдена, Valet встановлює через Homebrew
- **Вирішення**: знайдено через `find`, повний шлях `/usr/local/Cellar/mysql@5.7/5.7.44_1/bin/mysql`

### Проблема: GROUP BY помилка (sql_mode=only_full_group_by)
- **Контекст**: MySQL 5.7 strict mode при запиті до `information_schema`
- **Вирішення**: додано всі колонки в GROUP BY

## 📎 Артефакти
- `database/migrations/2026_04_20_000001_add_indexes_to_applications_table.php`
- `database/migrations/2026_04_20_000002_add_indexes_to_customers_table.php`
- `database/migrations/2026_04_20_000003_add_indexes_to_transports_trailers_table.php`

## 🔗 Пов'язані нотатки
- [[10-Work/Projects/bustrek/project-overview]]