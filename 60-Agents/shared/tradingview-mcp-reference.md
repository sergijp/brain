---
title: "TradingView MCP — повний довідник інструментів і патернів"
date: 2026-05-08
tags: [trading, reference, tradingview, mcp]
category: reference
status: active
aliases: ["tv-mcp", "tradingview-mcp", "tv-tools-reference"]
pinecone_indexed: false
last_verified: 2026-05-08
---

# TradingView MCP — повний довідник

Усі 78 інструментів TradingView MCP, згруповані по категоріях. Глобально доступний через global `~/.claude/CLAUDE.md` → vault, тому підтягується в будь-якій сесії.

## Запуск і з'єднання

| Інструмент | Призначення | Примітка |
|-----------|-------------|---------|
| `tv_launch` | Запустити TradingView Desktop з CDP | Завжди першим, якщо TV не запущено |
| `tv_health_check` | Перевірити CDP з'єднання | Якщо інші інструменти падають з "CDP failed" |
| `tv_ui_state` | Отримати стан UI | |
| `session_get` | Отримати поточну сесію | |
| `session_save` | Зберегти сесію | |

## Читання стану графіка

| Інструмент | Призначення | Примітка |
|-----------|-------------|---------|
| `chart_get_state` | Символ, таймфрейм, список індикаторів з entity ID | **Викликати першим** на початку аналізу |
| `quote_get` | Real-time ціна, OHLC, volume | `symbol: ""` = поточний символ |
| `data_get_ohlcv` | Свічки OHLCV | `summary: true` для компактного виводу, `count: 100` max |
| `data_get_study_values` | Числові значення всіх індикаторів (RSI, MACD, EMA...) | |
| `symbol_info` | Інфо про символ | |
| `symbol_search` | Пошук символів | |

## Читання Pine Script drawings

| Інструмент | Призначення | Примітка |
|-----------|-------------|---------|
| `data_get_pine_lines` | Горизонтальні рівні від `line.new()` | Завжди `study_filter="назва індикатора"` |
| `data_get_pine_labels` | Текстові підписи від `label.new()` | |
| `data_get_pine_tables` | Таблиці від `table.new()` | |
| `data_get_pine_boxes` | Зони від `box.new()` | |
| `data_get_indicator` | Дані індикатора | Не використовувати для захищених |

## Керування графіком

| Інструмент | Призначення | Приклад |
|-----------|-------------|---------|
| `chart_set_symbol` | Змінити символ | `"EURUSD"`, `"BTCUSD"`, `"ES1!"` |
| `chart_set_timeframe` | Змінити таймфрейм | `"1"`, `"5"`, `"15"`, `"60"`, `"D"`, `"W"` |
| `chart_set_type` | Тип графіка | `"Candles"`, `"HeikinAshi"`, `"Line"` |
| `chart_manage_indicator` | Додати/видалити індикатор | Повна назва: `"Relative Strength Index"` не `"RSI"` |
| `chart_scroll_to_date` | Прокрутити до дати | `"2026-04-21"` |
| `chart_set_visible_range` | Встановити видимий діапазон | Unix timestamps |
| `chart_get_visible_range` | Отримати видимий діапазон | |
| `indicator_set_inputs` | Змінити параметри індикатора | |
| `indicator_toggle_visibility` | Показати/приховати індикатор | |

## Малювання — `draw_shape`

```
shape types: horizontal_line, vertical_line, trend_line, rectangle, text
```

**Overrides для horizontal_line:**
```json
{ "linecolor": "#FF0000", "linewidth": 3, "linestyle": 0,
  "showLabel": true, "text": "Label", "textcolor": "#FF0000",
  "fontsize": 14, "bold": true }
```

| Інструмент | Призначення |
|-----------|-------------|
| `draw_shape` | Намалювати лінію/прямокутник/текст |
| `draw_list` | Список всіх drawings |
| `draw_get_properties` | Властивості drawing |
| `draw_remove_one` | Видалити одне drawing |
| `draw_clear` | Видалити всі drawings |

## Short / Long Position через JS API

Правильна назва shape: **`short_position`** / **`long_position`** (НЕ `RiskRewardShort`, НЕ `LineToolRiskRewardShort`).

```javascript
cw.createMultipointShape(
  [{ time: lastBarUnixTime, price: entryPrice }],
  { shape: 'short_position', lock: false, overrides: { stopLevel, profitLevel } }
);
```

> `createMultipointShape` повертає Promise — не чекати результату, одразу перевіряти `getAllShapes()`.

### Проблема: stop / profit не відображаються

Після створення Points 2 і 3 мають ту саму ціну, що і entry.

**Рішення** — вручну виставити через `setRawPoint`:

```javascript
const obj = cw.getShapeById(shapeId);
obj.setRawPoint(0, { index: 165, price: entryPrice, time: startTime });
obj.setRawPoint(1, { index: 798, price: entryPrice, time: farFutureTime });
obj.setRawPoint(2, { index: 241, price: stopPrice });    // STOP LOSS
obj.setRawPoint(3, { index: 241, price: profitPrice });  // TAKE PROFIT
```

### Завжди видимий drawing

Розтягнути time span від минулого до далекого майбутнього:

```javascript
obj.setPoints([
  { price: entryPrice, time: 1776470400 }, // ~Apr 2026
  { price: entryPrice, time: 1800000000 }  // ~Sep 2027
]);
obj.setProperties({ alwaysShowStats: true });
```

### Підписані горизонтальні лінії

```javascript
draw_shape('horizontal_line', point, overrides: {
  linecolor: '#FF0000', linewidth: 3,
  showLabel: true, text: '⛔ STOP LOSS: X.XXXXX',
  textcolor: '#FF0000', fontsize: 14, bold: true
})
```

### Корисні методи `getShapeById`

- `getProperties()` / `setProperties(props)` — стилі, кольори, stopLevel, profitLevel
- `getPoints()` / `setPoints([...])` — точки прив'язки drawing
- `getRawPoints()` / `setRawPoint(idx, point)` — raw точки (для stop/profit)
- `getAllShapes()` → `[{ id, name }]` — список всіх drawings

### Активація інструментів тулбара

```javascript
ui_click({ by: 'data-name', value: 'FavoriteToolbarLineToolRiskRewardShort' })
ui_click({ by: 'data-name', value: 'FavoriteToolbarLineToolRiskRewardLong' })
```

## Алерти

| Інструмент | Призначення |
|-----------|-------------|
| `alert_create` | Створити алерт (`condition: "crossing"/"greater_than"/"less_than"`) |
| `alert_list` | Список активних алертів |
| `alert_delete` | Видалити алерт |

## Pine Script розробка

| Інструмент | Призначення | Порядок |
|-----------|-------------|---------|
| `pine_new` | Новий скрипт | 1 |
| `pine_open` | Відкрити збережений скрипт | 1 |
| `pine_set_source` | Вставити код | 2 |
| `pine_smart_compile` | Компілювати + перевірити помилки | 3 |
| `pine_get_errors` | Читати помилки компіляції | 4 |
| `pine_get_console` | Читати `log.info()` вивід | 4 |
| `pine_save` | Зберегти у TradingView cloud | 5 |
| `pine_get_source` | Читати код (**обережно: 200KB+**) | тільки при потребі |
| `pine_list_scripts` | Список збережених скриптів | |
| `pine_analyze` | Аналіз скрипту | |
| `pine_check` | Перевірка без компіляції | |
| `pine_compile` | Компіляція | |

## Replay режим

| Інструмент | Порядок | Призначення |
|-----------|---------|-------------|
| `replay_start` | 1 | `date: "2025-03-01"` |
| `replay_step` | 2 | Крок вперед на 1 бар |
| `replay_autoplay` | 2 | Авто-програш (`speed` в мс) |
| `replay_trade` | 3 | `action: "buy"/"sell"/"close"` |
| `replay_status` | будь-коли | Позиція, P&L, дата |
| `replay_stop` | кінець | Повернутись у реальний час |

## Batch операції

```javascript
batch_run({
  symbols: ["EURUSD", "GBPUSD", "USDJPY"],
  action: "screenshot"  // або "get_ohlcv"
})
```

## UI навігація

| Інструмент | Призначення |
|-----------|-------------|
| `ui_click` | Клік по елементу (`by: "aria-label"/"data-name"/"text"`) |
| `ui_find_element` | Знайти елемент на сторінці |
| `ui_evaluate` | Виконати JavaScript у контексті TV |
| `ui_keyboard` | Натиснути клавішу (`key: "Escape"`, `modifiers: ["ctrl"]`) |
| `ui_mouse_click` | Клік по координатам x, y |
| `ui_hover` | Наведення курсору |
| `ui_type_text` | Ввести текст |
| `ui_scroll` | Прокрутка |
| `ui_open_panel` | Відкрити панель (pine-editor, strategy-tester...) |
| `ui_fullscreen` | Повноекранний режим |
| `capture_screenshot` | Скріншот (`region: "full"/"chart"/"strategy_tester"`) |

## Layouts і вкладки

| Інструмент | Призначення |
|-----------|-------------|
| `layout_list` | Список layouts |
| `layout_switch` | Переключити layout |
| `tab_list` | Список вкладок |
| `tab_new` | Нова вкладка |
| `tab_switch` | Переключити вкладку |
| `tab_close` | Закрити вкладку |
| `pane_list` | Список панелей |
| `pane_focus` | Фокус на панель |
| `pane_set_layout` | Макет панелей |
| `pane_set_symbol` | Символ для панелі |

## Watchlist і дані

| Інструмент | Призначення |
|-----------|-------------|
| `watchlist_get` | Отримати watchlist |
| `watchlist_add` | Додати символ |
| `depth_get` | Стакан (Level 2) |
| `data_get_equity` | Дані equity |
| `data_get_trades` | Список трейдів |
| `data_get_strategy_results` | Результати стратегії |

## Morning Brief

```javascript
morning_brief() // огляд ринку на початок дня
```

## Корисні JS патерни через `ui_evaluate`

```javascript
// Отримати всі shapes
const cw = window.TradingViewApi._activeChartWidgetWV.value();
cw.getAllShapes() // → [{id, name}, ...]

// Видалити всі shapes
cw.getAllShapes().forEach(s => cw.removeEntity(s.id));
```

## Важливі обмеження

- `data_get_ohlcv` — max 500 барів.
- `data_get_pine_labels` — max 50 per study (змінити через `max_labels`).
- `pine_get_source` — може повернути 200 KB+, уникати.
- Pine drawings видимі тільки якщо індикатор **видимий** на графіку.
- Entity ID — session-specific, не кешувати між сесіями.

## Пов'язані

- Trading skills: `~/MyVault/20-Trading/skills/{dixie, kassandra, tda-screenshot, tv-position}/SKILL.md`
- Сесійні нотатки трейдингу: `~/MyVault/20-Trading/Journal/`, `~/MyVault/20-Trading/Analysis/`
- Глобальні правила: `~/MyVault/CLAUDE-RULES.md` (TDA Standard, Position Setup)
