---
title: "Проект: VTS (onchul) — Bus Services CRUD"
date: 2026-06-19
tags: [onchul, work, session, vts, bus-services]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
Реалізація функціоналу "Послуги автобуса" (Bus Services) — додання набору послуг (WiFi, туалет, кондиціонер тощо) з адміністративним CRUD інтерфейсом та виведенням у публічні трип-ресурси.

## Виконано

| Задача | Результат |
|--------|-----------|
| Backend: каталог послуг (config) | ✅ Створено `config/bus_services.php` з 20 послуг + icon/translation_key |
| Backend: схема БД (migration) | ✅ `2026_06_19_101753_add_services_to_buses_table.php` + `php artisan migrate` |
| Backend: модель Bus (fillable + cast) | ✅ `services` додано у fillable + array cast |
| Backend: CRUD контролер | ✅ `BusesCrudController` - нове поле типу `bus_services` у табі "Сервіси" |
| Backend: переклади (uk/en) | ✅ 20 послуг + ключ `bus_services` у обох мовах |
| Backend: ресурси для API | ✅ `TripListResource` та `TripInfoResource` - метод `enrichServices()` + поле `bus_services` |
| Frontend: Vue компонент | ✅ `BusServicesField.vue` - checkbox-grid з іконками (Options API + FieldMixin) |
| Frontend: реєстрація поля | ✅ `resources/js/crud/config/fields.js` - import + registry entry |
| SVG іконки (20 шт.) | ✅ Створено у `public/images/icons/services/` - Material Design стиль |

## Важливі рішення (ADR)

| Рішення | Чому | Альтернативи |
|---------|------|--------------|
| Модель Bus знаходиться у `app/Entities/System/Content/Bus.php` | За архітектурою проекту - Content (не Tenant) | Зразок мав `Tenant/Bus` |
| Cast для `services` - нативний `'array'` | Простота, жодних спеціальних трансформацій | Кастомний `Json::class` (як у `phones`/`places`) |
| `enrichServices()` додано напряму у Resource-класи | Busfor API не має ендпоінту для послуг автобуса | Запит до зовнішнього API |
| Дві окремі реалізації методу у `TripListResource` та `TripInfoResource` | Кожна готує свої дані для JSON response | DRY trait (перш за все, работало швидше) |
| SVG іконки як простий філлер | Мінімальні залежності, легко розширяти | Font Icon + бібліотека (Material Icons, FontAwesome) |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Bus модель виявилась у System/Content, не у Tenant | Перевірив структуру проекту `app/Entities/` - портував за фактичною архітектурою |
| CRUD поле типу `bus_services` не існував | Створив новий Vue компонент з Options API + FieldMixin, зареєстрував у `fields.js` |
| Busfor API не знайдено за послугами автобуса | Реалізував direct SQL - на Eloquent моделі сранизу `services` JSON |
| Іконки потрібні до фронтенду | Створив 20 простих SVG з Material Design стилем у `public/images/icons/services/` |

## Артефакти

### Файли створені
- `config/bus_services.php`
- `database/migrations/2026_06_19_101753_add_services_to_buses_table.php`
- `resources/js/crud/base/fields/BusServicesField.vue`
- `public/images/icons/services/` — 20 SVG іконок

### Файли змінені
- `app/Entities/System/Content/Bus.php` — `$fillable`, `$casts`
- `app/Http/Controllers/Api/Crud/Content/BusesCrudController.php` — CRUD поле
- `lang/uk/crud.php` — 20 перекладів + `bus_services`
- `lang/en/crud.php` — 20 перекладів EN
- `app/Http/Resources/TripListResource.php` — `enrichServices()` + поле
- `app/Http/Resources/TripInfoResource.php` — `enrichServices()` + поле
- `resources/js/crud/config/fields.js` — реєстрація поля

### Команди запущені
```bash
php artisan migrate
```

### Послуги (config)
```
WiFi, Туалет, Кондиціонер, Гарячий напиток, Холодний напиток, 
Видео розваги, Розетка, USB, Постільна білизна, Подушка, 
Ковдра, Полотенце, Закуски, Гідробус, Масаж крісла, 
Гарячий лосьйон, Аптечка, Вікна z-шторками, Туалет з раковиною, Косметичка
```

## Пов'язані нотатки
- [[Bus Entity Architecture]] (якщо існує)
- [[CRUD System Overview]] (фреймворк CRUD у проекті)
- [[API Resources & Serialization]] (TripListResource, TripInfoResource)
