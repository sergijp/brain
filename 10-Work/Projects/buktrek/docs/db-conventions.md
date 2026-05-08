---
title: "DB Conventions — індекси, file upload, uniqueness"
date: 2026-05-08
tags: [buktrek, architecture, database, conventions]
category: docs
project: buktrek
status: active
aliases: ["buktrek-db", "buktrek-db-conventions"]
pinecone_indexed: false
---

# DB Conventions

Правила, яких треба дотримуватись при додаванні/зміні моделей, міграцій, форм валідації.

## 1. Індекси (аудит 2026-04-20)

Всі FK мали індекси, дублікатів немає. Додано міграції з відсутніми індексами:
- `applications`: `status`, `loading_date`, `archive`, `deleted_at`
- `customers`: `email`, `edrpou`
- `transports`, `trailers`: `number`

**Правило:** при додаванні нового поля-фільтра у `applications`/`customers` — одразу додавати індекс у міграції.

## 2. FileUploadService — кастомні імена файлів

**Файл:** `app/Services/AppApi/Services/FileUploadService.php`

API:
- `uploadFiles(array $files, Application $application, array $names = [])`
- `storeFile($file, $application, ?string $customName = null)`
- `buildFileName(?string $customName, string $fallback)` — транслітерує через `Transliterator::create('Any-Latin; Latin-ASCII; Lower()')`, пробіли → `_`, видаляє `[^a-z0-9_]`. Порожній результат → fallback на md5.
- `buildPrefix(Application $application)` — `{number}_{YYYY-MM-DD}` з `$application->transport->number`. Fallback `no_car`.
- `sanitize(string $text)` — спільна транслітерація.

**Формат імені:**
```
{custom_name}_{номер_авто}_{YYYY-MM-DD}.{ext}
```
Приклад: `cmr_dokument_aa_1234_bb_2026-04-21.pdf`

**Правила:**
- `original_name` у `files`-зв'язку зберігає **повну нову назву** (не сирий клієнтський рядок).
- Розширення завжди з `$file->getClientOriginalExtension()`, не з `names`.
- Якщо `names` не передано — `{md5}_{number}_{date}.{ext}`.
- Контролер: `MemberController::uploadFiles` передає `$request->input('names', [])`.

## 3. Carrier ↔ Member email uniqueness

При створенні `Carrier` автоматично створюється `Member` з тим самим email.

**Унікальність:**
- `carriers.email` — **БЕЗ** unique індексу.
- `members.email` — **MAY** unique індекс (`create_members_table`).
- `CarriersCrudController::beforeCreateAction` — шукає/створює `Member` за email.
- Валідація: `Rule::unique('members', 'email')` у `CreateCarrierRequest` (фікс 2026-04-28 — прибрано дубльовану перевірку з контролера).

**Правило:** при змінах у формі перевізника — пам'ятай, що email валідується відносно `members`, не `carriers`.

## 4. Coding rules (з `docs/AI_AGENT_CONTEXT.md`)

- PHP 8.1+, PSR-12, `declare(strict_types=1)` у нових файлах.
- Models у `app/Entities`, **НЕ** `app/Models`.
- CRUD controllers у `app/Http/Controllers/Api/Crud`, наслідують base.
- API routes у `routes/api.php` (для System); AppApi — у `app/Services/AppApi/routes.php`.

## Пов'язані

- [[INDEX]]
- [[multi-tenancy]]
- [[mobile-api]]
- [[application-flow]]
