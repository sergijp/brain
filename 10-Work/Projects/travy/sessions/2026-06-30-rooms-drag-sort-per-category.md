---
title: "Проект: Travy — drag-сортування кімнат у межах категорії"
date: 2026-06-30
tags: [travy, work, session, crud, reorder, vue]
category: session
project: travy
status: completed
aliases: ["Rooms reorder per category", "Сортування румсів по категорії"]
pinecone_indexed: false
---

# Travy — drag-сортування кімнат у межах категорії

## Мета сесії
Дати можливість в адмінці сортувати кімнати (`rooms`) drag'ом **у межах кожної категорії** (`categories`), вивести цей функціонал у зручному місці, і відобразити той самий порядок на публічному сайті (список будиночків).

## Виконано

| Задача | Результат |
|---|---|
| Backend: поле порядку | Міграція `add_order_to_rooms_table` — поле `order` (unsignedInteger, default 0), **без backfill у міграції** (за рішенням замовника) |
| Авто-order для нових кімнат | `Room::creating` hook → `max(order)+1` у межах своєї `category_id` (`static::`) |
| Scoped reorder | `RoomsCrudController` підключив `ReorderOperation` + перевизначив `reorder()` зі scope `where('category_id', ...)` через `Room::query()` (за зразком `MenuItemsCrudController`) |
| Фільтр категорії | `addFilter` `select_from_relation_ajax` + ендпойнт `categoryFilterSearch()` + маршрут `rooms.filter-search-category` |
| UX-вхід (Варіант A) | Колонка-кнопка «Сортувати кімнати» у списку **Категорії** → веде у список **Кімнати**, відфільтрований по категорії, з drag-хендлами |
| Deep-link фільтрів (frontend) | `LinkColumn` (route-query + статичний text), `ListViewManager.applyQueryFilters()` читає query до першого завантаження, `ListActiveFilter` guard від undefined-фільтра |
| Нормалізація даних | Одноразовий tinker-скрипт пересортував `order` для 3 наявних кімнат (інакше при всіх `order=0` drag = no-op) |
| Публічний сайт | `PageController::houses()` — `Room::query()->active()->orderBy('order')->get()->groupBy('category_id')` |

## Важливі рішення (ADR)

| Рішення | Чому |
|---|---|
| Варіант A (кнопка з категорії → відфільтрований список кімнат) замість окремої вкладеної сторінки (C) чи фільтра в Rooms (B) | Максимальне переви­користання наявної машинерії (`ListTable` draggable + фільтри), чіткий UX «одна категорія = один екран», мінімум нового Vue-коду |
| Scope reorder по FK `category_id`, **не** через relation | `category_id` уже на моделі — relation дав би зайвий запит; масовий increment/decrement усе одно на query-білдері |
| Backfill — поза міграцією (окремий runtime-скрипт) | Рішення замовника: міграція лише додає поле. Eloquent у міграціях небажаний |
| `'fake_column' => true` для колонки `sort_rooms` | Інакше `ListOperation` робить `$entity->append('sort_rooms')` → `getSortRoomsAttribute()` не існує → `BadMethodCallException` |
| Deep-link через convention `?<name>=id&<name>_label=label` | Універсально для relation-ajax фільтрів, дає коректний chip + prefill v-select, без прив'язки до async-конфігу фільтрів |

## Проблеми й як вирішили
- **`BadMethodCallException: getSortRoomsAttribute()`** — список аппендив віртуальну колонку як accessor. Фікс: `'fake_column' => true` на колонці `sort_rooms`.
- **`static::` у `reorder()` контролера** спершу помилково вказував на контролер, а не модель → виправлено на `Room::query()`.
- **Існуючі кімнати з `order=0`** → drag був би no-op. Фікс: одноразова нормалізація через tinker.

## Артефакти

**Backend**
- `database/migrations/2026_06_30_120000_add_order_to_rooms_table.php`
- `app/Entities/System/Content/Room.php` (fillable + creating hook)
- `app/Http/Controllers/Api/Crud/Content/RoomsCrudController.php` (ReorderOperation, filter, categoryFilterSearch, reorder override)
- `app/Http/Controllers/Api/Crud/Content/CategoriesCrudController.php` (колонка sort_rooms)
- `routes/api.php` (`rooms.filter-search-category`)
- `app/Http/Controllers/Frontend/PageController.php:52` (orderBy order)

**Frontend**
- `resources/js/crud/base/columns/LinkColumn.vue` (route-query + text)
- `resources/js/crud/base/operations/list/ListViewManager.vue` (applyQueryFilters)
- `resources/js/crud/base/operations/list/active-filters/ListActiveFilter.vue` (guard)

**Команди**
```bash
php artisan migrate --force          # застосовано
npm run build                        # ✓ built (фронтенд-зміни)
# нормалізація order (одноразово, через tinker) — пересортувала 3 кімнати
```
Маршрути перевірені: `rooms.reorder` (POST), `rooms.filter-search-category` (GET).

## Як працює (UX)
Адмінка → **Категорії** → «Сортувати кімнати» → список **Кімнати** відфільтрований по категорії з drag → `POST /system/rooms/reorder {from_id,to_id}` зсуває `order` лише в межах категорії. Публічний сайт (`pages.houses.index`) виводить кімнати кожної категорії за `order`.

## Пов'язані нотатки
- [[travy]]
- Патерн scoped-reorder: аналог `MenuItemsCrudController`
