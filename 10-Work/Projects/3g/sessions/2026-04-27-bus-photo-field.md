---
title: "Проект: 3G — Додано поле photo для автобуса"
date: 2026-04-27
tags: [work, session, 3g, bus, photo, image]
category: work
project: 3g
status: completed
pinecone_indexed: false
---

## Мета сесії
Додати окреме поле `photo` до автобуса — незалежне від галереї, для прикріплення у повідомленнях.

## Виконано

| Задача | Результат |
|--------|-----------|
| Міграція `add_photo_to_buses_table` | Колонка `photo` (string, nullable) після `visible` |
| `Bus::$fillable` | Додано `photo` |
| `Bus` — трейт `StoreImageHelper` | Мутатор `setPhotoAttribute` зберігає файл у `uploads/buses/` |
| `Bus::boot()` | `deleting` хук — видаляє файл з диску при видаленні автобуса |
| `BusesCrudController` | Поле `type: image`, лейбл "Фото для повідомлень", вкладка "Картинки" |

## Важливі рішення (ADR)

| Рішення | Причина |
|---------|---------|
| Окреме поле `photo`, не через `Gallery` | Незалежне від галереї, потрібне для повідомлень |
| `StoreImageHelper` — той самий патерн | Єдиний підхід у проекті для одиночних зображень |
| WebP конвертацію не додавали | Bus не потребує WebP версії |
| `boot::deleting` хук | При видаленні автобуса файл photo прибирається з диску |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| `SQLSTATE[22001]: String data, right truncated` | `ImageField.vue` надсилає base64 — потрібен мутатор, а не пряме збереження у VARCHAR |

## Патерн зображень у проекті
- `ImageField.vue` → base64 → `set{Field}Attribute` → `StoreImageHelper` → файл на диску
- Оригінал: `uploads/{folder}/{md5}.{ext}`
- WebP (тільки деякі моделі): `uploads/webp/{md5}.webp` через `ConvertImages` трейт
- При заміні — старий файл **не видаляється** (загальна поведінка)
- При видаленні — тільки якщо є `boot::deleting` хук

## Артефакти
- `database/migrations/2026_04_27_103813_add_photo_to_buses_table.php`
- `app/Entities/Tenant/Directories/Bus.php`
- `app/Http/Controllers/Api/Crud/Directories/BusesCrudController.php`

## Пов'язані нотатки
- [[project-overview]]