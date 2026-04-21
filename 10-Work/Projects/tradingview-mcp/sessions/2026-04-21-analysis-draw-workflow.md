---
title: "TradingView MCP — SMC Analysis + Draw Trade Plan Workflow"
date: 2026-04-21
tags: [work, session, tradingview, mcp, pine-script, smc, workflow]
category: work
project: tradingview-mcp
status: completed
pinecone_indexed: false
---

## 🎯 Мета сесії
Автоматизувати повний цикл: SMC аналіз (H4→H1→15m) + малювання Trade Plan на TradingView через MCP без ручних дій.

## ✅ Виконано
- Реалізовано команду "намалюй" — Claude аналізує і малює автоматично
- Підтверджено workflow для додавання Pine Script на графік через `ui_evaluate` (JS)
- Знайдено кнопку "Обновить на графике" для оновлення існуючого скрипту
- Задокументовано баги з fullscreen та Pine Editor

---

## 🔄 Повний Workflow: Аналіз + Draw Trade Plan

### 1. Аналіз (H4 → H1 → 15m)
```
1. chart_set_symbol("EURUSD")
2. chart_set_timeframe("240")        → H4 bias
3. data_get_ohlcv(summary=true, count=50)
4. capture_screenshot(region="chart") → візуальна перевірка структури
5. chart_set_timeframe("60")         → H1 контекст, OB/FVG зони
6. data_get_ohlcv(summary=true, count=50)
7. capture_screenshot(region="chart")
8. chart_set_timeframe("15")         → 15m тригер
9. data_get_ohlcv(count=30)          → детальні бари
10. capture_screenshot(region="chart")
```

### 2. Визначення рівнів (SMC алгоритм)
```
H4: bullish/bearish BOS? HH/HL чи LH/LL?
H1: ключові OB, FVG, підтвердження BOS/ChoCH
15m: SSL/BSL sweep → BOS/ChoCH → pullback → entry zone
```

### 3. Розрахунок лоту
```
risk_pips = entry - sl (для LONG) × 10000
lot = $100 / (risk_pips × $10)
Мінімум: округлити вниз до 2 знаків
```

### 4. Draw Trade Plan — Pine Script
```
1. pine_new(type="indicator")
2. pine_set_source(source=PINE_TEMPLATE_З_РІВНЯМИ)
3. pine_smart_compile()
4. Якщо study_added: false → ui_evaluate(JS_ADD_TO_CHART)
5. Якщо кнопка = "Обновить на графике" → ui_mouse_click(x=2122, y=62)
6. chart_get_state() → перевірити studies[]
```

### JS для "Добавить на график"
```javascript
// Крок 4 — якщо перший раз додаємо скрипт
(function() {
  const buttons = Array.from(document.querySelectorAll('button'));
  const addBtn = buttons.find(b => b.textContent.includes('Добавить на график'));
  if (addBtn) { addBtn.click(); return 'clicked'; }
  return 'not found';
})()
```

### JS для збереження діалогу "Сохранить скрипт"
```javascript
(function() {
  const buttons = Array.from(document.querySelectorAll('button'));
  const saveBtn = buttons.find(b => b.textContent.trim() === 'Сохранить');
  if (saveBtn) { saveBtn.click(); return 'saved'; }
  return 'not found';
})()
```

---

## 🐛 Відомі баги та рішення

| Баг | Причина | Рішення |
|-----|---------|---------|
| "Добавить на график" не знаходиться через JS | Pine Editor ще не відкритий | `pine_new()` → потім `pine_set_source` → компіляція → JS click |
| Fullscreen режим ламає координати | `getBoundingClientRect()` повертає y=0 | `ui_fullscreen()` → повторна спроба |
| Діалог "Сохранить скрипт" блокує | При `pine_new` TV просить зберегти | JS клік "Сохранить" → потім компіляція |
| Pine Editor завантажується з spinner | Редактор відкривається в правій панелі (не знизу) | Почекати, потім `pine_smart_compile()` |
| "Обновить на графике" замість "Добавить" | Скрипт вже є на графіку (попередня версія) | Клік `ui_mouse_click(x=2122, y=62)` — оновлює існуючий |
| Pine Editor close button | Кнопка X в header Pine Editor | `ui_mouse_click(x=2517, y=16)` або JS через `buttons.find(b => b.title==='Закрыть')` |

---

## 📝 Pine Script Trade Plan Template (v6)

```pine
//@version=6
indicator("Trade Plan — SYMBOL DIRECTION", overlay=true, max_boxes_count=10, max_labels_count=20, max_lines_count=10)

entry = 0.00000  // ← підставити
sl    = 0.00000  // ← підставити
tp1   = 0.00000  // ← підставити
tp2   = 0.00000  // ← підставити
tp3   = 0.00000  // ← підставити
lots  = 0.00     // ← підставити

risk_pips = math.round((entry - sl)    * 10000, 1)
tp1_pips  = math.round((tp1   - entry) * 10000, 1)
tp2_pips  = math.round((tp2   - entry) * 10000, 1)
tp3_pips  = math.round((tp3   - entry) * 10000, 1)
risk_usd  = math.round(lots * risk_pips * 10, 0)
tp1_usd   = math.round(lots * tp1_pips  * 10, 0)
tp2_usd   = math.round(lots * tp2_pips  * 10, 0)
tp3_usd   = math.round(lots * tp3_pips  * 10, 0)
rr1       = math.round(tp1_pips / risk_pips, 1)
rr2       = math.round(tp2_pips / risk_pips, 1)
rr3       = math.round(tp3_pips / risk_pips, 1)

if barstate.islast
    t1 = bar_index - 3
    t2 = bar_index + 80
    box.new(t1, entry, t2, sl,    bgcolor=color.new(color.red,   82), border_color=color.new(color.red,   20), border_width=1)
    box.new(t1, tp1,   t2, entry, bgcolor=color.new(color.green, 85), border_color=color.new(color.green, 40), border_width=1)
    box.new(t1, tp2,   t2, tp1,   bgcolor=color.new(color.green, 75), border_color=color.new(color.green, 20), border_width=1)
    line.new(t1, tp3,  t2, tp3,   color=color.new(color.teal, 10), width=2, style=line.style_dashed)
    label.new(t2, sl,    text="⛔ SL  "    + str.tostring(sl)    + "\n−" + str.tostring(risk_pips) + " pips  |  −$" + str.tostring(risk_usd), style=label.style_label_left, color=color.new(color.red,    5), textcolor=color.white, size=size.normal)
    label.new(t2, entry, text="⚡ ВХІД  "  + str.tostring(entry) + "\n" + str.tostring(lots) + " lot  |  Ризик $" + str.tostring(risk_usd) + "  (" + str.tostring(risk_pips) + " pips)", style=label.style_label_left, color=color.new(color.orange, 5), textcolor=color.white, size=size.normal)
    label.new(t2, tp1,   text="✅ TP1  "   + str.tostring(tp1)   + "\n+" + str.tostring(tp1_pips) + " pips  |  +$" + str.tostring(tp1_usd) + "  RR 1:" + str.tostring(rr1), style=label.style_label_left, color=color.new(color.green,  5), textcolor=color.white, size=size.normal)
    label.new(t2, tp2,   text="🎯 TP2  "   + str.tostring(tp2)   + "\n+" + str.tostring(tp2_pips) + " pips  |  +$" + str.tostring(tp2_usd) + "  RR 1:" + str.tostring(rr2), style=label.style_label_left, color=color.new(#00aa00,     5), textcolor=color.white, size=size.normal)
    label.new(t2, tp3,   text="🚀 TP3  "   + str.tostring(tp3)   + "\n+" + str.tostring(tp3_pips) + " pips  |  +$" + str.tostring(tp3_usd) + "  RR 1:" + str.tostring(rr3), style=label.style_label_left, color=color.new(color.teal,  5), textcolor=color.white, size=size.normal)
```

**Важливо:**
- Версія **v6** (v5 deprecated у TradingView)
- Hardcode рівнів напряму (не `input.float`) — щоб одразу малювалось
- `pip_value = $10` для EURUSD/GBPUSD (стандартний lot = 100,000 units)

---

## 🔑 Важливі рішення (ADR)

| Рішення | Причина | Альтернатива |
|---------|---------|-------------|
| JS `ui_evaluate` для "Добавить на график" | `ui_mouse_click` координати нестабільні між сесіями | Фіксовані координати — ламаються при зміні layout |
| `pine_new` перед кожним новим сетапом | Скидає стан редактора, уникає "Обновить" замість "Добавить" | Відкривати існуючий через `pine_open` |
| Hardcode рівнів в Pine Script | Input fields потребують ручного заповнення після додавання | `indicator_set_inputs` — нестабільний для нових скриптів |
| Fullscreen вимкнути перед роботою з Pine Editor | Координати ламаються (y=0) | — |

---

## 📎 Сетапи дня (2026-04-21)

### EURUSD LONG
- SSL sweep: 1.17200 | BOS: 1.17638 | Entry: 1.17320 | SL: 1.17160 | TP1: 1.17638 | TP2: 1.17800 | TP3: 1.18200 | Lot: 0.62

### GBPUSD LONG
- SSL sweep: 1.34760 | BOS: 1.35258 | Entry: 1.34900 | SL: 1.34730 | TP1: 1.35258 | TP2: 1.35500 | TP3: 1.35800 | Lot: 0.59

**USD weakness bias** — обидва сетапи збіглися в один час (NY session open)

---

## 🔗 Пов'язані нотатки
- [[10-Work/Projects/tradingview-mcp/sessions/2026-04-21-pine-script-obsidian-setup]]
- [[10-Work/Projects/tradingview-mcp/sessions/2026-04-21-tradingview-mcp-tools-reference]]
- [[20-Trading/Journal/2026-04-21-trading-session]]
