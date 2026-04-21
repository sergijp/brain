---
title: "Трейдинг: 2026-04-21 — EURUSD LONG Setup"
date: 2026-04-21
tags: [trading, journal, session, eurusd, smc, long]
category: trading
status: completed
pinecone_indexed: false
---

## 📊 Огляд дня
- **Депозит**: $10,000
- **Дата**: 2026-04-21
- **Сесія**: NY (після London KZ)
- **Інструмент**: EURUSD, 5m chart

## 🔍 Аналіз (SMC Top-Down)

### HTF Bias (H4/H1)
- Bias: **Bullish** — структура HH/HL на H4 підтверджена
- Ціна вище ключового H4 OB

### LTF Сетап (5m)
- **SSL Sweep** на 1.17200 ✅ — стопи під Asian Low зняті
- **BOS UP** на рівні 1.17638 ✅ — свічка +23 pips, об'єм 3504
- Pullback до 1.17320 (ретест BOS зони / bullish FVG)

## 📈 Trade Plan

| Рівень | Ціна | Пункти | P&L |
|--------|------|--------|-----|
| ⚡ Entry | 1.17320 | — | — |
| ⛔ SL | 1.17160 | −16 pips | −$100 |
| ✅ TP1 | 1.17638 | +31.8 pips | +$200 |
| 🎯 TP2 | 1.17800 | +48 pips | +$302 |
| 🚀 TP3 | 1.18492 | +117 pips | +$737 |
| **Lot** | **0.63** | RR TP2: 1:3 | — |

**Формула лоту**: $100 / (16 pips × $10) = 0.625 → округлено 0.63

## 💡 Ключові спостереження
- SSL sweep перед BOS — класичний ICT/SMC сетап підтверджений
- BOS свічка сильна (23 pips, великий об'єм) — momentum є
- Pullback до ретесту BOS зони = оптимальна точка входу
- TP2 на рівні PDH — логічна ціль ліквідності

## ⚠️ Помилки й навчання
- Спроби намалювати Long Position через native TV tools не вийшли (drag interaction не автоматизується через CDP)
- Найкращий підхід для Trade Plan на графіку — **Pine Script** (Варіант B)

## 🎯 План на завтра
- Перевірити чи досяг TP1 (1.17638)
- При TP1 → перенести SL в беззбиток (1.17320)
- Спостерігати за структурою на H1 для TP2/TP3

---

## 📈 Сетап 2: GBPUSD LONG (SMC 15m)

### LTF Сетап (15m)
- **SSL Sweep** на 1.34760 ✅ — стопи під поточним локальним мінімумом зняті
- **BOS UP** до 1.35258 ✅ — свічка +34.8 pips (bullish impulse)
- Pullback до 1.34840, entry limit на 1.34900 (OB/BOS retest)

| Рівень | Ціна | Пункти | RR |
|--------|------|--------|-----|
| ⚡ Entry | 1.34900 | — | — |
| ⛔ SL | 1.34730 | −17 pips | — |
| ✅ TP1 | 1.35258 | +35.8 pips | 1:2.1 |
| 🎯 TP2 | 1.35500 | +60 pips | 1:3.5 |
| 🚀 TP3 | 1.35800 | +90 pips | 1:3.3 |
| **Lot** | **0.59** | Ризик $100 | ✅ |

### Confluences
- H4 bias bullish (від 1.33809 до 1.35996)
- H1 показав SSL sweep + відновлення
- Збіг зі структурою EURUSD → USD weakness bias підтверджений
- Обидва сетапи в один час (NY session open)

---

## 💡 Ключові спостереження
- Обидва інструменти (EUR та GBP) показали ідентичну SMC структуру в один час → сильний сигнал USD weakness
- SSL sweep → BOS UP → pullback = стандартний ICT сетап підтверджений двічі
- Pine Script Trade Plan малюється автоматично через MCP workflow

## 🔗 Пов'язані нотатки
- [[10-Work/Projects/tradingview-mcp/sessions/2026-04-21-pine-script-obsidian-setup]]
- [[10-Work/Projects/tradingview-mcp/sessions/2026-04-21-tradingview-mcp-tools-reference]]
- [[10-Work/Projects/tradingview-mcp/sessions/2026-04-21-analysis-draw-workflow]]
