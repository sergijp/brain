---
title: "Проект: 3g — Дослідження Bus Services + промт для портування"
date: 2026-06-19
tags: [3g, work, session, bus, services, amenities]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Зрозуміти як реалізовані зручності/послуги автобуса (WiFi, туалет, кондиціонер тощо) і підготувати промт для портування цього функціоналу на інший проект.

## Виконано

| Задача | Результат |
|--------|-----------|
| Пошук реалізації Bus services | Знайдено на гілці `dev` (не `driver`) |
| Аналіз архітектури | JSON поле + конфіг як source of truth |
| Вивчення всіх шарів реалізації | Config, міграція, модель, CRUD, Vue, переклади, API |
| Написання промту для портування | Готовий детальний промт для `developer` агента |

## Де знаходиться функціонал

**Гілка:** `dev`

| Файл | Призначення |
|------|-------------|
| `config/bus_services.php` | 20 послуг з іконками та ключами перекладів |
| `database/migrations/2026_05_14_140112_add_services_to_buses_table.php` | Колонка `services` (longText, nullable) |
| `app/Entities/Tenant/Directories/Bus.php` | Поле `services` у `$fillable` + cast `json` |
| `app/Http/Controllers/Api/Crud/Directories/BusesCrudController.php` | Поле типу `bus_services` у вкладці "Сервіси" |
| `resources/js/crud/base/fields/BusServicesField.vue` | Vue компонент — клікабельна сітка послуг |
| `resources/js/crud/config/fields.js` | Реєстрація: `'bus_services': BusServicesField` |
| `lang/uk/crud.php` | Переклади `bus_services.*` (20 ключів) |
| `app/Services/Api/v1/Busfor/Resources/BusforResource.php` | Метод `enrichServices()` |
| `public/images/icons/services/` | 20 SVG іконок |

## Архітектурне рішення

**Підхід:** JSON масив ключів у полі `services` таблиці `buses`. Без окремих таблиць.

```
DB: buses.services = ["wifi", "air_conditioner", "wc"]
         ↓
Config: bus_services.php  ← single source of truth
         ↓
API: enrichServices() → [{key, title}, ...]
```

Послуги: `wifi`, `air_conditioner`, `wc`, `power_socket`, `usb`, `tv`, `audio_system`, `recliner_seats`, `extra_legroom`, `reading_lamp`, `blanket`, `pillow`, `seat_belt`, `coffee_service`, `snacks`, `fridge`, `microwave`, `wheelchair_lift`, `bike_rack`, `luggage_space`

## Метод enrichServices()

У `BusforResource` (базовий клас для Busfor API ресурсів):

```php
protected function enrichServices(?array $keys): array
{
    if (empty($keys)) { return []; }
    $catalog = config('bus_services', []);
    return collect($keys)
        ->filter(fn (string $key) => isset($catalog[$key]))
        ->map(fn (string $key) => ['key' => $key, 'title' => trans('crud.bus_services.'.$key)])
        ->values()->all();
}
```

Використовується в: `TripListResource`, `TripInfoResource`, `RouteResource`.

## Артефакти

- Промт для портування на інший проект — в тексті сесії в Claude Code (2026-06-19)
- Промт покриває всі 9 кроків: конфіг → міграція → модель → Vue → реєстрація → CRUD → переклади → API → іконки

## Пов'язані нотатки

- [[project_bus_photo]] — поле photo для Bus (попередня сесія)
- [[project_busfor_api_audit]] — Busfor API ресурси (BusforResource базовий клас)
