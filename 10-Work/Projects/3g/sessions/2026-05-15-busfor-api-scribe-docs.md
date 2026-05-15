---
title: "3g: Busfor API — документація через Scribe + Try-it-out"
date: 2026-05-15
tags: [3g, busfor, api-docs, scribe, work, session]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

# Busfor API — документація через Scribe + Try-it-out

## Мета сесії

Створити публічну документацію Busfor partner API в актуальному виді (легко оновлюваному, синхронізованому з кодом), щоб партнер міг читати endpoint specs, бачити приклади, і тестувати запити прямо зі сторінки.

## Виконано

### 1. Аналіз варіантів і вибір підходу
- Запропоновано 4 варіанти: Scribe, OpenAPI YAML+Redoc, VitePress, Markdown в репо
- Вибрано **Scribe (knuckleswtf/scribe)** — Laravel-нативний, авто-генерує з routes/Form Requests/Resources
- Причина: користувач сказав "важко оновлювати" — Scribe вирішує це через автогенерацію

### 2. Інсталяція Scribe
- `composer require knuckleswtf/scribe --dev`
- Поставлено **Scribe 4.x** (не 5.x — 5.x потребує PHP 8.4, проект на 8.1/8.2)
- Конфіг публіковано: `config/scribe.php`

### 3. Налаштування Scribe
- `type: static` → файли в `public/docs/busfor/`
- `routes[0].match.prefixes: ['busfor/*']` → тільки Busfor API
- `try_it_out.enabled` спочатку `false`, потім `true` (партнер просив)
- `auth.in: bearer` + `auth.extra_info` пояснює отримання токена через `/login`
- `intro_text`, `title`, `description` українською
- `groups.order` — точна послідовність груп і endpoint'ів з `BusforApiProvider::routes()`

### 4. Анотації у коді Busfor
- **5 контролерів** (Auth, Station, Trip, Order, Tickets): `@group`, `@authenticated`/`@unauthenticated`, `@response` (success + error), `@responseField`
- **11 Request класів**: `bodyParameters()` або `queryParameters()` з описами укр + реалістичними прикладами
- **14 endpoint'ів** покрито у 5 групах (Auth, Locations, Trips, Orders, Tickets)

### 5. Публічний маршрут і генерація
- `routes/web.php` → `Route::get('/docs/busfor', fn () => redirect('/docs/busfor/index.html'))`
- `php artisan scribe:generate` → 3 артефакти:
  - `index.html` (~126 KB)
  - `openapi.yaml` (~55 KB)
  - `collection.json` (~52 KB Postman v2.1)

### 6. PDF генерація
- Створено `app/Console/Commands/GenerateBusforDocsPdf.php`
- Команда: `php artisan busfor:docs:pdf`
- Використовує системний `/usr/local/bin/wkhtmltopdf` 0.12.6 + `--print-media-type` (one-column print stylesheet від Scribe)
- Output: `public/docs/busfor/busfor-api.pdf` (~202 KB, 19 сторінок)

### 7. Try-it-out увімкнено
- `try_it_out.enabled: true`, `base_url: http://3g.loc`
- Партнер може робити реальні запити прямо з doc-сторінки
- Workflow: login → отримати access_token → вставити в Authorization field угорі → тестувати решту endpoint'ів

## Важливі рішення (ADR)

| Рішення | Альтернативи | Чому |
|---------|--------------|------|
| Scribe 4.x, не 5.x | Scribe 5.x | 5.x вимагає PHP 8.4, проект на 8.1/8.2 |
| `type: static` | `type: laravel` | Зручніше деплоїти, не залежить від app boot, прямі static files |
| Try-it-out enabled | Disabled | Зручність партнерам, але реальні /reservate/buy/return create production data — мати на увазі |
| Сценарій PDF: `wkhtmltopdf` на Scribe HTML з `--print-media-type` | Pandoc, власний Blade | Швидко, використовує існуючий print CSS від Scribe. **АЛЕ** — користувач показав docs/Api BUSFOR.pdf у іншому стилі (Google Docs експорт) → треба зробити інший формат PDF (см. Pending) |
| Сценарій CSRF: видалити Sanctum middleware з api group | Додати exclusion у VerifyCsrfToken::$except | Sanctum ніде не використовується (тільки Passport) — це boilerplate, краще прибрати корінь |

## Проблеми й як вирішили

### Проблема 1: CSS/JS не вантажились на сторінці /docs/busfor
- **Симптом:** HTML рендериться, але без стилів (голий чорно-білий текст)
- **Причина:** старий route робив `response()->file('docs/busfor/index.html')` на URL `/docs/busfor` (без trailing slash). Браузер base path = `/docs/`, тому `./css/...` резолвилось як `/docs/css/...` → 404
- **Виправлення:** замість `response()->file()` → `redirect('/docs/busfor/index.html')`
- **Файл:** `routes/web.php:13-15`

### Проблема 2: CSRF token mismatch при Try-it-out
- **Симптом:** `POST /api/v1/busfor/login` повертає `{"message": "CSRF token mismatch."}`
- **Причина:** `Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful` був у groupі `api` (boilerplate з Laravel 10). При same-origin запитах Sanctum визначав їх як stateful і інжектив `web` group (StartSession + VerifyCsrfToken)
- **Чому Sanctum взагалі тут:** ніде не використовується (auth через Passport + кастомний `external.token`), залишився як boilerplate з install
- **Виправлення:** прибрано `EnsureFrontendRequestsAreStateful::class` з `app/Http/Kernel.php` middleware group `api`
- **Перевірено:** admin login (`/api/login`) працює як раніше, нічого не зламано

## Артефакти

### Файли створено
- `app/Console/Commands/GenerateBusforDocsPdf.php`
- `config/scribe.php` (з publish)
- `public/docs/busfor/{index.html, css/, js/, images/, collection.json, openapi.yaml, busfor-api.pdf}`
- `.scribe/` (intermediate, gitignore-кандидат)

### Файли змінено
- `composer.json`, `composer.lock` (+ knuckleswtf/scribe ^4 dev)
- `app/Http/Kernel.php` (видалено Sanctum middleware з api group)
- `routes/web.php` (додано публічний маршрут /docs/busfor)
- `app/Services/Api/v1/Busfor/Http/Controllers/*.php` (5 файлів, тільки PHPDoc анотації)
- `app/Services/Api/v1/Busfor/Requests/*.php` (11 файлів, додано bodyParameters/queryParameters)

### Команди
```bash
# Регенерувати документацію
php artisan scribe:generate

# Згенерувати PDF (current Scribe-style)
php artisan busfor:docs:pdf
```

### URLs
- Doc сторінка: `http://3g.loc/docs/busfor/`
- Postman: `http://3g.loc/docs/busfor/collection.json`
- OpenAPI: `http://3g.loc/docs/busfor/openapi.yaml`
- PDF: `http://3g.loc/docs/busfor/busfor-api.pdf`

## Pending — НЕ зроблено

### PDF у стилі docs/Api BUSFOR.pdf
- Користувач показав свій зразок PDF (`docs/Api BUSFOR.pdf`, 849 KB) у стилі **Google Docs/Word експорт**:
  - Великі сині заголовки методів (LOGIN, TRIPS...)
  - Inline-code для URL `/login`
  - Таблиці: field | type | required | description і field | description (для result)
  - JSON приклади у темному блоці
  - Без sidebar / двоколонкового layout Scribe
- Поточний PDF (`busfor-api.pdf`) — це Scribe HTML print-stylesheet, інший стиль
- **План для майбутньої сесії:**
  1. Прочитати решту сторінок зразка (poppler не встановився на macOS 12 — Tier 2 brew config; альтернатива: pypdf або pdftotext)
  2. Зробити власний Blade template `resources/views/docs/busfor/pdf.blade.php` зі стилем зразка
  3. Дані брати з `.scribe/endpoints/*.yaml`
  4. Оновити команду `busfor:docs:pdf` щоб рендерила Blade → Snappy → PDF замість wkhtmltopdf-на-Scribe-HTML

## Пов'язані нотатки

- [[project_busfor_api_audit]] — попередня велика робота над Busfor API (refact.md, контрактні баги)
- `app/Services/Api/v1/Busfor/checklist.md` — Фаза И (документація) частково виконана: §0-§7 покриті Scribe-аннотаціями, OpenAPI/Postman/PDF згенеровані. И-3 (edge cases), И-7 (CHANGELOG) — ще не зроблено

## Тегі для пам'яті

- Scribe Laravel docs
- knuckleswtf/scribe 4.x vs 5.x compat
- wkhtmltopdf print-media-type for one-column
- Sanctum boilerplate causes CSRF on API
- Same-origin Try-it-out CSRF gotcha