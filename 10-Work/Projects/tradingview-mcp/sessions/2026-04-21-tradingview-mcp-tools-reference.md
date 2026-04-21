---
title: "TradingView MCP — повний довідник 78 інструментів"
date: 2026-04-21
tags: [work, session, tradingview-mcp, reference, tools]
category: work
project: tradingview-mcp
status: completed
pinecone_indexed: false
---

## Мета сесії
Задокументувати всі доступні TradingView MCP інструменти з прикладами використання для швидкого доступу в майбутніх сесіях.

## Виконано
- Досліджено та класифіковано всі 78 інструментів TradingView MCP
- Виявлено ключові паттерни роботи з drawings через JS API
- Знайдено правильну назву shape для short/long position (`short_position`, не `RiskRewardShort`)
- Задокументовано фікс для stop/profit рівнів через `setRawPoint`

## Важливі рішення (ADR)

| Рішення | Причина |
|---------|---------|
| Зберігати довідник в пам'яті | Щоб не витрачати час на пошук щоразу |
| Групувати інструменти по категоріях | Легше орієнтуватись |

## Повний довідник інструментів

### Запуск і з'єднання
```
tv_launch          → запустити TradingView Desktop (CDP порт 9222)
tv_health_check    → перевірити з'єднання
session_get/save   → сесія
```

### Читання стану графіка
```
chart_get_state        → символ, таймфрейм, всі індикатори + entity ID (викликати першим!)
quote_get              → real-time ціна, OHLC, volume
data_get_ohlcv         → свічки (summary:true для компактного, max 500 барів)
data_get_study_values  → значення індикаторів (RSI, MACD, EMA...)
symbol_info / symbol_search
```

### Pine Script drawings (індикатор має бути ВИДИМИМ)
```
data_get_pine_lines   → горизонтальні рівні (line.new)
data_get_pine_labels  → текстові підписи (label.new), max 50
data_get_pine_tables  → таблиці (table.new)
data_get_pine_boxes   → зони (box.new)
→ завжди використовувати study_filter="назва індикатора"
```

### Керування графіком
```
chart_set_symbol       → "EURUSD", "BTCUSD", "ES1!"
chart_set_timeframe    → "1","5","15","60","D","W"
chart_set_type         → "Candles","HeikinAshi","Line"
chart_manage_indicator → повна назва: "Relative Strength Index" не "RSI"
chart_scroll_to_date   → "2026-04-21"
chart_set_visible_range → unix timestamps
indicator_set_inputs   → параметри індикатора
indicator_toggle_visibility
```

### Малювання (draw_shape)
```
shape types: horizontal_line, vertical_line, trend_line, rectangle, text

overrides для horizontal_line:
{ linecolor, linewidth, linestyle, showLabel, text, textcolor, fontsize, bold }
```

### Short/Long Position — JS API (через ui_evaluate)
```javascript
const cw = window.TradingViewApi._activeChartWidgetWV.value();

// 1. Створити (shape: 'short_position' або 'long_position')
cw.createMultipointShape(
  [{ time: lastBarTime, price: entryPrice }],
  { shape: 'short_position', overrides: { stopLevel, profitLevel } }
);

// 2. ОБОВ'ЯЗКОВО виправити рівні через setRawPoint
const obj = cw.getShapeById(id);
obj.setRawPoint(2, { index: 241, price: stopPrice });   // STOP
obj.setRawPoint(3, { index: 241, price: profitPrice }); // TAKE PROFIT

// 3. Зробити завжди видимим
obj.setPoints([
  { price: entry, time: 1776470400 }, // минуле
  { price: entry, time: 1800000000 }  // Sep 2027
]);
obj.setProperties({ alwaysShowStats: true });

// Інші корисні методи
cw.getAllShapes()           // [{id, name}, ...]
cw.removeEntity(id)        // видалити
obj.getProperties()        // стилі, stopLevel, profitLevel
obj.getRawPoints()         // всі 4 точки drawing
```

### Алерти
```
alert_create  → condition: "crossing"/"greater_than"/"less_than"
alert_list    → список активних
alert_delete  → видалити
```

### Pine Script pipeline
```
pine_new → pine_set_source → pine_smart_compile → pine_get_errors → pine_save
pine_get_console  → log.info() вивід
pine_get_source   → ⚠️ може бути 200KB+, уникати
```

### Replay
```
replay_start(date) → replay_step → replay_trade(buy/sell/close) → replay_stop
replay_autoplay(speed) → replay_status
```

### Batch
```javascript
batch_run({ symbols: ["EURUSD","GBPUSD"], action: "screenshot" })
```

### UI навігація
```
ui_click(by, value)    → by: "aria-label"/"data-name"/"text"
ui_evaluate(js)        → виконати JavaScript
ui_keyboard(key)       → "Escape", "Enter", modifiers: ["ctrl"]
ui_mouse_click(x, y)   → клік по координатах
ui_open_panel          → pine-editor, strategy-tester, watchlist
capture_screenshot     → region: "full"/"chart"/"strategy_tester"
```

### Тулбар інструментів (data-name)
```
FavoriteToolbarLineToolRiskRewardShort
FavoriteToolbarLineToolRiskRewardLong
```

### Layouts / Tabs / Panes
```
layout_list/switch
tab_list/new/switch/close
pane_list/focus/set_layout/set_symbol
```

### Інші
```
morning_brief      → огляд ринку
watchlist_get/add
depth_get          → стакан Level 2
data_get_equity / trades / strategy_results
```

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| `RiskRewardShort` створює `flag` | Використовувати `'short_position'` |
| Stop/profit = entry ціна після створення | `setRawPoint(2, stop)` і `setRawPoint(3, profit)` |
| Drawing зникає за межами екрану | `setPoints` з великим time span |

## Артефакти
- Claude memory: `~/.claude/projects/-Users-serhiin/memory/tradingview_mcp_tools_reference.md`

## Пов'язані нотатки
- [[2026-04-21-eurusd-short-setup]]
- [[TradingView MCP]]
- [[ICT Trading Strategy]]
