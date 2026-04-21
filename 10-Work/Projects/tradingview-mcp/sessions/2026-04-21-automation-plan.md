---
title: "TradingView MCP — Automation Plan (Signal + Draw + Telegram)"
date: 2026-04-21
tags: [work, session, tradingview, mcp, automation, telegram, smc]
category: work
project: tradingview-mcp
status: active
pinecone_indexed: false
---

## 🎯 Мета
Автоматизувати повний цикл: тригер → аналіз по SMC стратегії → малювання на графіку (Варіант A) → Telegram повідомлення зі скріншотом.

## 🔄 Процес

```
Тригер (розклад або TV Alert)
        ↓
Claude аналізує по стратегії
        ↓
Малює на графіку (Варіант A: long_position + TP2/TP3 horizontal_line)
        ↓
capture_screenshot
        ↓
Telegram: рівні + скріншот
```

## 🧩 Компоненти

| Компонент | Опис | Статус |
|-----------|------|--------|
| **Тригер** | Cron (розклад) або TV Alert → webhook | ❓ вибрати |
| **Orchestrator** | Claude CLI або Node.js скрипт → MCP tools | ❓ вибрати |
| **Draw** | Варіант A (long_position + horizontal_line) | ✅ готово |
| **Screenshot** | `capture_screenshot(region="chart")` | ✅ готово |
| **Telegram sender** | `sendPhoto(chatId, screenshot, caption)` | ⏳ зробити |

## 📲 Формат Telegram повідомлення

```
🚨 GBPUSD LONG сигнал (15m)
─────────────────────
⚡ Entry:  1.34900
⛔ SL:     1.34730  (−17p / −$100)
✅ TP1:    1.35258  RR 1:2.1
🎯 TP2:    1.35500  RR 1:3.5
🚀 TP3:    1.35800  RR 1:5.3
📦 Lot:    0.59
─────────────────────
[скріншот графіка]
```

## ❓ Відкриті питання (для наступної сесії)

1. **Тригер:** по розкладу (простіше) чи TV Alert в реальному часі (точніше)?
2. **Orchestrator:** Claude CLI `claude -p "намалюй GBPUSD"` чи Node.js скрипт з MCP tools напряму?

## 🔖 Що свідомо відкладено
- Торгова стратегія (Pine Script детектор SSL+BOS) — підключити пізніше
- HTF фільтр, сесійний фільтр, Daily DD check — другий ітерацією
- Telegram inline кнопки ("Беру" / "Пропускаю") — пізніше

## 🔗 Пов'язані нотатки
- [[10-Work/Projects/tradingview-mcp/sessions/2026-04-21-analysis-draw-workflow]]
- [[10-Work/Projects/tradingview-mcp/sessions/2026-04-21-tradingview-mcp-tools-reference]]
