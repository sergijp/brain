---
title: "Bus Photo — окреме фото для повідомлень"
date: 2026-05-08
tags: [3g, architecture, bus, image, storage]
category: docs
project: 3g
status: active
aliases: ["3g-bus-photo"]
pinecone_indexed: false
---

# Bus Photo — окреме фото для повідомлень

Поле `photo` у `Bus`, незалежне від галереї `media`. Призначене для прикріплення у sms/viber повідомленнях клієнтам.

**Why:** галерея `Bus` через `morphMany Gallery` — для адмінки/каталогу. У повідомленнях треба одне конкретне фото, контрольоване окремо.

## Що зроблено (2026-04-27)

- Міграція: `2026_04_27_103813_add_photo_to_buses_table.php` — колонка `photo` (string, nullable).
- `Bus::$fillable` — додано `photo`.
- `Bus` — підключено трейт `StoreImageHelper`, `setPhotoAttribute` (зберігає в `uploads/buses/`).
- `Bus::boot()` — при видаленні `Bus` файл `photo` видаляється з диску.
- `BusesCrudController` — поле `type: image`, лейбл "Фото для повідомлень", вкладка "Картинки".

## Патерн збереження зображень у проекті

- `ImageField.vue` надсилає base64 → мутатор `set{Field}Attribute` декодує і зберігає файл.
- Трейт `StoreImageHelper::handleStoreImageAttribute` — оригінал у `uploads/{folder}/`.
- Трейт `ConvertImages` — деякі моделі додатково генерують WebP у `uploads/webp/` (Bus — **не** використовує).
- При **заміні** фото старий файл **не видаляється** (загальна поведінка).
- При **видаленні** запису — видаляється тільки якщо є `boot::deleting` хук.

## Споживач

`TicketNotificationService::buildBusPhotoUrl(?Bus)` — перевіряє існування файлу через `Storage::disk('public')->exists()` перед побудовою URL для плейсхолдера `[busphoto]`.

## Пов'язані

- [[INDEX]]
- [[notifications]] — споживач `[busphoto]`
