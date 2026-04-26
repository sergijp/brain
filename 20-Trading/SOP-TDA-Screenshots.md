---
title: "SOP: Як робити скріни TradingView для TDA"
date: 2026-04-26
tags: [trading, sop, mcp, tradingview, screenshots, workflow]
category: trading
status: active
pinecone_indexed: false
---

# SOP — Скріншоти TradingView для Top-Down Analysis

## 🎯 Принцип

Кожен скрін має бути **читабельний**: бари заповнюють чарт по висоті/ширині, остання свічка ближче до центру (не на краю), Y-axis авто-масштабований під видимий діапазон.

## 🔄 Послідовність MCP-викликів (per timeframe)

```
1. mcp__tradingview__chart_set_timeframe(TF)
2. mcp__tradingview__ui_keyboard(key="r", modifiers=["alt"])     ← Alt+R = reset/auto-fit
3. mcp__tradingview__chart_set_visible_range(from, to)            ← вузький X-діапазон
4. mcp__tradingview__ui_evaluate(setRightOffset(N))               ← N барів буферу справа
5. mcp__tradingview__capture_screenshot(region="full")            ← обов'язково "full"
6. cp ~/tradingview-mcp-jackson/screenshots/[name].png \
       ~/MyVault/20-Trading/Analysis/YYYY-MM-DD/img/
```

### `region="full"` — обов'язково

`region="chart"` повертає чарт у малому квадранті екрану (TV рендериться в маленькому віджеті).
`region="full"` дає повне вікно — чарт заповнює простір нормально.

### Alt+R — обов'язково

Без `Alt+R` Y-axis залишається фіксованим з попереднього TF (особливо коли йдеш з W → 5m), бари сплющуються в смугу.

### `setRightOffset(N)` через ui_evaluate

`chart_set_visible_range(to=future)` MCP-tool **clamp-ить `to` до останнього бару**. Тому буфер справа тільки через JS API:

```js
(function(){
  const cw = window.TradingViewApi._activeChartWidgetWV.value();
  const ts = cw.chartModel().timeScale();
  ts.setRightOffset(15);   // 15 барів порожнього простору справа
  return ts.rightOffset();
})()
```

## 📐 Параметри per timeframe

| TF   | visible_range (X)         | rightOffset (N) | Логіка                          |
|------|---------------------------|-----------------|----------------------------------|
| W    | ~30 тижнів (18,144,000 s) | 15              | 9 місяців історії + 4 міс буфер  |
| D    | ~60 днів (5,184,000 s)    | 15              | 2 місяці + 2 тижні буфер         |
| H4   | ~60 барів (864,000 s)     | 20              | 10 днів + 3 дні буфер            |
| H1   | ~50 барів (180,000 s)     | 20              | 2 дні + ~1 день буфер            |
| 15m  | ~50 барів (45,000 s)      | 20              | 12 годин + ~5 годин буфер        |
| 5m   | ~50 барів (15,000 s)      | 20              | 4 години + ~1.5 год буфер        |

`from = last_bar_time - range_seconds`
`to = last_bar_time + 1` (clamped до останнього бару)

## 🖼 Іменування скрінів

```
[pair_lowercase]_[tf].png
```

Де `tf` = `w` / `d` / `h4` / `h1` / `m15` / `m5`.

Приклад: `eurusd_w.png`, `eurusd_d.png`, `eurusd_h4.png`, `eurusd_h1.png`, `eurusd_m15.png`, `eurusd_m5.png`.

## ✅ Чекліст перед скріном

- ☐ Правильний символ (`chart_get_state` для перевірки)
- ☐ Правильний TF (W/D/240/60/15/5)
- ☐ Alt+R натиснуто (Y auto-fit)
- ☐ visible_range встановлено (X bounded)
- ☐ rightOffset >= 15 (last bar не на краю)
- ☐ region="full" (не "chart")
- ☐ Файл скопійовано у `~/MyVault/20-Trading/Analysis/YYYY-MM-DD/img/`

## ❌ Відомі помилки

| Помилка | Як обійти |
|---------|-----------|
| `region="chart"` → чарт у лівому-верхньому квадранті | Завжди `region="full"` |
| Y-axis сплющений після W → 5m | Alt+R після кожної зміни TF |
| `to=future` clamp до last bar | `ui_evaluate setRightOffset(15+)` |
| `cw.activeChart()` не існує | Використовувати `cw.chartModel().timeScale()` |
| Fullscreen ламає координати кліків | Не вмикати fullscreen під час інших операцій |

## 🔗 Пов'язані

- [[20-Trading/Analysis/2026-04-26/EURUSD-analysis|EURUSD Top-Down 2026-04-26]]
- CLAUDE.md (project rules) — `~/AI/Projects/Trading/CLAUDE.md`
