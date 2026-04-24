---
title: Інструкція з виставлення позицій у TradingView MCP
date: 2026-04-24
tags: [tradingview, mcp, guide, trading]
category: Trading
project: tradingview-mcp-jackson
status: active
pinecone_indexed: true
---

# Як правильно ставити позиції через TradingView MCP

Щоб виставити стандартний інструмент "Long/Short Position" з відображенням PnL та Risk/Reward, потрібно використовувати інструмент `draw_shape` з наступними параметрами:

## 1. Довга позиція (Long)
**Інструмент:** `draw_shape`
- `shape`: `"long_position"`
- `overrides`: `{"stopLevel": X, "profitLevel": Y, "showLabels": true}`
- `point`: `{price: ENTRY_PRICE, time: TIMESTAMP}`

## 2. Коротка позиція (Short)
**Інструмент:** `draw_shape`
- `shape`: `"short_position"`
- `overrides`: `{"stopLevel": X, "profitLevel": Y, "showLabels": true}`
- `point`: `{price: ENTRY_PRICE, time: TIMESTAMP}`

## Важливо про рівні (Levels):
Рівні `stopLevel` та `profitLevel` вказуються в **пунктах (ticks/points)** від точки входу:
- Для EUR/USD (5 знаків): 1 піпс = 10 пунктів. Тобто 15 піпсів = `150`.
- Для Gold/Indices: згідно з мінімальним кроком ціни.

[[20-Trading/Journal/2026-04-24-trading-session|Переглянути сьогоднішню сесію]]
