---
title: "Application Flow — заявка → кроки → файли → проблеми"
date: 2026-05-08
tags: [buktrek, architecture, application, business-logic]
category: docs
project: buktrek
status: active
aliases: ["buktrek-application-flow", "buktrek-applications"]
pinecone_indexed: false
---

# Application Flow

Головний бізнес-процес buktrek: перевізник створює заявку (Application) → водій проходить кроки (Steps) → завантажує файли → адмін за потреби знімає прапор проблеми.

## 1. Заявка (Application)

Tenant-сутність. Контролер: `app/Http/Controllers/Api/Crud/ApplicationsCrudController` (2100+ рядків — техдовг).

**Не-CRUD методи** виносяться в окремі контролери:
- `ApplicationFilesController` — `getCarrierFiles`, `downloadFiles` (ZIP-архів). Файл: `app/Http/Controllers/Api/System/ApplicationFilesController.php`.

## 2. Кроки водія (Application Steps) — **спроектовано, не реалізовано**

Статус 2026-04-21: модуль повністю спроектовано, реалізацію не почато.

**Що робить:** переводить статичний `config/steps.php` (кроки AppApi для водія) у DB-конструктор, керований per-carrier через адмінку та кабінет перевізника.

**Архітектура (18 погоджених рішень):**
- Таблиця `application_steps` у System DB. Поля: `carrier_id` (NOT NULL), `type_transport`, `key`, `number`, `rules` (JSON), `active`. Без `title`/`description` — підтягуються з `config('steps')` по `key`.
- Резолвер 2-рівневий: БД (активні для carrier+type) → fallback на config. Request-scoped singleton.
- `key` — фіксований select з `DRIVER_STATUS_*` констант `Application` (не нові ключі).
- Unique `(carrier_id, type_transport, key)`. Max 20 кроків у наборі.
- Drag-and-drop через `POST /application-steps/reorder` (transactional renumber 1..N).
- `ApplicationStepPolicy`: admin або `user->carrier?->id === step->carrier_id`.
- `MemberController::setStep` додатково перевіряє, що `status` є у резолвленому наборі.
- UI banner попереджає про активні заявки перевізника при редагуванні кроків.
- `rules` нормалізується до `[]` через custom cast (null → []).
- Без сідера, без clone-defaults.

**Артефакти:**
- План: `~/.claude/plans/replicated-baking-turtle.md`
- Документація: `<repo>/docs/application-steps/` (README + tasks/01..11)

**Існуючі споживачі `config('steps')`** (треба замінити резолвером):
- `ApplicationStepsResource.php:57`
- `ApplicationListResource.php:53`

**Ключі кроків (DRIVER_STATUS_*):** `app/Entities/System/Content/Application.php:54-64`.

## 3. Файли заявок

`ApplicationFilesController` (System):
- `getCarrierFiles` — фільтри `carrier_id`, `transport_number`, `trailer_number`, `loading_date`, `date_unloading`. Тільки не-архівні заявки.
- `downloadFiles(file_ids[])` — ZIP, тимчасово в `storage/app/tmp/`.

**Завантаження файлів через AppApi** — деталі у [[db-conventions]] (FileUploadService).

## 4. RemoveProblem (2026-05-06)

- Роут: `POST /application/{id}/remove-problem`, middleware `can:applications-edit`
- Метод: `ApplicationsCrudController::removeProblem(int $id)` — `is_problem = false`, `note` не чіпається
- Frontend: `api-bridge.js` → `removeProblemFromApplication`

**Не дублюється в AppApi** — там використовується `MemberController` для мобільного, не цей контролер.

## Пов'язані

- [[INDEX]]
- [[multi-tenancy]]
- [[mobile-api]]
- [[db-conventions]]
- Tier-2 pointer'и: `~/.claude/projects/-Users-serhiin-Data-Source-buktrek/memory/project_application_*.md`
