---
title: "Mobile API — app/Services/AppApi/"
date: 2026-05-08
tags: [buktrek, architecture, mobile, api, passport]
category: docs
project: buktrek
status: active
aliases: ["buktrek-mobile-api", "buktrek-appapi"]
pinecone_indexed: false
---

# Mobile API (AppApi)

API для мобільного застосунку водіїв. Локалізовано в `app/Services/AppApi/`.

## Структура

```
app/Services/AppApi/
├── Controllers/        ← endpoint-логіка
├── Services/           ← бізнес-сервіси (FileUploadService та ін.)
├── Requests/           ← FormRequest валідація
├── Resources/          ← JSON-серіалізація
├── Middleware/         ← AppApi-specific middleware
├── Traits/             ← shared traits
└── routes.php          ← маршрути префіксу /app
```

## Auth

- **Laravel Passport (OAuth2)** — токени під мобільний клієнт.
- Routes префіксуються `/app/*`.

## Контекст

Це **Tenant-context** — водій належить перевізнику в конкретному tenant (website). Усі моделі через `OnTenant`.

## Ключові споживачі

- `MemberController` — основний контролер для дій водія (зміна статусу, завантаження файлів, дії над заявкою).
  - `MemberController::setStep` — після резолверу кроків (див. [[application-flow]]) перевіряє, що новий status є у резолвленому наборі.
  - `MemberController::uploadFiles` — приймає `files` + `names`, викликає `FileUploadService` (див. [[db-conventions]]).

## Правила

1. **Не плутати з System API** (`app/Http/Controllers/Api/System/`) — мобільні endpoint-и тільки в AppApi.
2. Нові методи для мобільного — в `MemberController` або новий контролер у `AppApi/Controllers/`.
3. Маршрути — у `app/Services/AppApi/routes.php`, **не** в кореневому `routes/api.php`.

## Пов'язані

- [[INDEX]]
- [[multi-tenancy]]
- [[application-flow]]
- [[db-conventions]]
