---
title: "Проект: 3g — SMS Templates CRUD + TicketNotificationService"
date: 2026-05-01
tags: [work, session, 3g, sms, viber, refactoring]
category: work
project: 3g
status: completed
pinecone_indexed: false
---

## Мета сесії

Перенести SMS шаблони з таблиці `settings` у окремий CRUD модуль `sms_templates`. Централізувати логіку відправки SMS/Viber у сервіс. Додати підтримку Viber каналу, dry-run режим, новий тестовий маршрут.

## SmsTemplate — що це і як працює

### Структура таблиці `sms_templates`

| Поле | Тип | Опис |
|------|-----|------|
| `key` | string, unique | Ідентифікатор шаблону (напр. `ticket_with_link`, `echeck`) |
| `name` | string | Назва для адмін-панелі |
| `body` | text | Тіло шаблону — HTML з WYSIWYG редактора |
| `placeholders` | json | Список доступних плейсхолдерів (для підказки в UI) |
| `description` | text, nullable | Опис призначення шаблону |
| `active` | boolean | Чи активний шаблон |
| `is_system` | boolean | Системний шаблон — не можна видалити |
| `deleted_at` | softDeletes | М'яке видалення |

### Шаблони (перенесені з `settings`)

- `ticket_with_link` — основний шаблон квитка з посиланням на PDF
- `ticket_without_link` — квиток без посилання
- `delay` — повідомлення про затримку рейсу
- `echeck` — фіскальний чек

### Плейсхолдери у шаблонах

```
[client]           — ПІБ пасажира
[trip]             — назва рейсу
[date]             — дата відправлення (d.m.Y)
[time]             — час відправлення (H:i)
[from]             — назва станції відправлення
[address]          — адреса станції відправлення
[busnumber]        — номер автобуса
[busphone]         — основний телефон автобуса
[driverphones]     — телефони водіїв (через кому)
[link]             — посилання на PDF квиток
[busphoto]         — URL фото автобуса
[link_geo_locator] — посилання на геолокацію (необов'язковий)
```

### Логіка моделі `SmsTemplate`

```php
// Отримати тіло шаблону з кешем (TTL 3600)
SmsTemplate::getBody('ticket_with_link');

// Рендер з підстановкою плейсхолдерів
SmsTemplate::render('ticket_with_link', [
    '[client]' => 'Іванов Іван',
    '[link]'   => 'https://...',
    // ...
]);
```

`render()` — pipeline:
1. `str_replace(placeholders, values, body)` — підставляє значення
2. `preg_replace(/<br\s*\/?>/i, "\n")` — `<br>` → новий рядок
3. `preg_replace(/<\/p>/i, "\n")` — `</p>` → новий рядок
4. `strip_tags()` — прибирає HTML теги
5. `trim()` — обрізає пробіли

**Чому так:** WYSIWYG зберігає HTML, а SMS/Viber потребує plain text з переносами рядків.

### Observer (`SmsTemplateObserver`)

- `saved()` → скидає кеш `sms_template_{key}`
- `deleted()` → скидає кеш
- `deleting()` → `abort(403)` якщо `is_system = true`

### CRUD особливості

- `body` — поле типу `wysiwyg`
- `key` — `readonly + disabled` при редагуванні (не можна змінити після створення)
- `key` — **відсутній** в `UpdateSmsTemplateRequest` rules (інакше CRUD фреймворк кидав помилку `prohibited`)
- Toggle-active кнопка: `POST /system/sms-templates/{id}/toggle-active`

## Виконано

| Задача | Результат |
|--------|-----------|
| SmsTemplate CRUD | Таблиця, модель, контролер, observer, permissions |
| Міграція шаблонів | 4 шаблони перенесено з `settings`, `sms_channel` setting додано |
| AlphaSms dry-run | `SMS_DRY_RUN=true` → логує `[channel:sms]` / `[channel:viber]` |
| Viber image+text | Тип `button` замість `image` для AlphaSMS API |
| TicketNotificationService | Централізований сервіс: `sendTicketNotification`, `configure`, `buildBusPhotoUrl`, `buildDriverPhones` |
| Рефакторинг споживачів | `SendTicketSmsOperation`, `sendSmsClients`, `sendAllSms`, `sendSmsMessage`, `sendSmsAboutDelay`, `SendEcheckSmsJob` |
| Тестовий маршрут | `GET /test/notify/{phone}?ticket_id=X` — читає `sms_channel`, відправляє відповідно |

## TicketNotificationService — логіка

```php
// Відправити квиткове сповіщення (SMS або Viber залежно від sms_channel)
$service->sendTicketNotification(
    $ticket,
    $geoLocatorUrl,   // '' якщо немає
    'ticket_with_link', // ключ шаблону
    $templateBody       // null → використає SmsTemplate::render()
                        // string → html_entity_decode + str_replace + strip_tags
);

// Тільки ініціалізація AlphaSms (для методів з довільним текстом)
$service->configure();

// Допоміжні методи
$service->buildBusPhotoUrl($bus);   // Storage::disk('public')->exists()
$service->buildDriverPhones($bus);  // collect phones JSON
```

**Канал** визначається з `config('settings.sms_channel', 'sms')`:
- `sms` → `AlphaSms::sendSms()`
- `viber` → `AlphaSms::sendViber()` з image (фото автобуса), button='Квиток', url=PDF

## Важливі рішення (ADR)

| Рішення | Чому |
|---------|------|
| `html_entity_decode` перед заміною плейсхолдерів | WYSIWYG зберігав `[` як `&#91;` → плейсхолдер не замінювався |
| Viber type=`button` при image+text | AlphaSMS type=`image` ігнорує текст повідомлення |
| `configure()` як окремий метод сервісу | `sendSmsAboutDelay` і `SendEcheckSmsJob` відправляють довільний текст — не через `sendTicketNotification()`, але ініціалізація AlphaSms однакова |
| `[link_geo_locator]` → завжди `''` коли не передано | Інакше залишається як literal текст у повідомленні |
| `key` відсутній в UpdateRequest rules | CRUD фреймворк надсилає всі поля включно з disabled — `prohibited` правило блокувало збереження |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| `[link_geo_locator]` не замінювався | `html_entity_decode()` на templateBody перед `Str::replace` |
| Dry-run не логував у `/trips/sms-send` | Не було `setViberSender` → `sendViber()` повертав false до dry-run. Фікс: `configure()` |
| Viber з фото не показував текст | Тип `image` ігнорує текст → `button` при наявності обох |
| `prohibited` validation error на update | `key` в rules → видалено з UpdateSmsTemplateRequest |

## .env змінні

```env
ALPHA_SMS_API_KEY=        # API ключ alphasms.ua
ALPHA_SMS_SENDER=         # Підпис для SMS
ALPHA_VIBER_SENDER=       # Підпис для Viber (якщо інший від SMS)
SMS_DRY_RUN=false         # true → лише лог, без реальної відправки
```

## Артефакти

- `database/migrations/2026_04_30_000001_create_sms_templates_table.php`
- `database/migrations/2026_05_01_122848_add_sms_channel_to_settings_table.php`
- `app/Entities/System/SmsTemplate.php`
- `app/Observers/SmsTemplateObserver.php`
- `app/Http/Controllers/Api/Crud/SmsTemplatesCrudController.php`
- `app/Http/Requests/SmsTemplate/UpdateSmsTemplateRequest.php`
- `app/Services/TicketNotificationService.php` ← новий
- `app/Services/Api/AlphaSms.php` — dry-run для SMS і Viber
- `app/Crud/Operations/SendTicketSmsOperation.php`
- `app/Jobs/Echeck/SendEcheckSmsJob.php`

## Пов'язані нотатки

- [[project_echeck_fiscal]] — echeck також використовує AlphaSms + sms_channel
- [[project_bus_photo]] — `Bus.photo` використовується в Viber повідомленнях