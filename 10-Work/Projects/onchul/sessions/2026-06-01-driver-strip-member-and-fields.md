---
title: "Проєкт: onchul — спрощення Driver: зрізано member + поля, 2 баги телефону/чекбокса"
date: 2026-06-01
tags: [onchul, work, session, refactoring, driver]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

# onchul — Driver: видалення полів і привʼязки до member

## Мета сесії

Гілка `migrate_refact`. Поетапно «роздягнути» сутність `Driver` від зайвих полів і повністю вирізати привʼязку до облікового запису (`member`/авторизація). Кожен крок — окремо, з підтвердженням обсягу через AskUserQuestion. Наприкінці — два суміжні баги, які спливли по ходу.

## Виконано

| Крок | Результат |
|------|-----------|
| **passports** | Прибрано масив паспортів повністю: поле в create/update, `$fillable`/`$casts`/`getMainPassportAttribute`/докблок/`logOnly` у `Driver`, колонка в міграції, правила/повідомлення в `Create/UpdateDriverRequest`, переклади (`crud.passports`, `fields.add_passport`, nested attr). Фронт: знято реєстрацію типу `passports` у `crud/config/fields.js` + **видалено осиротілий** `PassportsField.vue` |
| **identification_code** | Прибрано всюди (контролер, модель, міграція, реквести, переклади `crud.identification_code`, `validation.identification_code_required`, nested attrs). Це було останнє поле в табі «Документи» → **таб зник цілком**, ключ `crud.documents` теж видалено |
| **is_worked** | Прибрано поле + фільтр + **екшен `toggleIsWorked()`** + маршрут `drivers.toggle-is-worked` (`routes/api.php`) + модель (`$fillable`/`$casts`/докблок/`logOnly`) + колонка + переклади (`crud.has_already_worked`, nested) + право `drivers-toggle-is-worked` (uk/en) |
| **email + member** | **Повне вирізання member** (вибір користувача): поле `email`/`user_email`, `beforeCreateAction` (створення Member), trait-и `GenerateRandomPasswordOperation`/`ChangePasswordOperation` + перевизначені методи → знято й авто-маршрути generate/change-password + кнопки; звʼязок `member()`, акесор `getUserEmailAttribute`, колонка `member_id`+FK, права `drivers-generate-random-password`/`drivers-change-password`. `crud.email` **залишено** (спільний ключ) |
| **cleanup** | У контролері та моделі прибрано закоментований код і невикористані імпорти (`ActivitiesOperation`, Tenant `Role`, два альт-рядки `Carbon::now()->format('YmdHis')`) |
| **bugfix: archive default** | `CheckboxField.setValue(null)` примусово ставив `true` → ігнорувався `'default'=>false`. Фікс: при `null` брати `field.default`, інакше лишати `true` (щоб `active` і далі дефолтив у вкл.) |
| **bugfix: телефон у списку** | `Driver::getMainPhoneAttribute` читав `$mainPhone['value']`, а `PhonesField` зберігає ключ `phone`. Колонка завжди показувала «не вказано». Фікс: `['value']`→`['phone']` (як у `Bus`/`Carrier`/`Agency`/`Insurance`) |

## Важливі рішення

| Рішення | Чому |
|---------|------|
| member вирізано повністю, а не «лише email» | Користувач підтвердив: водій більше не потребує облікового запису. «Не створювати member» логічно тягне за собою мертві операції паролів, звʼязок і `member_id` |
| Колонки прибрано в **оригінальній** create-міграції | Гілка рефакторингу міграцій — спрацює на `migrate:fresh`. Для робочої БД потрібна окрема drop-міграція (відкладено) |
| `CheckboxField` фіксили на рівні компонента, не точково | Поведінка глобально бажана: поважати `default`, fallback `true` — backward-compatible для `active` |
| Bug телефону — одрук ключа, не зміна структури | Усі споріднені сутності читають `['phone']`; у водія була розбіжність |

## Проблеми й як вирішили

- **Закоментований column-блок «знав» про toggle-is-worked** — не плутати з реальним маршрутом: `toggleIsWorked` мав живий запис у `routes/api.php`, тож на кроці cleanup його НЕ чіпали, а видалили вже свідомо на кроці `is_worked`.
- **`crud.email` мало не видалили** — grep показав, що його юзають Tickets/Users/Clients/Insurances + фронт. Залишили.
- **Зовнішніх `$driver->member`** немає (тільки всередині контролера) → безпечно різати. `BookingController` `$order->member` — інша сутність.

## Артефакти

**Backend**
- `app/Http/Controllers/Api/Crud/Community/DriversCrudController.php`
- `app/Entities/System/Community/Driver.php`
- `app/Http/Requests/CRUD/Community/{Create,Update}DriverRequest.php`
- `database/migrations/2025_08_12_111625_create_drivers_table.php`
- `routes/api.php`

**Frontend**
- `resources/js/crud/base/fields/CheckboxField.vue` (фікс default)
- `resources/js/crud/config/fields.js` (знято `passports`)
- видалено `resources/js/crud/base/fields/PassportsField.vue`

**Lang**: `lang/{uk,en}/crud.php`, `validation.php`, `permissions.php`, `fields.php`

## Відкладене (TODO)

1. **Drop-міграція** для робочої БД: `passports`, `identification_code`, `is_worked`, `member_id`(+FK) — бо правки в оригінальній міграції лише для `migrate:fresh`.
2. **Orphan-права** (Spatie): `drivers-toggle-is-worked`, `drivers-generate-random-password`, `drivers-change-password` — зʼясувати механізм сидінгу прав, щоб коректно прибрати.
3. **Перегенерувати** `lang/php_{uk,en}.json` через `php artisan lang:publish` (досі містять старі ключі).
4. **Ребілд фронту** (`npm run dev`/`build`) — для змін у `CheckboxField.vue`/`fields.js`.

## Памʼятка

- Generic-CRUD кличе аксесори динамічно за іменем — `grep` не знайде. Не видаляти наосліп (урок із попередньої сесії: A3-аксесор → `BadMethodCallException`).

## Повʼязані нотатки

- [[2026-06-01-refactoring-backlog-a2-d10]] — попередній крок беклогу (та сама гілка/ефорт)
- [[2026-06-01-laravel12-vue-migration]]
