---
title: "Проект: buktrek — Транслітерація імен файлів при завантаженні"
date: 2026-04-21
tags: [work, session, bustrek]
category: work
project: bustrek
status: completed
pinecone_indexed: false
---

## Мета сесії
Додати підтримку кастомних імен файлів при завантаженні через AppApi — файли мають зберігатись з іменами з масиву `names`, транслітерованими в латиницю, з пробілами замість `_`.

## Виконано

| Задача | Результат |
|---|---|
| Додати `names` параметр в `uploadFiles` | ✅ `array $names = []` |
| Транслітерація через `Transliterator` | ✅ `Any-Latin; Latin-ASCII; Lower()` |
| Fallback якщо назва порожня/помилкова | ✅ md5-хеш від оригінальної назви |
| Розширення файлу з оригіналу | ✅ `getClientOriginalExtension()` |
| Передати `names` з контролера | ✅ `$request->input('names', [])` |

## Важливі рішення (ADR)

| Рішення | Причина |
|---|---|
| Використовувати існуючий `Transliterator` (з `ApplicationsCrudController`) | Не дублювати власну таблицю транслітерації |
| Розширення завжди з файлу, не з `names` | `names` — людська назва, не технічна |
| Fallback на md5 якщо `names` не передано | Зворотна сумісність зі старою поведінкою |

## Проблеми й як вирішили

- Граничні випадки в `names`: порожній рядок, null, лише спецсимволи → після `preg_replace` результат порожній → fallback на md5

## Артефакти

- `app/Services/AppApi/Services/FileUploadService.php` — методи `uploadFiles`, `storeFile`, `buildFileName`
- `app/Services/AppApi/Controllers/MemberController.php` — передача `names`

## Пов'язані нотатки
- [[project-overview]]
