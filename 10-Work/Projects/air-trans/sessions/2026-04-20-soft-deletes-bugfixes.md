---
title: "Проект: air-trans — Виправлення трьох багів soft-delete"
date: 2026-04-20
tags: [work, session, code, air-trans, laravel, soft-deletes, bugfix]
category: work
project: air-trans
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії

Проаналізувати й виправити три баги, пов'язані з soft-deletes та життєвим циклом водіїв, автобусів і клієнтів:

1. Не відображається назначений водій на поїздці після перепризначення
2. Відображаються лишні заплановані поїздки після видалення автобуса
3. Таблиця `clients` без `deleted_at` — пусті дані в системі, помилка у водія

## ✅ Виконано

- **Баг #1** → `TripsDispatcherCrudController::assignBusDriver` — ключ `updateOrCreate` змінено з `(trip_id, date, driver_id)` на `(trip_id, date, bus_id)`; додано null-safe на `driver_name` у `getFilteredTickets`
- **Баг #2** → створено `app/Observers/BusObserver.php` (cascade soft-delete/restore DTD); зареєстровано в `AppServiceProvider`
- **Баг #3** → міграція `2026_04_20_100000_add_soft_deletes_to_clients_table.php`; `SoftDeletes` trait у `Client.php`; null-safe у `TicketsResource`
- **Регресія від #3** → у `Client::getOrCreateByEmailAndName` і `RegistrationController::registration` додано `withTrashed()` + `restore()` (unique `clients.phone` ламав би створення після soft-delete)
- **Документація** → три файли у `docs/` проєкту (Obsidian-формат із callouts і frontmatter)

## 🔑 Важливі рішення (ADR)

| Рішення | Причина | Альтернатива |
|---------|---------|-------------|
| Ключ DTD `updateOrCreate` = `(trip_id, date, bus_id)` | Перепризначення водія має оновлювати існуючий DTD, а не створювати дубль (інакше квитки тримають стару FK) | Передавати `dtd_id` з UI завжди; деактивувати старі DTD перед створенням |
| Observer на `Bus::deleting` для каскаду DTD | Єдина точка правди: немає автобуса → немає поїздки; працює і на `restored` | `whereHas('bus')` у кожному запиті — неузгоджений стан у БД |
| `Client` з `SoftDeletes` + restore-on-recreate | `phone` UNIQUE → без restore створення падає з constraint violation | Прибрати SoftDeletes і використовувати `is_archived` — інша архітектура |
| `ForgotPassword`/`Login` не відновлюють soft-deleted | Видалений клієнт не має отримати доступ | Відновлювати при логіні — але це дірка в політиці видалення |

## 🐛 Проблеми й як вирішили

### Баг 1: Водій не відображається після перепризначення

- **Контекст**: призначити A → soft-delete A → призначити B → `driver_name=null`
- **Причина**: `updateOrCreate` з `driver_id` у ключі створював **другий** DTD при зміні водія. Квитки тримали `driver_trip_date_id` на старий DTD із soft-deleted водієм. `$dtd->driver` = null (глобальний scope), отже `driver_name` = null. Дубль DTD#2 не показувався через `existingBusIds->contains`
- **Вирішення**: ключ `(trip_id, date, bus_id)` оновлює той самий DTD. Null-safe на випадок DTD, що скидається в null на рядку 451

### Баг 2: Зайві заплановані поїздки після видалення автобуса

- **Контекст**: soft-delete автобуса → та сама поїздка показується двічі (як група квитків + planned)
- **Причина**: `Bus::whereIn` виключає soft-deleted → група з `bus_id=null`. DTD блок бере `active=true` з `bus_id=Y` → `existingBusIds->contains` не збігається → додається дубль. FK `nullOnDelete`/`cascadeOnDelete` не спрацьовують при Eloquent SoftDeletes
- **Вирішення**: `BusObserver::deleting` каскадно soft-delete DTD; `restored` відновлює

### Баг 3: Таблиця clients без deleted_at

- **Контекст**: hard-delete клієнта → `$this->client->name` на null → PHP error у системі, пусті дані у водія
- **Причина**: Client не мав SoftDeletes. `TicketsResource` звертався без `?->`
- **Вирішення**: міграція `softDeletes()`, trait `SoftDeletes`, null-safe у resource
- **Регресія**: `phone` UNIQUE → створення після soft-delete падало. Виправлено `withTrashed()->restore()` у двох точках створення

## 📎 Артефакти

- Контролер: `app/Http/Controllers/Api/Crud/TripsDispatcherCrudController.php` (рядки 463, 489-499)
- Observer: `app/Observers/BusObserver.php` (новий)
- Provider: `app/Providers/AppServiceProvider.php`
- Модель: `app/Entities/System/Directories/Client.php`
- Resource: `app/Http/Resources/TicketsResource.php`
- Auth: `app/Http/Controllers/Api/Auth/RegistrationController.php`
- Міграція: `database/migrations/2026_04_20_100000_add_soft_deletes_to_clients_table.php`
- Документація: `docs/bugfix-driver-reassignment-after-delete.md`, `docs/bugfix-planned-trips-after-bus-delete.md`, `docs/bugfix-clients-soft-deletes.md`

## 🔗 Пов'язані нотатки

- [[10-Work/Projects/air-trans/project-overview]]

## 📝 Дії після merge

```bash
php artisan migrate
```

## 💡 Вивчене / на майбутнє

> [!note] Патерн для soft-deletes + unique
> Якщо модель має `SoftDeletes` і водночас unique-колонку — у всіх точках створення треба `withTrashed()->first()` і `restore()` при знайденні. Інакше unique violation після soft-delete.

> [!note] Каскад soft-deletes
> FK `cascadeOnDelete`/`nullOnDelete` у міграції НЕ спрацьовують при Eloquent SoftDeletes — потрібні Observer-и.