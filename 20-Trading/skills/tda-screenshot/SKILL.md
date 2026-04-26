---
name: tda-screenshot
description: Робить читабельні скріншоти TradingView для Top-Down Analysis через MCP. Активується на /tda-screenshot або фразах "зроби скрін", "скріни для TDA", "знімок графіка для аналізу". Параметри (опціональні через args або з контексту чату): pair (символ TradingView, default = поточний на чарті), tfs (через кому, default "w,d,h4,h1,m15,m5"), date (YYYY-MM-DD, default = today).
---

# TDA Screenshot — TradingView через MCP

Створює серію читабельних скріншотів TradingView для Top-Down Analysis. Кожен таймфрейм отримує власний скрін з правильним масштабуванням (Y auto-fit, обмежений X-діапазон, last bar відступлений від правого краю).

## Коли активувати

- Користувач пише `/tda-screenshot` (з аргументами або без)
- Користувач каже: "зроби скріни", "скріни для аналізу", "знімки графіків", "скріни TDA", "TDA screens"
- Користувач просить top-down analysis і потрібні скрінші для нотатки в Obsidian

## Вимоги до середовища

- TradingView Desktop запущений з CDP (`~/tradingview-mcp-jackson/scripts/launch_tv_debug_mac.sh`)
- MCP server `tradingview` доступний (інструменти `mcp__tradingview__*`)
- Vault: `~/MyVault/20-Trading/Analysis/<date>/img/`
- Скрінші TradingView пишуться в `~/tradingview-mcp-jackson/screenshots/`

Перевірка перед запуском: `mcp__tradingview__tv_health_check`. Якщо fail → `mcp__tradingview__tv_launch` і чекати 3-5 сек.

## Аргументи

| Параметр | Default | Опис |
|----------|---------|------|
| `pair` | поточний символ на чарті (через `chart_get_state`) | Символ TV: `EURUSD`, `XAUUSD`, `GER40`, `US100`, ... |
| `tfs` | `w,d,h4,h1,m15,m5` | Список TF через кому |
| `date` | сьогодні (`YYYY-MM-DD`) | Папка призначення |

Парсити з тексту користувача: `"/tda-screenshot EURUSD h1,m15"` → `pair=EURUSD, tfs=h1,m15`.

## Mapping TF → API

| Аргумент | TradingView TF (для `chart_set_timeframe`) | Filename suffix |
|----------|-----|---|
| `w`   | `W`   | `_w`   |
| `d`   | `D`   | `_d`   |
| `h4`  | `240` | `_h4`  |
| `h1`  | `60`  | `_h1`  |
| `m15` | `15`  | `_m15` |
| `m5`  | `5`   | `_m5`  |

## Параметри per timeframe

| TF   | range_seconds (X) | rightOffset (N) |
|------|-------------------|-----------------|
| W    | 18,144,000 (~30 тижнів) | 15 |
| D    | 5,184,000 (~60 днів)    | 15 |
| H4   | 864,000 (~60 H4 барів)  | 20 |
| H1   | 180,000 (~50 H1 барів)  | 20 |
| 15m  | 45,000  (~50 m15 барів) | 20 |
| 5m   | 15,000  (~50 m5 барів)  | 20 |

`from = last_bar_time - range_seconds`
`to   = last_bar_time + 1` (TV clamp до last bar)

`last_bar_time` отримати через `mcp__tradingview__data_get_ohlcv(symbol, timeframe="5", limit=1, summary=true)` → останній timestamp (Unix seconds).

## Workflow (per TF)

Виконати **строго в цій послідовності**, окремо для кожного TF з `tfs`:

```
1. mcp__tradingview__chart_set_symbol(symbol=pair)            # тільки на першому TF
2. mcp__tradingview__chart_set_timeframe(timeframe=<TV_TF>)
3. mcp__tradingview__ui_keyboard(key="r", modifiers=["alt"])  # Alt+R = Y auto-fit
4. mcp__tradingview__chart_set_visible_range(from=<from>, to=<to>)
5. mcp__tradingview__ui_evaluate(expression=<JS_RIGHT_OFFSET>)
6. mcp__tradingview__capture_screenshot(region="full", filename="<pair_lower>_<suffix>")
7. cp ~/tradingview-mcp-jackson/screenshots/<pair_lower>_<suffix>.png \
      ~/MyVault/20-Trading/Analysis/<date>/img/
```

### JS для setRightOffset

Передавати в `ui_evaluate` як `expression`:

```javascript
(function(){
  const cw = window.TradingViewApi._activeChartWidgetWV.value();
  const ts = cw.chartModel().timeScale();
  ts.setRightOffset(N);
  return ts.rightOffset();
})()
```

де `N` — значення з таблиці вище (15 або 20).

### Створення папки призначення

Перед першим `cp`:
```bash
mkdir -p ~/MyVault/20-Trading/Analysis/<date>/img
```

## Жорсткі правила (не порушувати)

1. **`region="full"` завжди.** `region="chart"` рендерить чарт у вузькому квадранті — нечитабельно.
2. **Alt+R після кожної зміни TF.** Інакше Y-axis залишається з попереднього TF (особливо помітно при W → 5m).
3. **`setRightOffset` тільки через `ui_evaluate`.** `chart_set_visible_range(to=future)` clamp-ить майбутнє до останнього бару — буфер справа НЕ створюється цим викликом.
4. **Послідовність обов'язкова:** `set_timeframe` → `Alt+R` → `set_visible_range` → `setRightOffset` → `capture`. Зміна порядку ламає картинку.
5. **Не вмикати fullscreen** під час інших MCP-операцій — координати кліків ламаються.
6. **JS API path:** `cw.chartModel().timeScale()` — НЕ `cw.activeChart()` (така функція не існує).

## Чекліст (виконати mentally перед кожним скріном)

- [ ] Правильний символ на чарті (`chart_get_state` повертає `symbol == pair`)
- [ ] Правильний TF
- [ ] Alt+R натиснуто
- [ ] visible_range встановлено з правильним `range_seconds`
- [ ] `rightOffset() >= 15` (return value від `ui_evaluate`)
- [ ] `region="full"` у `capture_screenshot`
- [ ] Файл скопійовано у vault

## Вивід користувачу

Після завершення:

```
✨ Скріни TDA готові

📁 ~/MyVault/20-Trading/Analysis/<date>/img/
   ├── <pair_lower>_w.png
   ├── <pair_lower>_d.png
   ├── <pair_lower>_h4.png
   ├── <pair_lower>_h1.png
   ├── <pair_lower>_m15.png
   └── <pair_lower>_m5.png

🔗 Markdown посилання для нотатки:
   ![[img/<pair_lower>_w.png]]
   ![[img/<pair_lower>_d.png]]
   ...
```

## Відомі помилки та fix-и

| Симптом | Причина | Fix |
|---------|---------|-----|
| Чарт у малому квадранті екрану | `region="chart"` | Завжди `region="full"` |
| Бари сплющені у вузьку смугу | Y-axis з попереднього TF | Alt+R після зміни TF |
| Last bar на правому краю | `setRightOffset` не викликаний | Крок 5 обов'язковий |
| `cw.activeChart is not a function` | Невірний JS path | `cw.chartModel().timeScale()` |
| `to` не приймає майбутнє | TV clamp policy | Це нормально, буфер через `setRightOffset` |
| Координати кліків зламані | Ввімкнено fullscreen | Вийти з fullscreen |
| MCP не відповідає | TV без CDP / закритий | `tv_launch` + чекати 3-5 сек |

## Канонічне джерело

Цей файл — single source of truth, симлінкнутий у:
- `~/.claude/skills/tda-screenshot/SKILL.md`
- `~/.gemini/skills/tda-screenshot/SKILL.md`

Оригінал: `~/MyVault/20-Trading/skills/tda-screenshot/SKILL.md`

Розширений human-readable SOP: `~/MyVault/20-Trading/SOP-TDA-Screenshots.md`
