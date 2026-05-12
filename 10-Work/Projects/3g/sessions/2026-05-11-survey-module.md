---
title: "Проект: 3g — Модуль опитувань (Surveys)"
date: 2026-05-11
tags: [3g, work, session, surveys, crud]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

# Модуль опитувань (Surveys)

## Мета сесії

Створити модуль опитувань для збору фідбеку:
1. CRUD у адмінці (title, questions JSON, active)
2. Публічна сторінка `/survey/{hash?}` — рендеримо активні опитування; хеш ідентифікує юзера (опціонально)
3. Збереження відповідей юзерів — **поза скоупом** (наступна задача)

## Виконано

| Задача | Результат |
|---|---|
| Міграція `surveys` | `database/migrations/2026_05_11_120000_create_surveys_table.php` (id, title, questions json, active, timestamps, softDeletes, index по active) |
| Eloquent модель | `app/Entities/Tenant/Survey.php` (cast'и `questions=>array`, `active=>boolean`, scope `active()`) |
| Stateless hash сервіс | `app/Services/SurveyHashService.php` — HMAC-SHA256 з purpose-tag `survey:` + base64url. Без БД, stateless, з integrity check |
| Form Requests | `app/Http/Requests/Survey/{Create,Update}SurveyRequest.php` з Spatie permission check (`surveys-create` / `surveys-update`) |
| CrudController | `app/Http/Controllers/Api/Crud/SurveysCrudController.php` (list/create/update/delete/toggle-active) за зразком `SmsTemplatesCrudController` |
| Frontend контролер | `app/Http/Controllers/Frontend/SurveyController.php` — декодує hash (якщо є) → знаходить User → віддає Blade |
| Blade view | `resources/views/frontend/survey/show.blade.php` — порожня (вимога юзера: лише передача даних, верстка пізніше) |
| Routes | `api.php` (crud + toggle-active), `web.php` (`GET /survey/{hash?}` з `throttle:60,1`) |
| Permissions | `surveys-{create,read,edit,update,delete,toggle-active}` через сідер |
| Vue admin | `crud-routes.js`, `sidebar-router.js`, `breadcrumbs.js`, `api-bridge.js` — всі 4 точки додано |
| Translations | `lang/{uk,en}/{base,crud}.php` |

## Важливі рішення (ADR)

| # | Рішення | Альтернатива | Чому |
|---|---|---|---|
| 1 | JSON-колонка `questions` (array of `{question, answers[]}`) | Окремі таблиці `survey_questions` / `survey_answers` | Перша ітерація без агрегацій; нормалізація буде при додаванні `survey_responses` |
| 2 | Hash = `base64url("survey:{id}|hmac_sha256(payload, app_key)")` — без БД | Поле `users.hash` у таблиці | Юзер вимагав авто-генерацію без таблиці; stateless + integrity guaranteed |
| 3 | `Survey` у `app/Entities/Tenant/` | `app/Entities/System/` | Бізнес-сутність комунікації з клієнтом (буде FK на user_id/ticket_id у наступній ітерації), не інфраструктура |
| 4 | Окремий `SurveyHashService` | Статичні методи на User | Project rule: business logic → `app/Services/`. Тестується unit-тестом без RefreshDatabase |
| 5 | Hash payload з purpose-tag `survey:` | Просто `{user_id}` | Захист від cross-purpose attack якщо з'явиться інший hash-роут |
| 6 | Frontend route БЕЗ `auth.client` middleware | З auth.client | Hash сам по собі — capability token; auth.client зламає UX з SMS/email лінків |
| 7 | Hash optional (`{hash?}`) | Обов'язковий | Юзер запитав щоб працювало і без хешу — показуємо всі активні опитування без юзер-контексту |

## Проблеми й як вирішили

| Проблема | Рішення |
|---|---|
| **🔥 Видалив всі permissions в БД** через `php artisan db:seed --class=PermissionsTableSeeder` — а сідер першим рядком робить `Permission::query()->delete()`. Це поламало `role_has_permissions` через FK cascade | Запис у `/Users/serhiin/Data/Source/3g/CLAUDE.md` як **CRITICAL RULES**: ніколи не запускати сідери. Для permissions — або поштучно `permission:create-permission`, або окрема міграція з `Permission::firstOrCreate`. Roles треба відновити вручну або з бекапу |
| `TypeError: breadcrumbs[key] is not a function` — не додав `surveys` у `resources/js/config/breadcrumbs.js` | Додав entry поряд із sms-templates |
| `TypeError: Cannot read properties of undefined (reading 'crudInfo')` — не додав у `api-bridge.js` | Додав `...CrudApi('surveys')`. Це **головний пропуск** — skill `laravel-crud` явно вимагає api-bridge.js, але я пропустив під час реалізації |
| Reviewer знайшов: `trans('crud.question')` повертав масив (ключ зайнятий nested-структурою у `lang/uk/crud.php:1429`) | Перейменував на `crud.survey_question` |
| Reviewer знайшов: `UpdateSurveyRequest::authorize()` використовував `surveys-edit` замість `surveys-update` (project pattern) | Виправлено на `surveys-update` |

## Артефакти

### Створені файли
- `database/migrations/2026_05_11_120000_create_surveys_table.php`
- `app/Entities/Tenant/Survey.php`
- `app/Services/SurveyHashService.php`
- `app/Http/Requests/Survey/CreateSurveyRequest.php`
- `app/Http/Requests/Survey/UpdateSurveyRequest.php`
- `app/Http/Controllers/Api/Crud/SurveysCrudController.php`
- `app/Http/Controllers/Frontend/SurveyController.php`
- `resources/views/frontend/survey/show.blade.php`

### Змінені файли
- `CLAUDE.md` — додано CRITICAL RULES блок (ніколи не запускати сідери)
- `routes/api.php`, `routes/web.php`
- `database/seeders/PermissionsTableSeeder.php`
- `resources/js/api-bridge.js`
- `resources/js/router/crud-routes.js`
- `resources/js/router/sidebar-router.js`
- `resources/js/config/breadcrumbs.js`
- `lang/{uk,en}/base.php`, `lang/{uk,en}/crud.php`

### Команди
```bash
php artisan migrate                          # OK — migration ran
./vendor/bin/pint app/... database/...        # 7 files formatted
# ❌ php artisan db:seed --class=PermissionsTableSeeder  ← НЕ РОБИТИ. Видалило permissions
```

### Hash service smoke test
```
hash: c3VydmV5OjQyfGZkNzM2YjBhNmVmMGViNTZiYjNkYzVkZTkwYTEwZWFkZWMwZmZiMTc4YmJkODU3YzJhNDQxMDQ1MjkxZDVlNDE
decoded: 42
tampered: NULL
invalid: NULL
```

### Routes registered
- 10 CRUD admin routes (`api/system/surveys/*`)
- 1 public: `GET /survey/{hash?}` → `Frontend\SurveyController@show`

## Не входило (наступні задачі)

- POST endpoint для збереження відповідей (таблиця `survey_responses` + ідемпотентність "1 юзер — 1 відповідь")
- Розмітка питань на публічній Blade-сторінці (зараз порожня)
- Звіт по результатах у адмінці (агрегація по варіантах)
- Розсилка лінків через SMS/email шаблони (placeholder типу `[survey_link]` за зразком `[map_link]`)
- Відновлення `role_has_permissions` після інциденту з сідером

## Залишкові ризики

- **Стабільні ID для question/answer у JSON** — ddd-architect рекомендував додати UUID/int id зараз, я цього не зробив. Доведеться додати при імплементації `survey_responses`, інакше зміна порядку питань після збору відповідей зламає агрегації.
- **Roles → permissions assignments** треба відновити після інциденту з сідером.

## Пов'язані нотатки

- [[2026-05-01-sms-templates-refactor]] — патерн CrudController на якому базувалися
- [[2026-05-08-map-link-short-url]] — `ShortLinkController` як референс публічного роуту з токеном
- План: `~/.claude/plans/mellow-honking-yeti.md`