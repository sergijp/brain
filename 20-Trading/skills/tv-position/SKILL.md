---
name: tv-position
description: Малює native Long/Short Position drawing у TradingView через MCP з точними рівнями entry/SL/TP (RiskReward box з сірою risk-зоною та зеленою reward-зоною). Розв'язує відомий баг TradingView API де public-поля `stopLevel`/`profitLevel` зберігають значення в моделі але візуально не оновлюють рендер — використовує internal `_source.properties().childs().entryPrice/stopPrice/targetPrice.setValue(...)`. Активується на /tv-position, /position, /long, /short, або фразах "постав лонг X сл Y тп Z", "намалюй short", "відкрий позицію", "draw position". Використовується скілом `dixie` для візуалізації trade plan на чарті.
---

# tv-position — Long/Short Position Drawing у TradingView

Інструмент для малювання native Long/Short Position drawing у TradingView Desktop через MCP. Створює повноцінний RiskReward box (сіра risk-зона + зелена reward-зона) з точними рівнями entry/SL/TP.

## Коли активувати

- `/tv-position`, `/position`, `/long`, `/short` (з аргументами)
- "постав лонг 1.17010 sl 1.16961 tp 1.17431"
- "намалюй short EURUSD entry 1.17208 stop 1.17285 target 1.16790"
- "відкрий long position на XAUUSD"
- "draw position long ..."
- Викликається з skill `dixie` для візуалізації узгодженого trade plan

## Аргументи

| Параметр | Тип | Default | Опис |
|----------|-----|---------|------|
| `direction` | `long` \| `short` | — | Обов'язково |
| `entry` | float | — | Ціна входу |
| `sl` | float | — | Stop loss (для LONG: < entry; для SHORT: > entry) |
| `tp` | float | — | Take profit (для LONG: > entry; для SHORT: < entry) |
| `pair` | string | поточний на чарті | TV symbol (опц., якщо потрібно змінити) |
| `time` | unix sec | last bar time | Anchor — за замовчуванням останній бар |
| `clear_existing` | bool | `false` | Видалити попередні position drawings перед новою |
| `account_size` | float | `10000` | Для розрахунку lot/risk у TV info block |
| `risk_pct` | float | `1` | % ризику від депозиту |

Парсинг: `"постав лонг 1.17010 сл 1.16961 тп 1.17431"` → `direction=long, entry=1.17010, sl=1.16961, tp=1.17431`.

## Валідація (перед створенням)

1. **Direction sanity:**
   - LONG: `sl < entry < tp` — інакше помилка "Перевір напрям, для LONG SL має бути нижче entry, TP вище"
   - SHORT: `tp < entry < sl` — інакше помилка "Перевір напрям, для SHORT SL вище entry, TP нижче"
2. **RR sanity:**
   - `rr = abs(tp-entry) / abs(entry-sl)`
   - Якщо `rr < 1` — попередити: "⚠️ RR < 1:1, ти впевнений?"
3. **Entry близько до ринку:** якщо `|entry - last_close| / last_close > 0.05` (5% off) — попередити.
4. **Symbol:** якщо `pair` передано і відрізняється від поточного — `chart_set_symbol` спочатку.

## Workflow (точна послідовність)

### Крок 1 — Підготовка

```javascript
// JS виклик через mcp__tradingview__ui_evaluate
const cw = window.TradingViewApi._activeChartWidgetWV.value();
```

(Опціонально, якщо `clear_existing=true`):

```javascript
for (const s of cw.getAllShapes()) {
  if (/position/i.test(s.name)) {
    try { cw.removeEntity(s.id); } catch(e){}
  }
}
```

### Крок 2 — Anchor time

Якщо `time` не передано — взяти останній bar:

```
mcp__tradingview__data_get_ohlcv(symbol=<pair>, timeframe="<current TF>", limit=1, summary=true)
→ last bar time (unix seconds)
```

TV сам snap'не до найближчого бару.

### Крок 3 — Створити shape (single-point + правильний `shape` name)

```javascript
return new Promise((resolve) => {
  const shape = direction === 'long' ? 'long_position' : 'short_position';
  cw.createMultipointShape(
    [{ time: <anchor_time>, price: <entry> }],
    { shape: shape }
  ).then(id => {
    const ent = cw.getShapeById(String(id));
    // ⚡ КЛЮЧОВЕ: використати INTERNAL childs, не public setProperties
    const childs = ent._source.properties().childs();
    childs.entryPrice.setValue(<entry>);
    childs.stopPrice.setValue(<sl>);
    childs.targetPrice.setValue(<tp>);
    // optional: account/risk для TV info block
    childs.accountSize && childs.accountSize.setValue(<account_size>);
    childs.risk && childs.risk.setValue(<risk_pct>);
    function v(c){ return c && c.value ? c.value() : c; }
    resolve({
      id: String(id),
      entry: v(childs.entryPrice),
      stop:  v(childs.stopPrice),
      target: v(childs.targetPrice)
    });
  }).catch(e => resolve({ err: String(e) }));
});
```

### Крок 4 — Верифікація

Прочитати назад через ті ж childs, переконатись що значення збереглись точно як передано (з округленням до 5 знаків для FX, до 2 для індексів).

### Крок 5 — (Опціонально) Auto-fit Y щоб обидві зони видно

Якщо TP/SL виходять за межі поточного viewport (типово для LONG де TP далеко вище, або SHORT де TP далеко нижче):

```javascript
// service horizontal lines на TP та SL (невидимі) — щоб Alt+R fit включив їх
cw.createMultipointShape([{time:<t>,price:<tp>}],{shape:'horizontal_line',overrides:{showLabel:false,linecolor:'rgba(0,0,0,0)',linewidth:0}});
cw.createMultipointShape([{time:<t>,price:<sl>}],{shape:'horizontal_line',overrides:{showLabel:false,linecolor:'rgba(0,0,0,0)',linewidth:0}});
```

Потім: `mcp__tradingview__ui_keyboard(key="r", modifiers=["alt"])` + `setRightOffset(15-20)`.

⚠️ Не забути видалити service lines після Alt+R якщо не треба (вони невидимі, але впливають на Alt+R наступних разів).

### Крок 6 — Скрін (опціонально)

`mcp__tradingview__capture_screenshot(region="full", filename="position_<direction>_<pair>_<date>")` — для документування у Obsidian.

## ⚡ Ключове відкриття (root-cause баг)

**TradingView API має ДВА рівні properties у Long/Short Position drawing:**

| Public API (`getProperties`/`setProperties`/overrides) | Internal childs (`_source.properties().childs()`) |
|---|---|
| `stopLevel` | `stopPrice` |
| `profitLevel` | `targetPrice` |
| (немає прямого ентрі) | `entryPrice` |

**Public-поля `stopLevel`/`profitLevel`** — приймаються через `overrides:{}` у `createMultipointShape`, зберігаються в model (повертаються `getProperties()`), **АЛЕ ВІЗУАЛЬНО НЕ ОНОВЛЮЮТЬ РЕНДЕР**. Без override-у default = `244` (internal offset, не price).

**Internal childs `entryPrice`/`stopPrice`/`targetPrice`** — це **справжні візуальні рівні**. Їх треба set'ити через `.setValue(...)` ПІСЛЯ створення shape. Тільки тоді TV перерендерить boxes на правильних висотах.

Без цього кроку рендер показує дефолтні рівні ±1 pip від entry — позиція виглядає як крихітна смужка замість повноцінного box.

## Жорсткі правила

1. **Тільки через `_source.properties().childs()`.** Не використовувати public `setProperties({stopLevel, profitLevel})` — воно мовчки зберігає, але не рендерить.
2. **Single-point shape.** `short_position`/`long_position` приймають ОДНУ точку (entry). Передача 2-3 точок ігнорується (TV snap'ить до однієї).
3. **Ширина box по X — автоматична.** TV сам розтягує на ~5-7 барів вправо. Контролю немає (ні через 2nd point, ні через override).
4. **Time auto-snap до бара.** TV перетворює переданий `time` на найближчий bar timestamp. Це нормально.
5. **Direction-specific colors:**
   - LONG: зелений зверху (TP), сірий знизу (SL)
   - SHORT: сірий зверху (SL), зелений знизу (TP)
6. **Видаляти попередні позиції** тільки якщо явно `clear_existing=true`. Default — накопичувати (для multi-leg setupiв).
7. **Перевірити `chart_get_state`** перед створенням — переконатись що ти на правильному symbol+TF.
8. **Не використовувати `setPoints([p1, p2])` для розтягування ширини** — мовчки приймається, точки залишаються однаковими.

## Чекліст перед малюванням

- [ ] `chart_get_state` → правильний symbol
- [ ] Direction validation (LONG: sl<entry<tp; SHORT: tp<entry<sl)
- [ ] RR ≥ 1 (інакше попередити)
- [ ] Anchor time = last bar (через `data_get_ohlcv` з `summary=true, limit=1`)
- [ ] Створено через `createMultipointShape` з `shape: long_position|short_position` (single point)
- [ ] **Виставлено через `_source.properties().childs().{entryPrice,stopPrice,targetPrice}.setValue(...)`**
- [ ] Верифіковано — read-back значень
- [ ] (опц.) Auto-fit Y якщо TP/SL поза viewport

## Вивід користувачу

```
✅ Позиція намальована: <LONG/SHORT> на <PAIR>
   Entry:  <X>
   SL:     <Y>  (<N> pts ризику)
   TP:     <Z>  (<M> pts профіту)
   RR:     1:<X.X>
   Lot:    <L>  (ризик $<R> від депозиту $<D>)
```

Якщо викликано з Dixie — він додає коментар у своєму стилі.

## Відомі помилки і fix-и

| Симптом | Причина | Fix |
|---------|---------|-----|
| Box виглядає як тонка лінія / точка | Не set'ив через internal childs | `childs.entryPrice/stopPrice/targetPrice.setValue(...)` |
| `stopLevel: 244` після створення | Default offset, не ціна | Завжди set internal childs |
| Передав 2 точки, друга ігнорується | shape single-point | Це нормально, передавай 1 точку |
| `setProperties({stopLevel: X})` зберігає, але візуально не міняє | TV bug у public API | Використовувати internal childs |
| `risk_reward_short` створив `flag` | Невідомий shape name → fallback | Тільки `long_position` / `short_position` |
| `cw.activeChart()` не існує | Невірний JS path | `cw.chartModel().mainSeries()` etc |
| Anchor time зсунувся | TV snap до bar | Це нормально |

## Інтеграція з іншими skills

**Викликається з `dixie`:** після debate з Kassandra і узгодження плану — Dixie викликає `tv-position` з фінальними entry/SL/TP. Параметри передаються готовими (без додаткової валідації).

**Не викликає інших skills.** Це leaf-tool.

## Канонічне джерело

- Single source: `~/MyVault/20-Trading/skills/tv-position/SKILL.md`
- Симлінки: `~/.claude/skills/tv-position/SKILL.md`, `~/.gemini/skills/tv-position/SKILL.md`
- Project rules: `~/AI/Projects/Trading/CLAUDE.md`

## История експериментів (для контексту)

Skill розроблено через ітеративний reverse-engineering TradingView API. Основні milestones:
1. ❌ `createMultipointShape` з overrides `{stopLevel, profitLevel}` — значення в model є, рендер default
2. ❌ Передача 2 точок для розтягування ширини — TV ігнорує
3. ❌ `setProperties({stopLevel, profitLevel})` після створення — те саме
4. ❌ `risk_reward_short` як shape name — створює `flag`
5. ✅ **Через `_source.properties().childs().entryPrice/stopPrice/targetPrice.setValue(...)`** — працює
