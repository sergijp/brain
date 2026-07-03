---
title: "Проект: onchul — команда імпорту квитків зі старої бази vonchul"
date: 2026-07-03
tags: [onchul, work, session]
category: session
project: onchul
status: completed
pinecone_indexed: false
---

## Мета сесії

Розробити artisan-команду `tickets:import-from-old` для перенесення квитків зі старої бази перевізника vonchul (MySQL, та сама інстанція) у нову систему VTS. Старі маршрути й нові поки не пов'язані (маршрути — у конфігу). Потрібна ідемпотентність, валідація з логуванням причин пропусків, режим аналізу й режим імпорту.

### Контекст

- **Стара база vonchul:** 67,858 квитків (2020-06…2026-09), 38,090 клієнтів, 2,924 рейси, один маршрут Братислава ↔ Чернівці
- **Схема vonchul:** flights (id=1,2 основні) → trips (140 записів) → booking (квитки) → clients
- **Нова система VTS:** api_trip_id, api_number, note у Ticket; config/crud.php для маршрутів
- **Вимога:** тільки майбутні квитки (datetimeFrom ≥ сьогодні)

---

## Виконано

| Задача | Результат |
|--------|-----------|
| Дослідження vonchul схеми (таблиці, обсяги, статуси) | ✅ Виконано через Explore агент |
| Дослідження VTS інтеграційних точок (Ticket.php, crud.php) | ✅ Виконано через Explore агент |
| Конфіг database.php + mysql_old + .env.example | ✅ Виконано |
| Файл config/old-import.php (маршрути, міста) | ✅ Створено (2 маршрути, 4 станції замапані, ~47 очікує) |
| OldTicketsImportService (бізнес-логіка з валідацією) | ✅ Створено |
| Команда tickets:import-from-old (аналіз / --import) | ✅ Створено |
| Helpers/NormalizesOldContactData (normalizePhone, splitName) | ✅ Створено (спільний з ImportClientsFromOld) |
| Модифіковано Ticket.php ($fillable + api_number, api_trip_id, note) | ✅ Виконано |
| Написано 29 нових тестів (Feature + Unit) | ✅ Створено; весь suite 46 тестів зелений |
| Виправлено 2 баги (phone matching, phone NULL) | ✅ Виправлено |
| Тестування на реальних даних vonchul | ✅ Прогнано (830 квитків, route_mapping_missing, таблиця відсутніх рейсів) |

---

## Важливі рішення (ADR)

| Рішення | Чому | Альтернативи |
|---------|------|--------------|
| Ідемпотентність за (api_trip_id, place) | ticketnumber пустий у ~35%, дублюється між напрямками; api_trip_id + place унікально | ticketnumber (ненадійний) |
| print=1 → sold, інакше booked | print — ознака оплати в старій базі; не кожен старий квиток підтвердив оплату у перевізника | Усі як booked (потребує підтвердження) |
| Маршрути в config/old-import.php, не hard-code | База vonchul — тестова; реальну заллють пізніше; легше оновити конфіг | Hard-code у сервісі (неелегантно для future updates) |
| client_id NULL якщо не знайдено + ПІБ/телефон у note | Не втратити інформацію про клієнта, але дозволити системі шукати user-match потім | Відкидати квиток (втрата даних) |

---

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| **Phone matching:** OldTicketsImportService шукав "+380...", Client::setPhoneAttribute зберігає без префіксу → ніколи не матчило UA номери | Пошук по обох варіантах: пошук за "+380..." AND пошук за "380..." + перевірка обох форматів в json phones колоні |
| **TypeError на null phone:** Ticket::phone non-nullable мутатор, null phone з vonchul валив весь прогін на persist(); import 0/830 | phone не передається в create() коли null; додано try/catch на кожен booking; збій → skip-лог з причиною error:... + лічильник imported тільки після успішного persist() |

---

## Артефакти

### Файли

**Нові:**
- `config/old-import.php` — маршрути (flight_id → route_id), міста (текст → station_id)
- `app/Services/OldTicketsImportService.php` — читання vonchul чанками, валідація, пошук клієнтів, Orders+Tickets транзакція
- `app/Console/Commands/ImportTicketsFromOld.php` — команда tickets:import-from-old (аналіз / --import), прогресбар, таблиці результатів
- `app/Helpers/NormalizesOldContactData.php` — trait normalizePhone(), splitName() (спільна с ImportClientsFromOld)
- `tests/Feature/Import/ImportTicketsCommandTest.php` — тести команди (2 сценарії)
- `tests/Feature/Import/OldTicketsImportServiceTest.php` — тести сервісу (12 сценаріїв)
- `tests/Unit/Helpers/NormalizesOldContactDataTest.php` — тести helper (15 сценаріїв)

**Модифіковані:**
- `config/database.php` — додано mysql_old conexão
- `app/Models/Ticket.php` — додано $fillable: api_trip_id, api_number, note
- `.env.example` — додано DB_OLD_DATABASE, DB_OLD_HOST

### Команди

```bash
# Режим аналізу (сухий запуск)
php artisan tickets:import-from-old

# Режим імпорту
php artisan tickets:import-from-old --import

# Логи пропусків
cat storage/app/import/2026-07-03-vonchul-import-skipped.csv
```

### Тести

```bash
# Запуск усіх 46 тестів
./vendor/bin/phpunit

# Тільки нові імпорт-тести
./vendor/bin/phpunit tests/Feature/Import/
./vendor/bin/phpunit tests/Unit/Helpers/NormalizesOldContactDataTest.php
```

### Лог прогону (реальні дані vonchul)

```
Майбутніх квитків: 830
Аналіз:
  ✅ Готові до імпорту: 0
  ⏭️  Route mapping missing: 830 (очікується 2 маршрути в config/old-import.php)
  🚫 Station not mapped: 0 ( 47 станцій потребують маппінгу)
  
Відсутні рейси (найпалючіші дати):
  2026-07-15: 42 квитків
  2026-07-16: 18 квитків
  ... (85 дат всього)
```

---

## Наступні кроки

Коли реальна база vonchul буде залита:

1. **Маршрути:** вписати 2 flight_id → route_id у `config/old-import.php` (Братислава ↔ Чернівці)
2. **Станції:** домапити ~47 станцій (текст → station_id). Увага: Пряшів / Prešov — два написання
3. **Прогін:** `php artisan tickets:import-from-old` (аналіз) → `php artisan tickets:import-from-old --import` (імпорт)
4. **Перевірка:** таблиця результатів, CSV skip-логи у `storage/app/import/`

---

## Пов'язані нотатки

Майбутньо:
- [[Трекер рефакторингу]] — додати як задачу завершення маппінгу станцій
- [[Система прав/ролей]] — можуть знадобитися permission checks у команді (currently open)
