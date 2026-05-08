---
title: "Notifications — SMS / Viber / ShortLink / templates"
date: 2026-05-08
tags: [3g, architecture, notifications, sms, viber]
category: docs
project: 3g
status: active
aliases: ["3g-notifications", "3g-sms", "3g-templates"]
pinecone_indexed: false
---

# Notifications — SMS / Viber / ShortLink

Централізована система відправки повідомлень клієнтам (квитки, чеки, затримки).

## SmsTemplate CRUD

Таблиця `sms_templates`: `key` (unique), `name`, `body` (wysiwyg), `placeholders` (json), `description`, `active`, `is_system`, `softDeletes`.

- Міграція перенесла 4 шаблони з `settings`-таблиці.
- `app/Entities/System/SmsTemplate.php` — кеш TTL 3600, `render()`, `getBody()`, `flushCache()`.
- `app/Observers/SmsTemplateObserver.php` — скидає кеш при save/delete; блокує видалення `is_system=true`.
- `app/Http/Controllers/Api/Crud/SmsTemplatesCrudController.php` — CRUD + toggle-active, wysiwyg `body`, readonly `key` при update.
- Permissions: `sms-templates-read/create/update/delete/toggle-active`.

## AlphaSms — sms / viber, dry-run

- `SMS_DRY_RUN=true` → логує замість реальної відправки. У лог `[channel:sms]` або `[channel:viber]`.
- `sendViber()` підтримує `image+text` через тип `button` (НЕ `image` — бо image ігнорує текст).
- `sms_channel` setting (`sms`/`viber`) — перемикає канал без зміни коду.

## TicketNotificationService

`app/Services/TicketNotificationService.php` — централізована відправка квиткових повідомлень.

API:
- `sendTicketNotification(Ticket, geoLocatorUrl, templateKey, templateBody)` — основний вхід.
- `configure()` — ініціалізує AlphaSms (api key, sms sender, viber sender). Можна викликати окремо.
- `buildBusPhotoUrl(?Bus)` — перевіряє файл через `Storage::disk('public')->exists()`.
- `buildDriverPhones(?Bus)` — збирає телефони з JSON-поля.
- `buildMessage()` (private) — якщо `$templateBody` передано → `html_entity_decode` + `str_replace` + `strip_tags`, інакше → `SmsTemplate::render()`.

## Споживачі (хто шле через сервіс)

- `SendTicketSmsOperation` — повністю делегує `sendTicketNotification()`.
- `TripsCrudController::sendSmsClients()` — `configure()` + per-ticket виклик.
- `TripsCrudController::sendAllSms()`, `sendSmsMessage()` — через сервіс.
- `TripsCrudController::sendSmsAboutDelay()` — довільний текст, `configure()` + channel routing.
- `SendEcheckSmsJob::sendSms()` — `configure()` + channel routing для шаблону echeck.

## Плейсхолдери (актуально на 2026-05-08)

`[client]`, `[trip]`, `[date]`, `[time]`, `[from]`, `[address]`, `[flag_from]`, `[to]`, `[address_to]`, `[flag_to]`, `[arrival_date]`, `[arrival_time]`, `[busmodel]`, `[busnumber]`, `[busphone]`, `[driverphones]`, `[link]`, `[busphoto]`, `[link_geo_locator]`, `[map_link]`

**Прапори:** `[flag_from]`/`[flag_to]` — `optional(optional($ticket->from->city)->country)->flag` — Unicode-емоджі, заповнюється у `CountriesCrudController` (поле `flag`).

**`[map_link]`** — Google Maps URL з `lat`/`long` `Station`. `urlencode()` обов'язковий (DMS-формат містить символи, які Viber обрізає).

## ShortLink — скорочення URL

- `app/Entities/System/ShortLink.php` — `token` (unique, 8 chars), `url`, `expires_at`.
- `app/Services/ShortLinkService.php` — `shorten(string $url, int $days = 30): string` → `https://{APP_URL}/go/{token}`.
- Маршрут: `GET /go/{token}` → `ShortLinkController` → 301 (або 410 якщо протермінований).
- Команда: `short-links:prune` — видаляє прострочені, через scheduler щодня.
- `$geoLocatorUrl` у `TicketNotificationService` автоматично скорочується перед підстановкою у `[link_geo_locator]` та `[map_link]`.
- TTL: 30 днів.

## Тестовий маршрут

`GET /test/notify/{phone}?ticket_id=X` — відправляє через поточний `sms_channel`, `dd()` результат.

## Важливі деталі

- `html_entity_decode` перед заміною плейсхолдерів — WYSIWYG може зберігати `[` як `&#91;`.

## Пов'язані

- [[INDEX]]
- [[echeck-fiscal]] — використовує `SmsTemplate` + `AlphaSms`
- [[legacy-controllers]] — `TripsCrudController` має `sendAllSms`/`sendSmsMessage` (раніше дубль логіки, тепер через сервіс)
