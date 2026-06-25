---
title: "Проект: onchul — import-clients memory_limit debug"
date: 2026-06-25
tags: [onchul, work, session, debugging, memory, queue]
category: session
project: onchul
status: completed
aliases: [onchul-clients-import-memory-debug, vts-clients-import-64m]
pinecone_indexed: false
---

# onchul: import-clients memory_limit Debug

## Мета сесії

Зʼясувати, чому artisan-команда імпорту клієнтів `php artisan clients:import-from-old` на локалі залила ~24 000 клієнтів, а на проді — лише ~5 000, незважаючи на наявність повного набору даних (35 874 рядків у `old_clients`).

## Виконано

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Прочитати та аналізувати код команди `ImportClientsFromOld.php` | Команда синхронна, insert-only, без чергової обробки. Жодного LIMIT/take у коді немає. |
| 2 | Перевірити, чи є жорстко закодовані ліміти на вставку | Спростовано: помітив 35 874 читання, чанки по 1000, але видимих лімітів на 5000 немає. |
| 3 | Перевірити наявність і повноту `old_clients` на проді | Dry-run показав: Rows read **35874**, Unique phones **22380**, Would insert **24133** → джерело повне. |
| 4 | Перевірити гіпотезу про Guard «Table not empty» | Спростовано: `--fresh` скидає таблицю, але навіть після цього вставилось лише 5000, проблема лишилась. |
| 5 | Перевірити UNIQUE-constraint на phone | Спростовано: `SHOW INDEX FROM clients WHERE Non_unique=0` — лише PRIMARY(id); UNIQUE на phone НЕМАЄ. |
| 6 | Діагностувати тихий збій за exit-кодом | **ROOT CAUSE ЗНАЙДЕНО:** Exit code 255 → fatal PHP error, memory_limit вичерпано. |
| 7 | Підтвердити: запустити з `memory_limit=-1` | **Результат: SUCCESS** → залилось повні **24 133** клієнти за 15–20 сек. |

## Важливі рішення (ADR)

| # | Питання | Рішення | Чому |
|---|---------|---------|------|
| 1 | Як обійти проблему на проді без переписування коду? | Запускати команду з `php -d memory_limit=-1 artisan clients:import-from-old --fresh` | Швидкий фікс; код залишається у готівці; на проді пам'ять дозволяє, це не постійна проблема. |
| 2 | Чому `dry-run` не спіймав падіння по памʼяті? | `--dry-run` скипує БД-операції (`if (! $dryRun)`) але все одно нагромаджує весь масив `$byPhone` у RAM. Це оманливість. | dry-run діагностує логічні помилки, але НЕ контролює рантайм-ресурси (пам'ять, диск, час). Для повної валідації потрібен реальний запуск. |

> **Майбутнім ADR кандидат:** переписування команди на streaming-insert (вставляти прямо під час `chunk()`, без накопичення у RAM) + гарна обробка помилок для запобігання тихим частковим імпортам.

## Проблеми й як вирішили

- **Проблема:** Команда вставляє 24 133 рядки на локалі, але лише 5000 на проді. Виглядає як жорсткий ліміт, але де?
  - **Причина:** `php.ini` на проді: `memory_limit = 64M`. Команда тримає в RAM одночасно весь масив `$byPhone` (22 380 записів) + 35 874 читані рядки. На проді пам'ять вичерпувалась посеред фази вставки, PHP генерував fatal error «Allowed memory size exhausted», exit код 255. У таблиці залишалось рівно ~5000 (5 успішних чанків по 1000). Збій **тихий**: `laravel.log` нічого не записував (PHP-fatal при нестачі пам'яті не має ресурсу зробити запис); у консолі видно тільки прогрес-бар читання, потім тиша + exit.
  - **Фікс:** Запуск з `php -d memory_limit=-1 artisan clients:import-from-old --fresh` → лімітів нема → залилось **24 133** клієнти ✅

## Артефакти

- **Файл команди:** `app/Console/Commands/ImportClientsFromOld.php`
  - Метод обробки: chunk-читання з `old_clients` → нормалізація телефону → дедуплікація за `$byPhone` → bulk insert чанками по 1000
  - Guards: TRUNCATE без `--fresh` → відмова; `--dry-run` → логіка без БД

- **Діагностичні SQL-команди:**
  ```sql
  SELECT COUNT(*) FROM clients;
  SELECT COUNT(*) FROM old_clients;
  SHOW INDEX FROM clients WHERE Non_unique=0;
  SELECT phone, COUNT(*) as cnt FROM clients GROUP BY phone HAVING cnt > 1;
  ```

- **Робочий спосіб запуску на проді:**
  ```bash
  php -d memory_limit=-1 artisan clients:import-from-old --fresh
  # або скидання значення у php.ini на проді на більше значення (512M+ для комфорту)
  ```

- **Перевірка exit-коду локально:**
  ```bash
  php artisan clients:import-from-old --fresh
  echo "EXIT CODE: $?"  # 0 на локалі, 255 на проді до фіксу
  ```

## Важливі побічні знахідки

1. **Dry-run оманливий:** помітив `Would insert 24133`, але реальний import не виконується. Це дає хибну впевненість у коректності. Сам по собі dry-run не виловлює проблеми пам'яті, timeout, disk-space.

2. **Команда insert-only без append-режиму:** якщо `clients` непорожня, вимагає `--fresh` або кидає відмову. Немає режиму «додати нові, пропустити дублікати».

3. **Тихий отказ при нестачі ресурсів:** частковий імпорт з exit 255 залишає таблицю у невизначеному стані (5000 прислано, 19133 чекають). Виправимо — потрібен механізм повного rollback на помилку або streaming-insert.

## Пов'язані нотатки

- [[10-Work/Projects/onchul/project-overview]]
- [[10-Work/Projects/onchul/docs/INDEX]]
- Memory profiling & optimization (майбутня нотатка)
- Queue & async jobs architecture (як переписати на Job-based батч)
