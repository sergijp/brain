---
title: "Проект: bustrek — дизайн модуля Application Steps (DB-конструктор кроків водія)"
date: 2026-04-21
tags: [work, session, bustrek, planning, application-steps]
category: work
project: bustrek
status: completed
pinecone_indexed: false
---

## Мета сесії
Скласти план переведення статичного `config/steps.php` (кроки AppApi для водія) у керований через адмінку і кабінет перевізника DB-конструктор. Розбити на короткі таски і зберегти у `docs/application-steps/`.

## Виконано
- Проаналізовано існуючу систему: `ApplicationStepsResource.php:57`, `ApplicationListResource.php:53`, `config/steps.php`, константи `Application::DRIVER_STATUS_*`.
- Обговорено і погоджено **18 архітектурних рішень**.
- Створено повну документацію:
  - `docs/application-steps/README.md` — головний таск, 18 рішень, граф залежностей, таблиця тасок.
  - `docs/application-steps/tasks/01..11*.md` — 11 підтасок.
- План затверджено: `~/.claude/plans/replicated-baking-turtle.md`.
- Записано у auto-memory: `project_application_steps_module.md`.

## Важливі рішення (ADR)

| # | Рішення | Чому |
|---|---------|------|
| 1 | БД зберігає **лише override-и per-carrier** | Zero-downtime: існуючі перевізники автоматом читають `config/steps.php` |
| 2 | Резолвер **2-рівневий**: БД → config | Немає потреби у сідері і глобальних дефолтах у БД |
| 3 | `carrier_id` — **NOT NULL** | MySQL composite unique з NULL не спрацьовує коректно |
| 4 | **Без полів `title`/`description`** у таблиці | Підтягуються з `config('steps')` по `key` у резолвері |
| 5 | `key` — **фіксований select** із `DRIVER_STATUS_*` | Сумісність із `MemberController::setStep` |
| 6 | Унікальність `(carrier_id, type_transport, key)` | Один ключ на набір |
| 7 | Drag-and-drop через `POST /application-steps/reorder` (transactional renumber 1..N) | Атомарне перевпорядкування |
| 8 | Max 20 кроків у наборі | Health-сейф |
| 9 | `ApplicationStepPolicy`: admin або `user->carrier?->id === step->carrier_id` | Адмін і перевізник у своєму кабінеті |
| 10 | `MemberController::setStep` перевіряє `status` у резолвленому наборі | Guard від деактивованих кроків |
| 11 | UI banner про активні заявки перевізника | Попередження перед edit/reorder/toggle |
| 12 | `rules` через custom cast `null → []` | Уніфікація формату |
| 13 | Резолвер — request-scoped singleton (`$app->scoped()`) | Уникнення N+1 на list-ендпоінтах |
| 14 | Без сідера і без clone-defaults | Простота, config завжди є fallback |

## Проблеми й як вирішили
- **NULL у composite unique (MySQL)** → `carrier_id NOT NULL`.
- **N+1 на списку заявок** → request-scoped memoization у резолвері.
- **Довільні ключі ламають `setStep`** → select із `DRIVER_STATUS_*`.
- **Data loss при зміні `action.type` у rules** → не вирішуємо (прийнято за п.11).
- **Дублювання `config('steps')` у двох Resources** → резолвер — єдина точка читання.

## Артефакти
- План: `~/.claude/plans/replicated-baking-turtle.md`
- Документація модуля: `docs/application-steps/README.md`
- 11 підтасок: `docs/application-steps/tasks/01-migration-model.md` … `11-tests-and-verification.md`
- Auto-memory: `~/.claude/projects/-Users-serhiin-Data-Source-buktrek/memory/project_application_steps_module.md`

## Ключові файли (для реалізації)
- **Створити:** `database/migrations/{ts}_create_application_steps_table.php`, `app/Entities/System/Content/ApplicationStep.php`, `app/Services/Steps/ApplicationStepsResolver.php`, `app/Http/Controllers/Api/Crud/Content/ApplicationStepsCrudController.php`, `app/Http/Requests/ApplicationStepRequest.php`, `app/Policies/ApplicationStepPolicy.php`, `resources/js/crud/fields/StepRulesBuilder.vue`, Vue-сторінка CRUD `application-steps`.
- **Змінити:** `app/Services/AppApi/Resources/ApplicationStepsResource.php`, `app/Services/AppApi/Resources/ApplicationListResource.php`, `routes/api.php`, `app/Providers/AuthServiceProvider.php`, `app/Http/Controllers/Api/AppApi/MemberController.php`, `lang/uk/crud.php`, новий `lang/uk/driver_statuses.php`.

## Статус реалізації
**Спроектовано, не реалізовано.** Команда для старту: "реалізуй кроки" / "почнемо з кроків" → читати `docs/application-steps/README.md` і починати з `tasks/01-migration-model.md`.

## Пов'язані нотатки
- [[2026-04-20-db-index-audit]]
- [[2026-04-21-file-upload-custom-names]]