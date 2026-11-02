---
title: "Проект: rodyna — закріплення статті вгорі категорії"
date: 2026-10-14
tags: [rodyna, work, session]
category: session
project: rodyna
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
На family.cv.ua дати змогу закріплювати статтю вгорі списку статей категорії (кейс: `jakscho_obrazhajut` у категорії `stop bullying`).

## Виконано
- Міграція `2026_10_14_120000_add_field_pinned_to_posts_table.php`: `posts.pinned` boolean default false.
- `Post`: `pinned` у `$fillable` і `$casts`.
- `Admin/PostCrudController`: поле «Закріплено» (select_from_array) на вкладці main.
- `Frontend/CategoryController::categoryPage`: статті категорії сортуються `orderByDesc('pinned')->latest()`.
- `resources/lang/uk/crud.php`: ключі `pinned`, `not_pinned`, `is_pinned`.

## Важливі рішення (ADR)
| Рішення | Чому |
|---|---|
| Прапорець `pinned` на пості, а не `pinned_post_id` на категорії | Пост належить рівно одній категорії (`category_id`), тож прапорець однозначний; мінімум змін |

## Проблеми й як вирішили
- Локально немає `php` — синтаксис не перевірено, на проді потрібно `php artisan migrate`.

## Артефакти
- `php artisan migrate` на сервері; далі в адмінці відкрити статтю → «Закріплено вгорі».

## Пов'язані нотатки
