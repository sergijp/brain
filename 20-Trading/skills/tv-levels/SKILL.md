---
name: tv-levels
description: Малює ключові торгові рівні у TradingView через MCP — Daily Open, NY Open, PDH/PDL, PWH/PWL, PMH/PML. Промені (horizontal_ray) прив'язані до свічок де реально був хай/лоу. Мітки справа з ціною. При кожному виклику видаляє попередні рівні (не чіпає позиції та індикатори). Активується на /tv-levels, /levels, /key-levels або фразах "намалюй рівні", "постав рівні", "draw levels".
---

# tv-levels — Ключові торгові рівні у TradingView

Малює 8 рівнів через `horizontal_ray` (промінь від anchor-свічки вправо). Запускається через MCP TradingView.

## Коли активувати

- `/tv-levels`, `/levels`, `/key-levels`
- "намалюй рівні", "постав рівні", "постав ключові рівні"
- "draw levels", "key levels на чарті"
- Автоматично з Dixie перед аналізом

## Рівні та стилі

| Рівень | Колір | LW | Стиль | Label |
|--------|-------|----|-------|-------|
| D Open | `#2962FF` синій | 2 | суцільний | `D Open  <price>` |
| NY Open 7am Kyiv | `#FF1744` червоний | 2 | суцільний | `NY Open  <price>` |
| PDH | `#2E7D32` темно-зелений | 1 | переривчастий | `PDH  <price>` |
| PDL | `#2E7D32` темно-зелений | 1 | переривчастий | `PDL  <price>` |
| PWH | `#FF6D00` помаранчевий | 1 | переривчастий | `PWH  <price>` |
| PWL | `#FF6D00` помаранчевий | 1 | переривчастий | `PWL  <price>` |
| PMH | `#AA00FF` фіолетовий | 1 | переривчастий | `PMH  <price>` |
| PML | `#AA00FF` фіолетовий | 1 | переривчастий | `PML  <price>` |

`linestyle`: 0 = суцільний, 2 = переривчастий  
`horzLabelsAlign: "right"` — мітки завжди справа  
`vertLabelsAlign`: highs → `"top"`, lows → `"bottom"`

## Визначення дат

- **D Open** — остання закрита D свічка (або поточна якщо є)
- **NY Open** — H1 бар о 07:00 UTC поточного/останнього торгового дня  
  (= 7am Kyiv за підтвердженням user; для EURUSD OANDA = 7:00 UTC)
- **PDH / PDL** — попередній торговий день (для Monday → Friday)
- **PWH / PWL** — поточний тижень Mon–Fri (або попередній якщо weekend)
- **PMH / PML** — попередній місяць (усі D бари)

## Workflow (точна послідовність)

### Крок 0 — Зберегти поточний TF

```javascript
const cw = window.TradingViewApi._activeChartWidgetWV.value();
// запам'ятати resolution для повернення після збору даних
```

Через `chart_get_state` зберегти поточний `resolution`.

### Крок 1 — Отримати H1 дані (для D Open, NY Open, PDH, PDL, PWH, PWL)

```
mcp__tradingview__chart_set_timeframe(timeframe="60")
mcp__tradingview__data_get_ohlcv(count=200, summary=false)
```

200 H1 барів = ~8 торгових днів, покриває повний тиждень і попередній день.

З отриманих барів знайти:

**D Open anchor:**
- Перший H1 бар поточного/останнього торгового дня (00:00 UTC або початок сесії)
- `price` = `open` цього бару

**NY Open anchor:**
- H1 бар з часом 07:00 UTC поточного/останнього торгового дня
- `price` = `open` цього бару
- timestamp = `day_start_unix + 7*3600`

**PDH anchor:**
- Перебрати всі H1 бари попереднього торгового дня
- Знайти бар з `max(high)` → його `time` = anchor, `high` = price

**PDL anchor:**
- Знайти бар з `min(low)` → його `time` = anchor, `low` = price

**PWH anchor:**
- Перебрати всі H1 бари поточного тижня (Mon–Fri)
- Знайти бар з `max(high)` → його `time` = anchor

**PWL anchor:**
- Знайти бар з `min(low)` → його `time` = anchor

### Крок 2 — Отримати D дані (для PMH, PML)

```
mcp__tradingview__chart_set_timeframe(timeframe="D")
mcp__tradingview__data_get_ohlcv(count=60, summary=false)
```

60 D барів = ~3 місяці. Відфільтрувати бари попереднього місяця:

**PMH anchor:**
- Знайти D бар попереднього місяця з `max(high)` → `time` = anchor, `high` = price

**PML anchor:**
- Знайти D бар попереднього місяця з `min(low)` → `time` = anchor, `low` = price

### Крок 3 — Повернутись на початковий TF

```
mcp__tradingview__chart_set_timeframe(timeframe=<original_resolution>)
```

### Крок 4 — Cleanup (видалити попередні рівні)

```javascript
(function(){
  const cw = window.TradingViewApi._activeChartWidgetWV.value();
  let deleted = 0;
  for (const s of cw.getAllShapes()) {
    if (/horizontal_ray|horizontal_line/i.test(s.name)) {
      try { cw.removeEntity(s.id); deleted++; } catch(e){}
    }
  }
  return { deleted };
})()
```

⚠️ Фільтр тільки `horizontal_ray|horizontal_line` — не чіпає `long_position`, `short_position`, `trend_line`, studies.

### Крок 5 — Намалювати всі 8 рівнів

Викликати `mcp__tradingview__draw_shape` для кожного рівня. Усі 8 можна паралельно:

```
draw_shape(
  shape="horizontal_ray",
  point={ time: <anchor_unix>, price: <level_price> },
  overrides='<json>'
)
```

#### D Open
```json
{"linecolor":"#2962FF","linewidth":2,"linestyle":0,"showLabel":true,
 "text":"D Open  <price>","textcolor":"#2962FF",
 "horzLabelsAlign":"right","vertLabelsAlign":"top","fontsize":11,"bold":true}
```

#### NY Open
```json
{"linecolor":"#FF1744","linewidth":2,"linestyle":0,"showLabel":true,
 "text":"NY Open  <price>","textcolor":"#FF1744",
 "horzLabelsAlign":"right","vertLabelsAlign":"bottom","fontsize":11,"bold":true}
```

#### PDH
```json
{"linecolor":"#2E7D32","linewidth":1,"linestyle":2,"showLabel":true,
 "text":"PDH  <price>","textcolor":"#2E7D32",
 "horzLabelsAlign":"right","vertLabelsAlign":"top","fontsize":11,"bold":false}
```

#### PDL
```json
{"linecolor":"#2E7D32","linewidth":1,"linestyle":2,"showLabel":true,
 "text":"PDL  <price>","textcolor":"#2E7D32",
 "horzLabelsAlign":"right","vertLabelsAlign":"bottom","fontsize":11,"bold":false}
```

#### PWH
```json
{"linecolor":"#FF6D00","linewidth":1,"linestyle":2,"showLabel":true,
 "text":"PWH  <price>","textcolor":"#FF6D00",
 "horzLabelsAlign":"right","vertLabelsAlign":"top","fontsize":11,"bold":false}
```

#### PWL
```json
{"linecolor":"#FF6D00","linewidth":1,"linestyle":2,"showLabel":true,
 "text":"PWL  <price>","textcolor":"#FF6D00",
 "horzLabelsAlign":"right","vertLabelsAlign":"bottom","fontsize":11,"bold":false}
```

#### PMH
```json
{"linecolor":"#AA00FF","linewidth":1,"linestyle":2,"showLabel":true,
 "text":"PMH  <price>","textcolor":"#AA00FF",
 "horzLabelsAlign":"right","vertLabelsAlign":"top","fontsize":11,"bold":false}
```

#### PML
```json
{"linecolor":"#AA00FF","linewidth":1,"linestyle":2,"showLabel":true,
 "text":"PML  <price>","textcolor":"#AA00FF",
 "horzLabelsAlign":"right","vertLabelsAlign":"bottom","fontsize":11,"bold":false}
```

## Жорсткі правила

1. **Тільки `horizontal_ray`** — не `horizontal_line`. Промінь стартує від anchor-свічки де реально був хай/лоу.
2. **Anchor = фактична свічка** де ціна occurred (H1 бар з max high / min low), не початок дня/тижня.
3. **Мітки справа** (`horzLabelsAlign: "right"`) — завжди, без варіантів.
4. **D Open і NY Open — суцільні** (`linestyle: 0`). Решта — переривчасті (`linestyle: 2`).
5. **Cleanup тільки horizontal_ray/horizontal_line** — не чіпати `long_position`, `short_position`, indicators.
6. **Повернутись на початковий TF** після збору H1/D даних.
7. **PDH/PDL = попередній торговий день**, навіть якщо сьогодні понеділок (тоді PD = пятниця).
8. **PWH/PWL = поточний тиждень** (Mon–Fri). У weekend — тиждень що щойно завершився.
9. **PMH/PML = попередній календарний місяць** (всі D бари за той місяць).
10. **Ціна в мітці**: `"PDH  1.17236"` (два пробіли між назвою і ціною).

## Вивід користувачу

```
✅ Рівні намальовано: EURUSD | 26 Apr 2026

   D Open   1.16836  ──────────────────
   NY Open  1.16780  ──────────────────

   PDH      1.17236  - - - - - - - - -
   PDL      1.16729  - - - - - - - - -

   PWH      1.17911  - - - - - - - - -
   PWL      1.16692  - - - - - - - - -

   PMH      1.17958  - - - - - - - - -
   PML      1.14110  - - - - - - - - -
```

## Відомі нюанси

| Симптом | Причина | Fix |
|---------|---------|-----|
| Лінія зникла після зміни TF | TV не перемальовує при TF switch | Перемалювати заново |
| PWL і PDL збігаються (однакова ціна) | Реально той самий рівень | Залишити обидві (різні кольори) |
| `horzLabelsAlign: "right"` не працює | Старіша версія TV Desktop | Спробувати `"center"` як fallback |
| PMH/PML — якір на початку дня, а не на свічці | Немає H1 даних за той місяць | Використати D bar time як anchor (прийнятно) |
| Бари з `summary=true` не мають часу кожної свічки | `summary=true` повертає агреговані дані | Завжди `summary=false` для пошуку anchor |

## Канонічне джерело

- Single source: `~/MyVault/20-Trading/skills/tv-levels/SKILL.md`
- Симлінки: `~/.claude/skills/tv-levels/SKILL.md`, `~/.gemini/skills/tv-levels/SKILL.md`
- Project rules: `~/AI/Projects/Trading/CLAUDE.md`

## Підтверджені значення (EURUSD, 26 Apr 2026)

Використовувались для розробки і тестування скілу:

| Рівень | Ціна | Anchor (unix) | Anchor (UTC) |
|--------|------|---------------|--------------|
| D Open | 1.16836 | 1776978000 | Fri Apr 25, 00:00 UTC |
| NY Open | 1.16780 | 1777003200 | Fri Apr 25, 07:00 UTC |
| PDH | 1.17236 | 1777060800 | Fri Apr 25, 23:00 UTC |
| PDL | 1.16729 | 1776999600 | Fri Apr 25, 06:00 UTC |
| PWH | 1.17911 | 1776726000 | Tue Apr 22, 02:00 UTC |
| PWL | 1.16692 | 1776963600 | Thu Apr 24, 20:00 UTC |
| PMH | 1.17958 | 1772402400 | Mon Mar 3, D bar |
| PML | 1.14110 | 1773349200 | Fri Mar 14, D bar |
