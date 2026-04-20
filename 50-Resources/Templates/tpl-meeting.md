---
title: "<% tp.file.rename(tp.date.now("YYYY-MM-DD") + "-" + await tp.system.prompt("Тема зустрічі")) %>"
date: <% tp.date.now("YYYY-MM-DD") %>
time: <% tp.date.now("HH:mm") %>
tags: [work, meeting]
category: work
project: <% await tp.system.prompt("Проект (або Enter щоб пропустити)") %>
participants: []
pinecone_indexed: false
---

## 📋 Порядок денний

-

## 💬 Нотатки

<% tp.file.cursor(1) %>

## ✅ Рішення прийняті

-

## 📌 Action items

- [ ]  (@<% tp.date.now("YYYY-MM-DD") %>)

## ❓ Відкриті питання

-
