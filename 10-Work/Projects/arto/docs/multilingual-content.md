---
title: "Проект: arto — мультимовність контенту"
date: 2026-10-08
tags: [arto, work, architecture]
category: architecture
project: arto
status: active
aliases: []
pinecone_indexed: false
---

# Мультимовність контенту

- Перекладні значення живуть у поліморфній таблиці `texts` (entity_type/entity_id/lang), а не в колонках сутності. Модель — `use ModelHasTexts`.
- Колонки `texts`: title, subtitle, content, subcontent, characteristics (json), city, address, image_title, image_caption, meta_*, url.
- Перекладні сутності: Page, WidgetPage, Menu/MenuItems, Slider, Category, Event, GalleryCategory/Item, Delivery/PaymentMethod, **Product, ProductCategory, ProductType, ProductColor, ProductSize, TradePoint** (останні 6 — з 2026-10-08, міграція `2026_10_08_000007` перенесла колонки в `texts` мовою за замовчуванням і видалила колонки).
- Fallback: `protected $textsFallbackToDefault = true` → `$model->title` на сайті бере мову за замовчуванням, якщо перекладу немає. `getText($attr, $lang)` з явною мовою (форми адмінки) — без fallback.
- Валідація: `App\Http\Requests\CRUD\Concerns\TranslatableRules::translatable($field, $rules, $required)` — обовʼязково в мові за замовчуванням.
- Адмінка: поле CRUD `'translatable' => true`; підтримують Text, TextArea, Wysiwyg, KeyValue (з 2026-10-08).
- Запити: `withContents()` для eager-load, пошук — `whereHas('texts', ...)`.
