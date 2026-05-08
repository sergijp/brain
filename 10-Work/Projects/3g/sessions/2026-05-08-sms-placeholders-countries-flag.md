---
title: "Проект: 3g — SMS плейсхолдери + емоджі прапора країн"
date: 2026-05-08
tags: [work, session, 3g, sms, notifications]
category: work
project: 3g
status: completed
pinecone_indexed: false
---

## Мета сесії

Розширення системи SMS/Viber шаблонів — додавання нових плейсхолдерів у `TicketNotificationService` для надання операторам більш детальних даних у повідомленнях.

## Виконано

| Задача | Результат |
|--------|-----------|
| Додано нові плейсхолдери в `TicketNotificationService.php` | 7 нових плейсхолдерів |
| Додано поле `flag` у CRUD форму країн | Поле відображається між `title` і `active` |
| Додано переклади в `lang/uk/crud.php` та `lang/en/crud.php` | `'flag' => 'Прапор (емоджі)'` |

### Нові плейсхолдери

| Плейсхолдер | Джерело | Опис |
|-------------|---------|------|
| `[to]` | `$ticket->to->title` | Назва станції прибуття |
| `[address_to]` | `$ticket->to->description` | Адреса станції прибуття |
| `[arrival_date]` | `$ticket->arrival->format('d.m.Y')` | Дата прибуття |
| `[arrival_time]` | `$ticket->arrival->format('H:i')` | Час прибуття |
| `[busmodel]` | `$bus->name` | Марка/модель автобуса |
| `[flag_from]` | `$ticket->from->city->country->flag` | Емоджі прапора країни відправлення |
| `[flag_to]` | `$ticket->to->city->country->flag` | Емоджі прапора країни прибуття |

### Повний список плейсхолдерів після сесії

```
[client], [trip], [date], [time], [from], [address], [flag_from],
[to], [address_to], [flag_to], [arrival_date], [arrival_time],
[busmodel], [busnumber], [busphone], [driverphones],
[link], [busphoto], [link_geo_locator]
```

## Важливі рішення (ADR)

| Рішення | Обґрунтування |
|---------|---------------|
| Використано `optional()` для ланцюжка `city->country` | Уникнення null pointer якщо місто або країна не задані для станції |
| Поле `flag` у країнах — текстове (не upload) | Зберігає Unicode-символ емоджі; не потребує файлового завантаження |
| Поле `flag` вже існувало в БД і моделі | Лише додали його до CRUD форми — не потрібна нова міграція |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Null pointer при отриманні прапора (country може бути null) | Загорнуто у `optional()` для безпечного ланцюжкового доступу |

## Артефакти

### Змінені файли

- `app/Services/TicketNotificationService.php` — нові плейсхолдери
- `app/Http/Controllers/Api/Crud/Directories/CountriesCrudController.php` — поле `flag` у формі
- `lang/uk/crud.php` — переклад `'flag' => 'Прапор (емоджі)'`
- `lang/en/crud.php` — переклад `'flag' => 'Flag (emoji)'`

## Пов'язані нотатки

- [[SMS Templates CRUD + TicketNotificationService]] — попередня сесія по SMS шаблонам
- [[project-overview]]