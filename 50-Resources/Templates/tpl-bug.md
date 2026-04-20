---
title: "<% tp.file.rename("bug-" + await tp.system.prompt("Коротко про баг")) %>"
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [work, bug, solution]
category: work
project: <% await tp.system.prompt("Назва проекту") %>
status: <% await tp.system.suggester(["open", "solved", "wontfix"], ["open", "solved", "wontfix"]) %>
pinecone_indexed: false
---

## 🐛 Проблема

_Що відбувається? Яка помилка?_

## 🔍 Контекст

- **Проект:**
- **Середовище:**
- **Коли виникає:**

## 🧪 Кроки відтворення

1.
2.
3.

## 💡 Причина

_Чому це відбувається?_

## ✅ Рішення

```

_Код або опис вирішення_

## 📚 Джерела

-
