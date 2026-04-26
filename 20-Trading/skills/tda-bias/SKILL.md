---
name: tda-bias
description: Виконує повний Top-Down Analysis (TDA) для торгової пари — визначає HTF bias, ключові рівні (OB/FVG/sweeps/BOS-CHoCH) на W/D/H4/H1/15m/5m, будує торговий план (Entry/SL/TP1-3/Lot за SMC+PA Combo), робить скрінші через skill `tda-screenshot` і зберігає аналіз у Obsidian vault. Активується на /tda-bias, /bias, або фразах "зроби TDA", "топ-даун аналіз", "визнач bias", "проаналізуй пару", "trade plan для X". Параметри: pair (символ TV, обов'язковий або з контексту чарту), date (YYYY-MM-DD, default = today), deposit (default $10000), risk_pct (default 1%).
---

# TDA Bias — SMC + Price Action Top-Down Analysis

Повний top-down аналіз торгової пари за стратегією SMC + Price Action Combo. Виконує читання OHLCV з TradingView через MCP, визначає bias на кожному TF, ідентифікує ключові SMC-структури (OB, FVG, BOS, CHoCH, liquidity sweeps), будує торговий план з розрахованим лотом і записує markdown-аналіз у Obsidian vault.

## Коли активувати

- `/tda-bias`, `/bias`, `/tda` (з аргументом-парою або без)
- "зроби TDA по EURUSD"
- "топ-даун аналіз GER40"
- "визнач bias для XAUUSD"
- "проаналізуй [pair]"
- "побудуй trade plan для [pair]"
- "зроби аналіз пари"

## Залежності

- **Skill `tda-screenshot`** — для генерації візуалів (запускається автоматично як етап 1)
- **MCP `tradingview`** — інструменти `mcp__tradingview__*` (TradingView Desktop з CDP)
- **Obsidian vault** — `~/MyVault/20-Trading/Analysis/<date>/<PAIR>-analysis.md`

Перевірити перед стартом: `mcp__tradingview__tv_health_check`. Якщо fail → `tv_launch` + 3-5s.

## Аргументи

| Параметр | Default | Опис |
|----------|---------|------|
| `pair` | поточний символ (`chart_get_state`) | Символ TV: `EURUSD`, `XAUUSD`, `GER40`, `US100`, ... |
| `date` | сьогодні (`YYYY-MM-DD`) | Папка призначення в vault |
| `deposit` | `10000` | Розмір рахунку в USD |
| `risk_pct` | `1` | Ризик на угоду у % від депозиту |

Парсити: `/tda-bias EURUSD` → `pair=EURUSD`. `/tda-bias XAUUSD risk=0.5` → `risk_pct=0.5`.

## Workflow (виконати строго по порядку)

### Етап 0 — Підготовка

1. **Синхронізація годинника (обов'язково першим кроком).** Отримати реальний UTC/локальний час з системи, не покладатись на внутрішній час моделі чи `currentDate` з контексту:
   ```bash
   date -u "+%Y-%m-%d %H:%M:%S UTC"   # Universal — для сесійних вікон (London/NY KZ)
   date    "+%Y-%m-%d %H:%M:%S %Z"    # Локальний (Київ) — для правила "не входити раніше 09:00"
   ```
   - Використати UTC для перевірки активної сесії (London KZ 07:00-09:00 UTC, NY KZ 12:00-14:00 UTC) з урахуванням DST (взимку UTC+0, влітку UTC+1 для London; для NY: UTC-5 / UTC-4).
   - Використати Київський час для правила входу ≥ 09:00 Kyiv.
   - Якщо `<date>` не передано аргументом — взяти його з `date "+%Y-%m-%d"` (а не з контексту моделі).
   - Якщо last bar з `data_get_ohlcv` старший за поточний UTC час більше ніж на ~1 годину (для FX в торговий час) — попередити: "⚠️ TradingView дані застарілі".
2. `mcp__tradingview__tv_health_check`. Якщо TV не відповідає → `tv_launch`.
3. `mcp__tradingview__chart_set_symbol(symbol=pair)`.
4. `mcp__tradingview__draw_clear()` — прибрати малюнки попереднього дня (не чіпає відкритих позицій).
5. `mkdir -p ~/MyVault/20-Trading/Analysis/<date>/img`.

### Етап 1 — Скрінші (делегувати в `tda-screenshot`)

Викликати skill `tda-screenshot` з `pair=<pair>`, `tfs=w,d,h4,h1,m15,m5`, `date=<date>`. Не дублювати логіку — повністю довіряти тому workflow. Дочекатись завершення (всі 6 PNG у `~/MyVault/20-Trading/Analysis/<date>/img/`).

Якщо `tda-screenshot` недоступний — fallback: виконати його кроки інлайн (див. SKILL.md скіла).

### Етап 2 — Збір даних per TF

Для кожного TF (`W`, `D`, `240`, `60`, `15`, `5`) виконати:

```
mcp__tradingview__chart_set_timeframe(timeframe=<TF>)
mcp__tradingview__data_get_ohlcv(symbol=pair, timeframe=<TF>, limit=30, summary=true)
mcp__tradingview__quote_get(symbol=pair)         # один раз — поточна ціна
```

`summary=true` обов'язково — інакше повернеться 30+ барів raw даних і роздує контекст. Summary дає: open/close/high/low діапазон, % change, останні 5 барів, HH/LL за період.

Зібрати в робочий dataset:
- 15W range (high/low за 15 тижнів) + W % change + останні 5W closes
- 20D range + D % change + останні 5D closes
- H4 range (30 барів) + останні 5 H4 closes
- H1 range + останні 5 H1 closes
- M15/M5 — поточна структура для пошуку тригера

### Етап 3 — Аналіз bias per TF

**Weekly (HTF):**
- Bullish: серія HH/HL, ціна над key support, BOS вгору
- Bearish: LH/LL, BOS вниз
- Distribution/Exhaustion: довгі upper wicks на топі, sideways під ATH
- Записати: `HTF Bullish` / `HTF Bearish` / `HTF Bullish-Exhausted` / `Bearish-Corrective` / etc.

**Daily:**
- Position у W range (top/mid/bottom)
- Останні 5D — accumulation чи distribution?
- Sweeps PDH/PDL за останній тиждень
- Статус відносно key OB/FVG зон з W

**H4:**
- Структура: BOS UP / BOS DOWN / consolidation
- H4 swing high/low → ключові рівні для SL/TP
- Recovery з лоу чи failure?
- Формується HL чи LH?

**H1 (entry context):**
- Tight accumulation чи expansion?
- H1 OB / FVG для ретесту
- SMT (Smart Money Technique): порівняти з корелятом
  - Indices: US100 ↔ US500 ↔ GER40
  - Metals: XAUUSD ↔ XAGUSD
  - FX: EURUSD ↔ GBPUSD ↔ DXY
  - Розбіжність → потенційна reversal зона

**M15/M5 (тригери):**
- Сценарій A (консервативний): ретест X-зони + CHoCH → entry
- Сценарій B (агресивний): sweep liquidity X → reversal
- Sweep + BOS — мінімум для входу

### Етап 4 — Торговий план

За зібраним bias скласти план:

| Поле | Як визначити |
|------|--------------|
| Bias | З Етапу 3 W+D+H4 (узгоджена цільова сторона) |
| Entry | H1 OB / FVG / зона ретесту |
| SL | За H4 swing low/high (LONG: нижче H4 low; SHORT: вище H4 high) |
| TP1 | Найближчий H1/H4 рівень — RR ~1.0 |
| TP2 | H4 high/low — RR 2-3 |
| TP3 | D ATH/ATL або Fib extension — RR 4+ |
| Lot | `lot = (deposit × risk_pct/100) / (sl_pips × pip_value)` |

**Pip values (брокер OANDA, перевірити для свого):**
- FX major (EURUSD, GBPUSD, ...): `1 pt = $10` на 1 lot
- USDJPY: `1 pt = ~$6.7` на 1 lot (інверсно, перевірити)
- XAUUSD: `1 pt = $1` на 0.01 lot → `$100` на 1 lot
- XAGUSD: `1 pt = $0.50` на 0.01 lot → `$50` на 1 lot
- US100 / NAS100: `1 pt = $0.20` на 1 contract
- US500 / SPX500: `1 pt = $0.50` на 1 contract
- GER40 / DAX: `1 pt = $1` на 1 contract

⚠️ **Завжди додавати "перевірити брокер"** у markdown — pip values залежать від бірж/брокера.

### Етап 5 — Запис у Obsidian

**Шлях:** `~/MyVault/20-Trading/Analysis/<date>/<PAIR>-analysis.md`

**Шаблон markdown:**

```markdown
---
title: <PAIR> Top-Down Analysis
date: <YYYY-MM-DD>
tags: [<PAIR>, TDA, <bias-tag>, <category>]
category: Analysis
project: Trading
status: analysis-complete
pinecone_indexed: false
---

# <PAIR>: Top-Down Analysis — <DD.MM.YYYY>

## 🏛 Weekly (Тижневий графік)
W: <±X.XX%>. Останні 5W: `... → ... → ... → ... → ...` — <структурний коментар>. <HTF bias verdict>.

![[img/<pair_lower>_w.png]]

## 📅 Daily (Денний графік)
20D <±X.XX%>, range `<low>–<high>`. Останні 5D: `... → ... → ... → ... → ...` — <структурний коментар>.

![[img/<pair_lower>_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `<low>–<high>`, <±X.XX%>. Останні 5×4H: `...` — <структурний коментар>.

![[img/<pair_lower>_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 <±X.XX%>. Останні 5H: `...` — <структурний коментар>.
**SMT:** з <корелят> — <вердикт SMT>.

![[img/<pair_lower>_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
Сценарії:
1. **Консервативно (LONG/SHORT):** ретест `<зона>` + CHoCH → <напрям> до `<ціль>`.
2. **Агресивно:** sweep `<зона>` → <напрям> з `<зона>`.

![[img/<pair_lower>_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

- **Bias:** <Bullish/Bearish> (<long/short>, <momentum/corrective>) <📈/📉>
- **Entry Zone:** `<low> – <high>`
- **Stop Loss:** `<price>` (нижче/вище <H4 swing>) — **<X> pts**
- **TP1:** `<price>` — RR <X.X>
- **TP2:** `<price>` — RR <X.X>
- **TP3:** `<price>` — RR <X.X>
- **Lot Size:** `$<risk> / (<sl> × $<pip_value>) ≈ <lot> lot` (<інструмент>: <pip note> — перевірити брокер)

![[img/<pair_lower>_m5.png]]

---
**Коментар:** <контекст ринку, кореляції, news risks (FOMC/NFP/ECB/earnings), сесії (London KZ / NY KZ)>.
```

### Етап 6 — Вивід користувачу

```
✨ TDA готово: <PAIR>

📊 Bias: <Bullish/Bearish/Neutral> (<momentum/corrective/exhausted>)
📁 ~/MyVault/20-Trading/Analysis/<date>/<PAIR>-analysis.md

🎯 Trade Plan:
   Entry:  <X> – <Y>
   SL:     <price> (<X> pts)
   TP1:    <price> — RR <X.X>
   TP2:    <price> — RR <X.X>
   TP3:    <price> — RR <X.X>
   Lot:    <X.XX> (ризик $<X>)

⚠️ News risks: <список>
🕐 Best session: <London KZ / NY KZ / etc>
```

## Жорсткі правила (не порушувати)

1. **Синхронізація годинника — перший крок завжди.** Виконати `date -u` + `date` ДО будь-якого MCP-виклику. Не використовувати `currentDate` з контексту моделі і не вгадувати поточну дату/час — тільки системний час. Це визначає `<date>`, активну сесію (London/NY KZ з урахуванням DST) і свіжість даних TV.
2. **Завжди `summary=true` у `data_get_ohlcv`.** Без нього контекст роздувається raw барами.
3. **Не входити раніше 09:00 Київського часу** (07:00 UTC взимку, 06:00 UTC влітку) — записати у коментарі.
3. **Risk = max 1% депозиту на угоду.** Якщо `risk_pct > 2` — попередити користувача.
4. **RR мінімум 1:2 на TP2.** Якщо план не дає 1:2 → позначити "⚠️ Setup не торгувальний" у markdown.
5. **Тег `<bias-tag>` у frontmatter** — один з: `bullish-strong`, `bullish-corrective`, `bullish-exhausted`, `bearish-strong`, `bearish-corrective`, `neutral`, `range`.
6. **Категорія `<category>`** — один з: `forex`, `indices`, `metals`, `crypto`, `commodities`.
7. **SMT обов'язково** — підібрати корелят з watchlist:
   - EURUSD ↔ GBPUSD / DXY
   - GBPUSD ↔ EURUSD
   - USDJPY ↔ DXY
   - XAUUSD ↔ XAGUSD / DXY
   - XAGUSD ↔ XAUUSD
   - GER40 ↔ US500 / EURUSD
   - US100 ↔ US500
   - US500 ↔ US100
8. **Пробіли у числах** для читабельності тільки якщо > 4 розрядів (`27 345`, не `27,345`).
9. **Якщо чарт без свіжих даних** (last bar > 1 година тому для FX в торговий час) — попередити: "⚠️ Дані застарілі, оновити TradingView".

## Чекліст перед записом markdown

- [ ] Папка `<date>/img/` існує і містить 6 PNG
- [ ] Bias на W/D/H4 узгоджений (або явно зазначено diverge)
- [ ] Entry / SL / TP1-3 у правильному порядку (LONG: SL < Entry < TP1 < TP2 < TP3)
- [ ] RR TP2 ≥ 1:2
- [ ] Lot розрахований з правильним pip value
- [ ] SMT з корелятом зазначений
- [ ] Frontmatter має `pinecone_indexed: false`
- [ ] Усі 6 `![[img/...]]` посилань вставлені

## Опціонально — Pine Script на чарт

Якщо користувач каже "намалюй план на чарті" або "додай Pine":
1. Підставити Entry/SL/TP1/TP2/TP3/Lot у Pine шаблон з `~/AI/Projects/Trading/CLAUDE.md`
2. `pine_set_source` → `pine_smart_compile`
3. Якщо `study_added: false` → `ui_mouse_click(x=2400, y=79)`
4. `chart_get_state` → перевірити що "Trade Plan" у `studies[]`

## Канонічне джерело

Single source of truth:
- `~/MyVault/20-Trading/skills/tda-bias/SKILL.md`

Симлінки:
- `~/.claude/skills/tda-bias/SKILL.md`
- `~/.gemini/skills/tda-bias/SKILL.md`

Залежний skill: `tda-screenshot` (`~/MyVault/20-Trading/skills/tda-screenshot/SKILL.md`).
Стратегія і pip values: `~/AI/Projects/Trading/CLAUDE.md`.
