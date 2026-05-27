---
title: "Проект: 3g — Survey invite via SMS/Viber при закритті станції"
date: 2026-05-26
tags: [3g, work, session, survey, sms, viber]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Реалізувати відправку SMS/Viber запрошень на опитування клієнтам, які доїхали до певної станції, в момент коли станція закривається (marked as arrived).

## Виконано

| Задача | Результат |
|--------|-----------|
| Тестовий роут `GET /api/test/survey-invite/{phone}/{ticket_id}` | Додано в `routes/api.php` — генерує хеш, короткий URL, надсилає SMS/Viber |
| CSRF fix для `/api/survey/submit` | Додано в `VerifyCsrfToken::$except` — Sanctum викликав CSRF для браузерних запитів |
| Migration `add_send_survey_to_routes_table` | Поле `boolean send_survey default(false)` у таблиці `routes` |
| Route модель | `$fillable`, cast `boolean`, `@property bool $send_survey` |
| RoutesCrudController | Checkbox поле `send_survey` на вкладці Settings |
| Переклади | `lang/uk/crud.php` → `'send_survey' => 'Надсилати опитування'`, `lang/en/crud.php` → `'Send survey'` |
| `SendSurveyInviteJob` | Новий job `app/Jobs/Surveys/SendSurveyInviteJob.php` — encode hash → short URL → SmsTemplate::render → AlphaSms |
| Хук в `TripManagementOperation::arrived()` | Dispatch `SendSurveyInviteJob` після закриття станції якщо `route->send_survey = true` |

## Важливі рішення (ADR)

| Рішення | Обґрунтування |
|---------|---------------|
| `to_id = station_id` (не `from_id`) | Опитування отримують ті хто **доїхав** до станції (висадка), а не ті хто **сів** (посадка). `from_id` = посадка, `to_id` = висадка. Echeck навпаки використовує `from_id`. |
| `checked = true` на квитку | Відправляємо тільки тим хто фізично з'явився. Без фільтру по `status` і `phone`. |
| `optional($trip->route)->send_survey` | Eager load `route` доданий до `arrived()`. `optional()` захищає від null якщо route не завантажений. |
| SMS шаблон з ключем `survey_invite` | Плейсхолдер `[survey_link]` — користувач додає вручну через SMS Templates CRUD. |
| `ShortLinkService::shortUrl($url, 30)` | TTL 30 днів для survey посилань (vs 7 днів для тестового роуту). |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| CSRF token mismatch на `/api/survey/submit` | `EnsureFrontendRequestsAreStateful` (Sanctum) в api group вмикає CSRF для браузерних запитів з того ж домену. Додано в `VerifyCsrfToken::$except`. |
| `ticket_id` required при submit без хешу | Тестовий роут змінено: приймає `{ticket_id}` параметром, генерує хеш через `SurveyHashService::encode()`. |
| `Ticket::STATUS_SOLD` не існує | Це статична властивість `Ticket::$STATUS_SOLD`. Але пізніше прибрали цей фільтр — залишили тільки `checked = true`. |

## Артефакти

- `database/migrations/2026_05_26_134458_add_send_survey_to_routes_table.php`
- `app/Jobs/Surveys/SendSurveyInviteJob.php` (новий файл)
- `app/Crud/Operations/TripManagementOperation.php` — метод `arrived()`, рядки ~138+
- `app/Entities/Tenant/Route.php` — fillable, cast, @property
- `app/Http/Controllers/Api/Crud/RoutesCrudController.php` — checkbox поле
- `app/Http/Middleware/VerifyCsrfToken.php` — CSRF except
- `routes/api.php` — тестовий роут + CSRF fix

## Пов'язані нотатки

- [[project_surveys_custom_routes]] — попередня робота по surveys модулю
- [[project_sms_templates_refactor]] — SmsTemplate CRUD, AlphaSms, ShortLinkService
