---
title: "TradingView MCP — Інструменти та Workflow"
date: 2026-04-21
tags: [trading, tools, tradingview, mcp, pine-script, workflow]
category: trading
status: active
pinecone_indexed: false
---

# 🛠️ TradingView MCP — Інструменти та Workflow

## ⚙️ Налаштування

| Компонент | Деталі |
|-----------|--------|
| Репо | `~/tradingview-mcp-jackson` |
| Реєстрація | `claude mcp add --scope user tradingview -- node ~/tradingview-mcp-jackson/src/server.js` |
| Запуск TV | `~/tradingview-mcp-jackson/scripts/launch_tv_debug_mac.sh` |
| Якщо CDP не відповідає | Використати `tv_launch` tool |
| Конфіг стратегії | `~/tradingview-mcp-jackson/rules.json` |

---

## 📋 Стандартний Workflow Аналізу

```
1. chart_set_symbol("EURUSD")
2. chart_set_timeframe("240")        ← H4: визначити bias
   → quote_get()
   → data_get_ohlcv(summary=true)
   → data_get_pine_labels()
   → data_get_pine_boxes()
   → data_get_pine_lines()
   → capture_screenshot(region="chart")

3. chart_set_timeframe("60")         ← H1: контекст, OB/FVG зони

4. chart_set_timeframe("5")          ← 5m: тригер входу
   → data_get_ohlcv(count=20)        ← останні бари
   → capture_screenshot()

5. Розрахувати:
   → Bias: bullish / bearish / neutral
   → Entry, SL, TP1, TP2, TP3
   → Lot = $100 / (risk_pips × $10)

6. Намалювати Trade Plan (Pine Script)
```

---

## 🎨 Trade Plan на Графіку (Pine Script — Варіант B)

### Workflow
```
1. pine_set_source(source=PINE_CODE)
2. pine_smart_compile()
3. Якщо study_added: false → ui_mouse_click(x=2400, y=79)
4. chart_get_state() → перевірити "Trade Plan" в studies[]
```

### UI Координати (verified via DOM, Retina 2x дисплей)
| Елемент | CSS координати |
|---------|---------------|
| "Добавить на график" | x=2400, y=79 |
| Pine Editor кнопка | x=2548, y=1290 |

### Pine Script Шаблон
```pine
//@version=6
indicator("Trade Plan — EURUSD LONG", overlay=true, max_boxes_count=10, max_labels_count=20, max_lines_count=10)

entry = input.float(0.0, "Entry",     step=0.00001)
sl    = input.float(0.0, "Stop Loss", step=0.00001)
tp1   = input.float(0.0, "TP1",       step=0.00001)
tp2   = input.float(0.0, "TP2",       step=0.00001)
tp3   = input.float(0.0, "TP3",       step=0.00001)
lots  = input.float(0.0, "Lot Size",  step=0.01)

risk_pips = math.round((entry - sl)    * 10000, 1)
tp1_pips  = math.round((tp1   - entry) * 10000, 1)
tp2_pips  = math.round((tp2   - entry) * 10000, 1)
tp3_pips  = math.round((tp3   - entry) * 10000, 1)
risk_usd  = math.round(lots * risk_pips * 10, 0)
tp1_usd   = math.round(lots * tp1_pips  * 10, 0)
tp2_usd   = math.round(lots * tp2_pips  * 10, 0)
rr1       = math.round(tp1_pips / risk_pips, 1)
rr2       = math.round(tp2_pips / risk_pips, 1)
rr3       = math.round(tp3_pips / risk_pips, 1)

if barstate.islast
    t1 = bar_index - 3
    t2 = bar_index + 80
    box.new(t1, entry, t2, sl,    bgcolor=color.new(color.red,   82), border_color=color.new(color.red,   20), border_width=1)
    box.new(t1, tp1,   t2, entry, bgcolor=color.new(color.green, 85), border_color=color.new(color.green, 40), border_width=1)
    box.new(t1, tp2,   t2, tp1,   bgcolor=color.new(color.green, 75), border_color=color.new(color.green, 20), border_width=1)
    line.new(t1, tp3, t2, tp3, color=color.new(color.teal, 10), width=2, style=line.style_dashed)
    label.new(t2, sl,    text="⛔ SL  "   + str.tostring(sl)    + "\n−" + str.tostring(risk_pips) + " pips  |  −$" + str.tostring(risk_usd),                                                   style=label.style_label_left, color=color.new(color.red,    5), textcolor=color.white, size=size.normal)
    label.new(t2, entry, text="⚡ ВХІД  " + str.tostring(entry) + "\n" + str.tostring(lots) + " lot  |  Ризик $" + str.tostring(risk_usd) + "  (" + str.tostring(risk_pips) + " pips)",        style=label.style_label_left, color=color.new(color.orange, 5), textcolor=color.white, size=size.normal)
    label.new(t2, tp1,   text="✅ TP1  "  + str.tostring(tp1)   + "\n+" + str.tostring(tp1_pips) + " pips  |  +$" + str.tostring(tp1_usd) + "  RR 1:" + str.tostring(rr1),                    style=label.style_label_left, color=color.new(color.green,  5), textcolor=color.white, size=size.normal)
    label.new(t2, tp2,   text="🎯 TP2  "  + str.tostring(tp2)   + "\n+" + str.tostring(tp2_pips) + " pips  |  +$" + str.tostring(tp2_usd) + "  RR 1:" + str.tostring(rr2),                    style=label.style_label_left, color=color.new(#00aa00,      5), textcolor=color.white, size=size.normal)
    label.new(t2, tp3,   text="🚀 TP3  "  + str.tostring(tp3)   + "\n+" + str.tostring(tp3_pips) + " pips  |  RR 1:" + str.tostring(rr3),                                                     style=label.style_label_left, color=color.new(color.teal,   5), textcolor=color.white, size=size.normal)
```

---

## 🔧 Основні MCP Інструменти

### Читання графіку
| Інструмент | Призначення |
|-----------|-------------|
| `chart_get_state` | Symbol, timeframe, всі індикатори з entity IDs |
| `quote_get` | Real-time ціна, OHLC, volume |
| `data_get_ohlcv(summary=true)` | Компактна статистика барів |
| `data_get_study_values` | Числові значення індикаторів (RSI, MACD, EMA...) |
| `data_get_pine_labels` | Текстові аннотації від Pine індикаторів |
| `data_get_pine_boxes` | Цінові зони (OB, FVG...) |
| `data_get_pine_lines` | Горизонтальні рівні від Pine індикаторів |

### Зміна графіку
| Інструмент | Приклад |
|-----------|---------|
| `chart_set_symbol` | `"EURUSD"`, `"XAUUSD"` |
| `chart_set_timeframe` | `"5"`, `"15"`, `"60"`, `"240"`, `"D"` |
| `capture_screenshot` | `region="chart"` або `"full"` |

### Pine Script
| Інструмент | Призначення |
|-----------|-------------|
| `pine_set_source` | Інжектувати код в редактор |
| `pine_smart_compile` | Компілювати + перевірити помилки |
| `pine_get_errors` | Читати помилки компіляції |
| `pine_save` | Зберегти в TradingView cloud |

### UI Автоматизація
| Інструмент | Призначення |
|-----------|-------------|
| `ui_mouse_click(x, y)` | Клік за координатами |
| `ui_evaluate` | Виконати JS в контексті TV (DOM queries) |
| `ui_open_panel` | Відкрити/закрити панелі (pine-editor, alerts...) |

---

## ⚠️ Відомі обмеження

| Проблема | Вирішення |
|---------|-----------|
| `pine_smart_compile` → `study_added: false` | Клік `ui_mouse_click(x=2400, y=79)` |
| Native Long/Short Position tool | Не автоматизується (drag interaction) → використовувати Pine Script |
| `draw_shape` обмежений | Тільки: horizontal_line, vertical_line, trend_line, rectangle, text |
| Pine Editor не відкривається через `ui_open_panel` | Відкрити вручну або через `pine_set_source` |
| TV не запускається | Використати `tv_launch` tool |

---

## 🔗 Пов'язані нотатки
- [[20-Trading/Strategies/smc-price-action-combo]]
- [[20-Trading/Resources/trading-rules]]
- [[10-Work/Projects/tradingview-mcp/sessions/2026-04-21-pine-script-obsidian-setup]]
