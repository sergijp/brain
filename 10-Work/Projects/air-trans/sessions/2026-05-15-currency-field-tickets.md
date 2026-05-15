---
title: "Проект: air-trans — Поле валюти в квитках + ClientField label keys"
date: 2026-05-15
tags: [air-trans, work, session, tickets, currency, frontend, backend]
category: session
project: air-trans
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

1. Додати підтримку кастомних ключів перекладу для лейблів у `ClientField.vue`
2. Додати поле валюти (select з settings) поруч з ціною у квитках
3. Скрізь де передається валюта — брати з квитка або fallback EUR

## Виконано

### ClientField — кастомні translation keys
- `ClientField.vue`: лейбли тепер читають `field.phoneLabelKey` / `field.nameLabelKey` з fallback на `crud.client_phone` / `crud.client_name`
- `TicketsCrudController.php`: передаються `phoneLabelKey` і `nameLabelKey` у визначення поля `client`

### Поле валюти у квитках

| Файл | Зміна |
|------|-------|
| `database/migrations/2026_05_15_000000_add_currency_to_tickets_table.php` | nullable string `currency` після `price` |
| `app/Entities/System/Directories/Ticket.php` | `currency` у `$fillable` |
| `database/seeders/SettingsTableSeeder.php` | запис `currencies = 'UAH,USD,EUR'` |
| `TicketsCrudController.php` | select_from_array поле `currency`, options з `config('settings.currencies')`, default — перша зі списку |
| `lang/uk/crud.php` | `settings_keys.currencies = 'Валюти (через кому)'` |

### Mail класи — валюта з квитка
- `TicketsSold.php` і `TicketsBooked.php`: замінено хардкод `'UAH'` на `$this->order->tickets()->value('currency') ?? 'EUR'`

## Важливі рішення

| Рішення | Обґрунтування |
|---------|---------------|
| `config('settings.currencies')` замість `Setting::get()` | AppServiceProvider кешує всі settings у config на старті — швидше і без зайвого імпорту |
| `translation_key = value` для валют | Валютні коди (UAH/EUR/USD) не потребують перекладу, `$t('UAH')` повертає 'UAH' |
| `->value('currency')` для mail | Ефективніше ніж `->first()?->currency` — один SQL-запит без гідрації моделі |

## Артефакти

- `database/migrations/2026_05_15_000000_add_currency_to_tickets_table.php`
- `resources/js/crud/base/fields/ClientField.vue`
- `app/Mail/Admin/Tickets/TicketsSold.php`
- `app/Mail/Admin/Tickets/TicketsBooked.php`

## Проблеми й як вирішили

- `config('settings.currencies')` повертав `[]` — запис у БД був відсутній. Вирішено вставкою через UI/тінкер вручну (data-міграцію відхилили)
- Хук `READ-BEFORE-EDIT` спрацьовував повторно — усі редагування проходили успішно, хук є попередженням

## Пов'язані нотатки

- [[ticket-validation-fixes]]
- [[trips-dispatcher-architecture]]