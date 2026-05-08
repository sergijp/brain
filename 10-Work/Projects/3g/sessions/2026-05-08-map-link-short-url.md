---
title: "Проект: 3g — map_link плейсхолдер + власний скорочувач URL"
date: 2026-05-08
tags: [work, session, 3g]
category: work
project: 3g
status: completed
pinecone_indexed: false
---

## Мета сесії

1. Додати плейсхолдер `[map_link]` у сповіщення — посилання на Google Maps з координатами станції відправлення
2. Скоротити `$geoLocatorUrl` (дуже довгий) через власний сервіс коротких посилань

## Виконано

| Задача | Результат |
|--------|-----------|
| Додати `[map_link]` у `TicketNotificationService` | `https://maps.google.com/?q=urlencode(lat,lng)` |
| Фікс DMS-координат у Viber (обривало посилання) | `urlencode()` на координати — `°`, `'`, `"` стали `%xx` |
| Міграція `short_links` | Таблиця з `token`, `url`, `expires_at` |
| Модель `ShortLink` | `scopeActive` фільтрує прострочені |
| `ShortLinkService` | `shorten()` + `shortUrl()`, токен 8 символів, retry на колізію |
| `ShortLinkController` | Редирект 301 або 404 |
| Маршрут `/go/{token}` | Публічний, без auth, перед catch-all |
| `PruneShortLinks` команда | `php artisan short-links:prune` |
| Scheduler | `->daily()` прибирання прострочених записів |
| Інтеграція в `TicketNotificationService` | `$geoLocatorUrl` скорочується перед відправкою |

## Важливі рішення (ADR)

| Рішення | Чому |
|---------|------|
| `urlencode()` для координат | Viber обриває URL на символах `°'\"` (DMS формат) |
| Власний скорочувач замість bit.ly | Немає залежності від зовнішнього сервісу, повний контроль |
| Термін дії 30 днів | Баланс між розміром БД і доступністю посилань |
| `use` імпорт не потрібен | `ShortLinkService` і `TicketNotificationService` в одному namespace `App\Services` |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Viber обрізав Google Maps посилання на `°` | `urlencode()` координат перед конкатенацією в URL |
| Зайвий `use App\Services\ShortLinkService` | Видалено — обидва класи в `App\Services`, `::class` резолвиться без імпорту |

## Артефакти

```
database/migrations/2026_05_08_122228_create_short_links_table.php
app/Entities/System/ShortLink.php
app/Services/ShortLinkService.php
app/Http/Controllers/Frontend/ShortLinkController.php
app/Console/Commands/PruneShortLinks.php
routes/web.php                          — GET /go/{token}
app/Console/Kernel.php                  — short-links:prune daily
app/Services/TicketNotificationService.php — [map_link] + geoLocatorUrl shortening
```

## Пов'язані нотатки

- [[SMS Templates CRUD + TicketNotificationService]]
