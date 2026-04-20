---
title: "<% tp.file.rename(await tp.system.prompt("Пара і таймфрейм, напр: EURUSD-H4")) %>"
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [trading, analysis]
category: trading
pair: <% await tp.system.prompt("Валютна пара / інструмент") %>
timeframe: <% await tp.system.prompt("Таймфрейм") %>
bias: <% await tp.system.suggester(["bullish", "bearish", "neutral"], ["bullish", "bearish", "neutral"]) %>
pinecone_indexed: false
---

## 📊 Технічний аналіз

**Тренд (старший TF):**

**Ключові рівні:**
- Resistance:
- Support:
- POI (Point of Interest):

**Структура ринку:**

## 🎯 Сетап

**Умова входу:**

**Вхід:**
**Stop Loss:**
**Take Profit 1:**
**Take Profit 2:**
**R:R:**

## 📰 Фундаментал

**Важливі новини / події:**

## ⏰ Тригери для входу

- [ ]
- [ ]

## 📌 Нотатки

