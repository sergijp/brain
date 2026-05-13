---
title: "Проект: 3g — Survey hash, зберігання відповідей, results endpoint"
date: 2026-05-13
tags: [3g, work, session, survey, questions-module]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Розширити модуль опитувань: хеш з ticket_id, зберігання відповідей у БД, endpoint для перегляду результатів по рейсу.

## Виконано

| Задача | Результат |
|--------|-----------|
| `SurveyHashService` — спрощено до `encode(int $ticketId)` | Хеш ~27 символів (HMAC-8 байт + Base64 URL-safe) |
| Виправлено модель у `SurveyController` | `Member` замість `User`, eager load `order.member` |
| Artisan команда `survey:hash {ticket_id}` | `app/Console/Commands/GenerateSurveyHash.php` |
| Міграції `survey_responses` + `survey_response_answers` | Запущено, таблиці в БД |
| Моделі `SurveyResponse`, `SurveyResponseAnswer` | `app/Entities/Tenant/` |
| Form Request `StoreSurveyResponseRequest` | `app/Http/Requests/Survey/` |
| `SurveyController::submit()` | `POST /api/survey/submit` (routes/api.php) |
| `SurveysCrudController::results()` | `POST /api/system/surveys/results` |
| Top-level кнопка `survey-results` у CRUD | `setupListOperation()` |

## Важливі рішення

Детальні ADR — [[decisions/INDEX]]

- **Тільки `ticket_id` у хеші** — квиток вже містить user_id через `order.member`, дублювати не потрібно
- **HMAC 8 байт замість 32** — хеш для SMS, потрібна коротка форма (~27 символів)
- **Дві таблиці замість JSON** — `survey_responses` + `survey_response_answers` для можливості `AVG(answer)` по `question_id`
- **`ticket_id` UNIQUE** у `survey_responses` — захист від повторного проходження
- **Маршрут submit у `api.php`** — `apiFront` відправляє на `/api/...`, не `web.php`
- **`POST` для results endpoint** — не GET, бо передаються `route_id` + `date` у тілі

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| `MethodNotAllowedHttpException` для `/api/survey/submit` | Маршрут був у `web.php`, перенесено до `api.php` |
| `Undefined class 'User'` у SurveyController | Замінено на `App\Entities\System\Member` |
| Хеш занадто довгий для SMS (~100 символів) | HMAC усічено до 8 байт → ~27 символів |

## Артефакти

```
app/Services/SurveyHashService.php          — encode(ticketId), decode → ?int
app/Console/Commands/GenerateSurveyHash.php — php artisan survey:hash {ticket_id}
app/Entities/Tenant/SurveyResponse.php      — ticket_id, trip_id
app/Entities/Tenant/SurveyResponseAnswer.php — response_id, question_id, type, answer
app/Http/Requests/Survey/StoreSurveyResponseRequest.php
app/Http/Controllers/Frontend/SurveyController.php — submit()
app/Http/Controllers/Api/Crud/SurveysCrudController.php — results()
database/migrations/2026_05_13_115940_create_survey_responses_table.php
database/migrations/2026_05_13_121048_create_survey_response_answers_table.php
```

**API endpoints:**
- `POST /api/survey/submit` → `{ticket_id, answers[]}` → `{success, average_rating, google_maps_rating}`
- `POST /api/system/surveys/results` → `{route_id, date}` → `{trip_id, responses_count, averages, answers}`

## Пов'язані нотатки

- [[2026-05-13-surveys-custom-routes]] — попередня сесія по surveys (storeCustom/editCustom/updateCustom)
- [[2026-05-11-survey-module]] — початкова реалізація модуля