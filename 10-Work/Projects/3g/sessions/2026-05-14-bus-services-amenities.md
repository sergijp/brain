---
title: "Проект: 3g — Сервіси автобуса (amenities)"
date: 2026-05-14
tags: [3g, work, session, bus, amenities, crud]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Додати до автобусів вибір сервісів (Wi-Fi, розетки, кондиціонер тощо):
1. Конфіг всіх можливих сервісів (~20) з іконками
2. Новий таб "Сервіси" у CRUD автобуса з чекбоксами

## Виконано

| Задача | Результат |
|--------|-----------|
| Планування | `.claude/plans/smooth-frolicking-star.md` |
| 20 SVG іконок | `public/images/icons/services/` (18 lucide, 1 tabler, 1 ручний) |
| Міграція | `2026_05_14_140112_add_services_to_buses_table.php` — `longText services nullable after photo` |
| Bus модель | `services` у `$fillable` + `$casts` (Json::class) |
| Конфіг | `config/bus_services.php` — 20 сервісів з `icon` + `translation_key` |
| Переклади | `lang/uk/crud.php` + `lang/en/crud.php` — секція `bus_services` (20 ключів) |
| CRUD контролер | `BusesCrudController.php` — новий таб `trans('crud.services')` з полем типу `bus_services` |
| Vue компонент | `resources/js/crud/base/fields/BusServicesField.vue` — Options API + FieldMixin |
| Реєстрація типу | `resources/js/crud/config/fields.js` — `'bus_services': BusServicesField` |
| Міграція виконана | `php artisan migrate` — DONE (179ms) |

## Важливі рішення (ADR)

| Рішення | Варіанти | Вибір | Причина |
|---------|----------|-------|---------|
| Зберігання сервісів | JSON колонка vs pivot table | JSON колонка `services` | Узгоджено з патерном phones/places у Bus (App\Casts\Json) |
| Іконки | SVG власні vs FontAwesome vs Lucide | SVG у public/images/icons/services/ | Патерн проєкту — 60+ SVG там само |
| Довідник сервісів | config vs БД | config/bus_services.php | Статичний список, не потребує адмін-керування |

## Список 20 сервісів

`wifi`, `air_conditioner`, `wc`, `power_socket`, `usb`, `tv`, `audio_system`, `recliner_seats`, `extra_legroom`, `reading_lamp`, `blanket`, `pillow`, `seat_belt`, `coffee_service`, `snacks`, `fridge`, `microwave`, `wheelchair_lift`, `bike_rack`, `luggage_space`

## Проблеми й рішення

- `developer` і `frontend` агенти не існують у системі → виконано через `general-purpose`
- `blanket.svg` відсутня у lucide/tabler → намальовано вручну (stroke, 24×24)
- `npm run build` не виконано (користувач скасував) → статус збірки не підтверджено

## Артефакти

**Нові файли:**
- `database/migrations/2026_05_14_140112_add_services_to_buses_table.php`
- `config/bus_services.php`
- `public/images/icons/services/*.svg` (20 файлів)
- `resources/js/crud/base/fields/BusServicesField.vue`

**Змінені файли:**
- `app/Entities/Tenant/Directories/Bus.php`
- `app/Http/Controllers/Api/Crud/Directories/BusesCrudController.php`
- `lang/uk/crud.php`
- `lang/en/crud.php`
- `resources/js/crud/config/fields.js`

## Out of scope (для наступних сесій)

- Синхронізація services з Busfor/Infobus API
- Відображення сервісів на публічному сайті (фронтенд пошуку рейсів)
- Bulk-операція "застосувати набір сервісів до групи автобусів"
- Окремий CRUD довідника сервісів (якщо знадобиться адмін-керування)
- Підтвердження npm run build

## Пов'язані нотатки

- [[bus-photo-field]] — попередня сесія по полю photo у Bus
