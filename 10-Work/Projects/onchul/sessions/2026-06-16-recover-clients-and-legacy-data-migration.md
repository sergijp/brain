---
title: "Проект: onchul — відновлення таблиці clients та міграція legacy-даних"
date: 2026-06-16
tags: [onchul, work, session, database, migration, data-recovery]
category: session
project: onchul
status: in-progress
aliases: []
pinecone_indexed: false
---

# onchul — відновлення `clients` та перенос legacy-таблиць

## Мета сесії

1. Відновити випадково видалену (DROP TABLE) таблицю `clients` на локальній dev-базі.
2. Перенести дані зі старої таблиці `old_clients` у відновлену `clients` (написати artisan-команду).
3. Оцінити, чи можна перенести `old_buses` / `old_carriers` без окремої команди.

## Виконано

| Задача | Результат |
|--------|-----------|
| Відновлення `clients` | ✅ Структуру відновлено з міграцій (дані втрачені — сидера немає) |
| Команда переносу `old_clients → clients` | ✅ `clients:import-from-old`, імпортовано 24 133 рядки |
| Доопрацювання команди (чистка) | ✅ Пропуск name-як-телефон, іноземні номери без `+`, `--dry-run` |
| Аналіз `old_buses → buses` | ✅ Достатньо даних — простий `INSERT…SELECT` без змін схеми |
| Аналіз `old_carriers → carriers` | ⏸️ На паузі — user уточнив, що це агенти продажу (зберігаються в `users`), ціль переносу під питанням |

### Деталі відновлення `clients`
- Таблицю знесено через DROP, але **обидва записи міграцій лишались** у таблиці `migrations` → звичайний `php artisan migrate` їх пропускав.
- Рішення: точково `DELETE FROM migrations` для 2 записів (`create_clients_table`, `add_confirmed_at_to_clients_table`), потім `migrate`. Повний `migrate:rollback` був небезпечний (вся БД у batch 1).

### Команда `clients:import-from-old`
- `old_clients` — журнал операторських бронювань (35 874 рядки), без password/email; `name` = повне ПІБ одним полем; масові дублікати по телефону; `phone_pln` = альт-номер.
- Логіка: дедуплікація по нормалізованому телефону (`+380…`), розщеплення імені (1-е слово → `surname`, решта → `name`), альт-номери → JSON `clients.phones`.
- Фінал: 35 874 прочитано → **24 133 вставлено**, 43 пропущено (name був телефоном), 1 753 без телефону (кожен окремо).

## Важливі рішення (ADR)

| # | Рішення | Чому |
|---|---------|------|
| 1 | `clients.password` → nullable | У old_clients паролів немає; чесний NULL замість фейкового хешу |
| 2 | Дедуплікація по нормалізованому phone | Один акаунт на номер; old_clients дублював контакти при кожному замовленні |
| 3 | Розщеплення name: 1-е слово → surname, решта → name | У даних переважає порядок «Прізвище Ім'я» |
| 4 | Нова колонка `clients.phones` (JSON) + cast `array` | Зберегти phone_pln і варіантні номери, нічого не губити |
| 5 | Рядки, де name = телефон → НЕ імпортувати | Брудні дані; критерій: немає літер, ≥9 цифр, ≥70% цифрових символів |
| 6 | Іноземні номери — без `+` (тільки UA `+380…` з `+`) | Узгоджено з user |

## Проблеми й як вирішили

- 🐛 **DROP таблиці + «завислі» записи міграцій** → migrate її ігнорував. Fix: точковий DELETE з `migrations` + migrate.
- 🐛 **MySQL 5.7 `server has gone away` / FD-ліміт** (`FD_SETSIZE=1024`, ~2042 таблиці). Fix: `brew services restart mysql@5.7`; на майбутнє — `open_files_limit=8192`, `table_open_cache=4096` у `my.cnf` (+ можливо `launchctl limit maxfiles`).
- 🐛 **`--fresh` truncate блокувався FK** (`tickets.client_id`, `clients_verify_phone.client_id`). Fix: обгортка `SET FOREIGN_KEY_CHECKS=0/1`. ⚠️ На проді `--fresh` небезпечний — осиротить квитки.

## Артефакти

**Створено:**
- `database/migrations/2026_06_15_120000_make_clients_password_nullable.php`
- `database/migrations/2026_06_15_120100_add_phones_to_clients_table.php`
- `app/Console/Commands/ImportClientsFromOld.php` — `clients:import-from-old [--fresh] [--dry-run]`

**Змінено:**
- `app/Entities/System/Directories/Client.php` — cast `phones => array`, `phones` у `$fillable`

**Команди:**
```bash
php artisan clients:import-from-old --dry-run   # перевірка без запису
php artisan clients:import-from-old --fresh      # truncate + імпорт
brew services restart mysql@5.7                  # лікування FD-ліміту
```

**Не закомічено** — усі зміни в робочому дереві, чекають рев'ю/коміту.

## Стан legacy-таблиць (для наступної сесії)

- `old_buses` (10) → `buses`: ✅ готовий `INSERT…SELECT`, без змін схеми. `owners_id/cards/description/type` губляться (прийнятно).
- `old_carriers` (31) → ⏸️ **відкрите питання**: user каже це «агенти продажу», що зберігаються в `users`, а не перевізники. Треба з'ясувати правильну ціль (`users` з роллю? `members`? `carriers`?). Серед 31 рядка є «Готівка», «АВ Чернівці» — схоже на точки продажу/автовокзали, не людей. Блокери для `carriers`: `email` NOT NULL, `percent` NULL у 4 рядків, `phone`→JSON трансформація.

## Наступні кроки

- [ ] Обговорити доменну ціль для `old_carriers` (users/members/carriers)
- [ ] Виконати перенос `old_buses → buses`
- [ ] (Опц.) feature-тест на `nameLooksLikePhone()` / `normalizePhone()`
- [ ] (Опц.) `reviewer` для команди + коміт
- [ ] Підняти `open_files_limit` у MySQL, щоб FD-ліміт не повторювався

## Пов'язані нотатки

- [[onchul]]
