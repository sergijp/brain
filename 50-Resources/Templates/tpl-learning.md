---
title: "<% tp.file.rename(await tp.system.prompt("Назва книги / статті")) %>"
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [learning]
category: learning
type: <% await tp.system.suggester(["book", "article", "course", "video", "podcast"], ["book", "article", "course", "video", "podcast"]) %>
author: <% await tp.system.prompt("Автор (або Enter щоб пропустити)") %>
source:
status: <% await tp.system.suggester(["reading", "completed", "on-hold"], ["reading", "completed", "on-hold"]) %>
rating:
pinecone_indexed: false
---

## 💡 Про що

_2-3 речення_

## 🔑 Ключові ідеї

1.
2.
3.

## 📝 Нотатки по ходу читання

### Частина 1


## 💬 Цитати

>

## 🔧 Практичне застосування

_Як можу використати у роботі або трейдингу?_

## 🔗 Пов'язані матеріали

-
