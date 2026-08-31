---
title: "3g — API мобільного застосунку пасажира (/api/v1/app)"
date: 2026-08-24
tags: [3g, architecture, api, mobile, docs]
category: docs
project: 3g
status: active
aliases: ["app-api", "3g-mobile-api"]
pinecone_indexed: false
last_verified: 2026-08-24
---

# API мобільного застосунку пасажира

Гілка: `user-app-api`. Довідник у репозиторії: `APP_API.md` (оновлений 2026-08-24).
Код: `app/Services/Api/v1/App/`.

## Суть

27 маршрутів під префіксом `/api/v1/app` для Expo/React Native застосунку пасажира
(`3g-user-app`). Контролери — **тонкі адаптери** над наявними контролерами сайту:
приводять запит до очікуваного формату і повертають ті самі ресурси. Власної
бізнес-логіки бронювання немає.

Підхід до захисту й сумісності — [[../decisions/2026-08-24-app-api-adapter-guards]].

## Два користувачі одночасно

| Хто | Гуард | Хто ставить | Навіщо |
|---|---|---|---|
| Технічний Member | `api` (Passport) | `isLoggedIn` / `AuthCheck` | від `request()->user()` залежать `TripsService::getTripPlaces()` і `BookingService` |
| Пасажир (Client) | `clients` | `AppClientAuth` за Bearer-токеном | кабінет; гуард у проєкті сесійний, тому для застосунку зроблено власні токени |

`AppClientAuth` виставляє заголовок `Client`, за яким `BookingService::bookOriginal()`
привʼязує куплені квитки до кабінету. Саме тому публічна група підключає
`app.client:optional` — без нього `/order/create` (він публічний, бо гість теж купує)
не виставляв би заголовок, і покупка залогіненого не потрапляла б у «Мої квитки».

## Токени

`client_api_tokens` + модель `ClientApiToken`. У БД лише sha256-хеш, клієнту —
`{id}|{60 символів}` (формат Sanctum). Приймається як `Authorization: Bearer`,
так і `X-Client-Token`.

Налаштування — `config/app_api.php`: `token_ttl_days` (env `APP_API_TOKEN_TTL_DAYS`,
типово 365; `0` — безстроково), `max_tokens_per_client` (env, типово 10).
`issue()` викликає `prune()` — прибирає протерміновані й найстаріші понад ліміт.

## Ланцюжок middleware

```
NormalizeJsonInput → ForceJsonResponse → CaptureAppClientToken → WithoutTicketScope
    → [api] → app.client | app.client:optional → isLoggedIn → api.locale → [throttle]
```

Перші чотири зареєстровані в `RouteServiceProvider` **до** групи `api`, діють лише
на `/api/v1/app`.

| Middleware | Проблема, яку закриває |
|---|---|
| `NormalizeJsonInput` | контролери сайту читають `$request->get()`, який не бачить JSON-тіла; мобільний клієнт шле JSON → параметри приходили `null`, і `merge()` в адаптерах теж не працював |
| `ForceJsonResponse` | без `Accept: application/json` помилка валідації → 302 замість JSON |
| `CaptureAppClientToken` | `throttle` у групі `api` піднімає Passport, той не впізнає наш Bearer і **стирає** заголовок `Authorization` |
| `WithoutTicketScope` | `TicketScope` звужує квитки до `order.member_id` поточного користувача; в API це один технічний Member → видно 16.6% квитків (28 228 із 169 572) |

## Правила доступу

| Ендпоінт | Гість | З токеном |
|---|---|---|
| `/order/tickets`, `/order/check` | лише за **uuid**; числовий `orders.id` → 404 | числовий id — лише для власного замовлення |
| `/ticket/status`, `/ticket/download` | за номером квитка, під throttle | лише власні квитки |
| `/profile/*` | 401 | лише власні (`tickets.client_id`) |

`orders.id` послідовний → анонімний доступ за ним закрито. Перевірка належності
робиться **без** `TicketScope`, інакше guard не бачив би власні квитки пасажира,
куплені в касі.

Ліміти: `app-public-tickets` 30/хв, `app-error-reports` 20/хв — ключ по **IP + шлях**,
бо по `$request->user()` ліміт був би спільним на весь застосунок.

## Вхід

`loginFront` шукає клієнта лише через `where('email', $login)`, тому телефон до перевірки
пароля не доходив. Адаптер резолвить телефон у email до делегування; неоднозначний
збіг ігнорується (25 номерів належать 2+ клієнтам).

## Відомі обмеження

1. 41 157 із 51 639 клієнтів не мають email — увійти не можуть у принципі.
2. Дублікати: 9 адрес email на 18 клієнтів, 25 телефонів у 2+ клієнтів.
3. Телефон через `/profile` не оновлюється: контролер пише `phone`, модель зберігає `phones` (JSON).
4. `/order/create` не звіряє кількість `seats` із `passcount`.
5. `/auth/forgot-password` розкриває існування email (200 проти 422), у тексті — сирий `:email`.
6. `TrustProxies` не налаштований → за проксі ліміти ключуються по IP проксі.
7. `/texts` віддає `lang/{locale}/app.php`: 130 ключів, з яких сайт використовує **один**
   (`meta_site_title`), решта — сироти; 10 ключів контактної форми у файлі відсутні.
   261 ключ застосунку ще не перенесено; `lang=ru` віддає українські тексти через fallback.
8. Тестів у `tests/` немає — перевірки виконувались разовими скриптами.

## Пов'язані

- [[../decisions/2026-08-24-app-api-adapter-guards]]
- [[../sessions/2026-08-24-app-api-audit-and-fixes]]
- [[notifications]] — інший модуль поверх тих самих сутностей
- [[legacy-controllers]] — стан контролерів, над якими надбудований цей шар
