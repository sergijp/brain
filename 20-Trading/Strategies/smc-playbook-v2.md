---
title: "SMC + PA Combo v2 — Розширений Playbook"
date: 2026-04-21
tags: [trading, strategy, smc, price-action, playbook, v2]
category: trading
status: active
pinecone_indexed: false
---

# 📊 SMC + Price Action Combo — v2 (Extended)

**Version:** 2.0
**Replaces:** [[20-Trading/Strategies/smc-price-action-combo]] (v1, legacy)
**Session reference:** [[10-Work/Projects/trading/sessions/2026-04-21-strategy-v2-planning]]

---

## 🎯 Філософія

Top-down multi-TF SMC з **7 моделями входу**, **3 scoring профілями**, формалізованим trailing SL і tilt-protection risk-sizing. Кожен трейд проходить 6-point pre-trade gate + psychology check. Edge валідується через чотириетапний бектест (manual → Pine → paper → live).

---

## ⏱️ Таймфрейми

| Рівень | TF | Призначення |
|--------|-----|-------------|
| HTF Bias | W / D / H4 | Загальний напрямок, ключові зони |
| Entry Context | H1 | POI (OB/FVG/breaker), BOS/ChoCH |
| Entry Trigger | 15m / 5m | Sweep → BOS/ChoCH → inner FVG → вхід |

---

## 🏦 Watchlist

| Клас | Інструменти |
|------|-------------|
| Forex Majors | EURUSD, GBPUSD, USDJPY, USDCAD, USDCHF |
| Metals | XAUUSD, XAGUSD |
| Indices | GER40, US100, US500 |

**Inter-market:** DXY (для USD-пар), US10Y yields (для XAU).

---

## 💰 Торговий профіль

- **Рахунок:** $10,000
- **Базовий ризик:** 1% = $100/трейд
- **Daily DD limit:** 3% ($300) → стоп торгівлі до завтра
- **RR мінімум:** 1:2, ціль 1:3+
- **Формула лоту (EURUSD):** `Lot = $100 / (risk_pips × $10)`

---

## 🧠 Ключові концепції

### Order Block (OB)
Остання протилежна свічка перед impulse-рухом. Вхід при ретесті з LTF-confirm.

### Fair Value Gap (FVG / Imbalance)
3-бар gap: High[2] vs Low[0] (bullish) або Low[2] vs High[0] (bearish).

### Breaker Block
OB, пробитий ціною → тепер працює у протилежному напрямку. Ретест breaker у напрямку пробиття = valid entry.

### BOS / ChoCH
- **BOS** — break of structure (продовження тренду)
- **ChoCH** — change of character (перший сигнал розвороту)

### Liquidity (SSL / BSL)
- **SSL** — стопи під низами (PDL, Asian Low, equal lows)
- **BSL** — стопи над верхами (PDH, Asian High, equal highs)
- **Sweep** — викид за рівень → повернення = сигнал

### POI (Points of Interest) — розширений набір
- H4/H1 OB, FVG, Breaker
- Weekly Open, Monthly Open
- Previous Week H/L, Quarterly H/L
- Session H/L (London, NY)

---

## 📈 Bias Definition

### ✅ Bullish
- H4/H1: HH/HL структура
- Ціна вище ключового H4 OB/FVG
- BOS up на H1 підтверджено
- SSL sweep виконано
- DXY bearish (для EUR/GBP/AUD) / real yields down (для XAU)

### 🔴 Bearish
- H4/H1: LH/LL структура
- Ціна нижче ключового H4 OB/FVG
- BOS down на H1 підтверджено
- BSL sweep виконано
- DXY bullish / real yields up

### ⚪ Neutral (no trade)
- Consolidation без BOS
- Між рівнями без напрямку
- Поза торговими сесіями

---

## 🎲 7 Моделей входу

### Модель 1: Classic BOS Retest (v1 carry-over)

**Setup:** H4 bias → H1 POI → 15m sweep → 15m BOS → pullback до BOS zone → вхід.
**SL:** за swing що створив BOS + 2-5 pips буфер.
**TP:** TP1 1:1 → BE, TP2 наступна ліквідність, TP3 HTF ціль.

---

### Модель 2: Delayed Entry (alert-driven)

**Setup:**
1. H4/H1 аналіз → ідентифіковано POI (OB/FVG/breaker на H1).
2. Alert на рівень POI (через TV → `mcp__tradingview__alert_create`).
3. Повернення до графіка **тільки при спрацюванні** (години/дні пізніше).
4. Валідація:
   - HTF bias не інвалідовано (нема протилежного H4 BOS)
   - POI не violated (mitigation, не пробиття)
   - LTF trigger (sweep + BOS/ChoCH) з'явився

**Time stop:** якщо ціна не дійшла до POI протягом N сесій — alert знято, setup expired.

---

### Модель 3: Inner FVG after LTF BOS

**Setup:** після LTF BOS (5m або 15m) у напрямку HTF bias → знайти **FVG всередині impulse leg BOS**.
**Entry:** limit-ордер на proximal edge FVG (top для long, bottom для short).
**SL:** за 50% equilibrium FVG АБО за swing що створив BOS — що далі.
**Переваги:** tighter SL → кращий RR порівняно з ретестом broad OB/BOS zone.

---

### Модель 4: AMD / Power of Three (ICT)

**Структура:**
- **Accumulation** — Asian session (00:00-07:00 UTC), range, низька волатильність.
- **Manipulation (Judas Swing)** — в KZ (London 07:00-09:00 UTC або NY 12:00-14:00 UTC) ціна знімає протилежну сторону Asian range.
- **Distribution** — реальний рух у напрямку HTF bias після sweep.

**Entry conditions:**
- HTF bias визначено (H4/D)
- Asian range розмічено (high/low)
- У KZ-вікні — sweep проти HTF bias (Judas)
- Після sweep — LTF ChoCH у напрямку bias
- Вхід: OB/FVG що створив ChoCH
- SL: за sweep extreme

**Сесії:** обидві (London KZ + NY KZ).

---

### Модель 5: Breaker Block Entry

**Setup:** OB не відпрацював (ціна пробила його) → тепер breaker.
**Entry:** limit на ретест breaker у напрямку пробиття.
**SL:** за дальню сторону breaker + буфер.
**Часто:** кращий RR ніж original OB, бо структура вже зламана.

---

### Модель 6: Silver Bullet (sub-model)

**Вікно:** 10:00-11:00 NY time (15:00-16:00 UTC стандартно).
**Setup:** FVG fill у напрямку HTF bias у цьому вікні.
**Entry:** на першому касанні FVG.
**SL:** за FVG extreme.
**TP:** наступна ліквідність (часто денний high/low).

---

### Модель 7: London Reversal (sub-model)

**Вікно:** ~10:00 UTC (після London open expansion).
**Setup:** Judas sweep проти HTF bias у перші 2-3 години London → reversal до bias.
**Entry:** LTF ChoCH після sweep.
**SL:** за sweep extreme.

---

## 📊 Confluence Scoring — 3 Профілі

### Базові ваги (спільні для всіх профілів)

| Фактор | Бали |
|--------|------|
| HTF bias align | +2 |
| POI на HTF рівні (H4 OB/FVG/Weekly Open) | +2 |
| Killzone time (London/NY KZ) | +1 |
| Sweep виконано (SSL/BSL) | +2 |
| Inner FVG present | +1 |
| RR ≥ 1:3 до ліквідності | +2 |
| **Макс** | **10** |

### Профілі порогів

| Профіль | A (full 1%) | B (0.5%) | C (skip/paper) | Коли використовувати |
|---------|-------------|----------|-----------------|----------------------|
| **Conservative** | ≥9 | 7-8 | <7 | Drawdown recovery, нова модель, unstable market |
| **Standard** | ≥8 | 5-7 | <5 | Default — норма торгівлі |
| **Aggressive** | ≥6 | 4-5 | <4 | Trending market, high-conviction week, підтверджений edge |

**Записувати у journal:** поле `scoring_profile: conservative|standard|aggressive`.
**A/B тестування:** тиждень на профіль, порівняти expectancy (D4).

---

## 🛡️ Risk & Money Management

### A1. Реальний R з витратами
Кожен трейд у journal має поле `cost_R` ≈ -0.1R (spread + commission). Expectancy рахується **після** витрат.

### A2. Trailing SL (формалізовано)

| Стан | Дія |
|------|-----|
| TP1 hit | SL → entry (BE) |
| TP2 hit | SL → TP1 (lock profit) |
| Між TP2-TP3 | Trail за 15m swing low (long) / high (short) |

### A3. Dynamic Risk Sizing (tilt protection)

| Тригер | Дія |
|--------|-----|
| 3 losses підряд | Risk/trade → 0.5% |
| 2 wins підряд (після cut) | Повернення → 1% |
| Daily DD 3% hit | Стоп торгівлі до завтра |

### A4. Kelly-lite Compounding
Кожні +5% equity growth → перерахунок $risk на новий баланс.
Приклад: $10,000 → $10,500 → новий risk = $105/трейд.

### A5. Correlation Risk
Див. [[20-Trading/Strategies/correlation-table]]. Правило: другий скорельований трейд = 0.5% замість 1%. Max USD-напрямок cumulative risk ≤ 2%.

---

## 🎯 Entry Precision Rules

### B1. DXY / Inter-market Confluence
Обов'язковий окремий screenshot перед входом:
- **EUR/GBP/AUD long** → DXY bearish structure
- **EUR/GBP/AUD short** → DXY bullish structure
- **XAU long** → DXY bearish + yields down
- **XAU short** → DXY bullish + yields up

### B2. News Filter (hard rule)
**±30 хв** від high-impact events: NFP, CPI, FOMC, ECB, BoE, SNB, unemployment claims.
Автоматизувати через TV economic calendar alert.
**No exceptions** — пропускаємо setup якщо навіть ідеальний.

### B3. HTF Key Levels (weekly ritual)
На початку тижня розмічати на графіку:
- Weekly Open / Monthly Open
- Previous Week H/L
- Quarterly H/L

### B4. Daily Profile Classification
До NY open класифікувати день:
- **Expansion** — trending, великі TP досяжні
- **Consolidation** — range, TP1 only, реверс після TP1
- **Retracement** — контр-тренд пуллбек, обережні входи

### B5. Liquidity-to-Liquidity TP Framework
TP ставляться **тільки** до наступних pool ліквідності:
- Equal highs/lows
- Old H/L (PDH/PDL, PWH/PWL)
- Session H/L
**Не довільні** "round numbers" чи "приблизно".

---

## 🚨 Invalidation Rules (до входу)

Setup скасовується якщо:
- Після BOS ціна закривається назад за BOS level на тому ж TF
- LTF формує протилежний BOS до входу
- Time stop: ціна не дійшла до POI протягом N годин/сесій → alert знято
- Виходить high-impact news у найближчі 30 хв → pause

---

## ✅ Pre-Trade Checklist (6-Point Gate)

**Обов'язковий перед будь-яким market/limit entry:**

1. ☐ HTF bias визначений?
2. ☐ POI валідний (не violated)?
3. ☐ Sweep виконано?
4. ☐ LTF BOS/ChoCH підтверджено?
5. ☐ RR ≥ 1:2 до ліквідності?
6. ☐ Psychology OK (AM I CALM?)

**Якщо хоч 1 ❌ → skip трейд.**

### AM I CALM? — Psychology Gate
Мій стан зараз:
- Tilted / Angry / Manic / Impatient / **Calm**?

Тільки **Calm** → OK. Всі інші → пауза мінімум 30 хв або вихід на сьогодні.

---

## 🔁 Ритуали

### Щоденний: Daily Bias Log
Після NY close (17:00-18:00 UTC / 20:00-21:00 Kyiv):
- Файл: `20-Trading/Journal/YYYY-MM-DD-bias.md`
- Для кожної пари watchlist: bias (bullish/bearish/neutral) + ключові рівні на завтра
- **Не змінювати інтрадей** без H4 BOS

### Тижневий: Weekly Review
П'ятниця 18:00 Kyiv після NY close:
- Equity curve огляд
- Rule adherence % (скільки трейдів з повним дотриманням)
- Top 3 помилки тижня
- 1 фокус на наступний тиждень
- Файл: `20-Trading/Journal/YYYY-Www-weekly-review.md`

---

## 📊 Measurement & Feedback

### D1. Dataview Dashboard
`20-Trading/Dashboards/live-stats.md` — live queries:
- Win rate by pair / model / session / grade / day-of-week
- Avg R, expectancy, max DD
- Adherence distribution

### D2. Model Retirement Rule
Модель з <40% WR на 30+ трейдів → призупинити, переглянути правила. Повернути тільки після 10+ paper-трейдів з >45% WR.

### D3. Adherence Tracking
Кожен трейд: `rule_adherence: full|partial|broken`.
- Ціль: ≥90% full
- <90% → процесна проблема, не edge

### D4. A/B Testing Scoring Profiles
- Тиждень 1: Conservative
- Тиждень 2: Standard
- Тиждень 3: Aggressive
- Тиждень 4: повторити найкращий
Метрика: expectancy в R.

---

## 🏷️ Journal Trade Schema

```yaml
---
date: YYYY-MM-DD
pair: EURUSD
model: classic|delayed|inner_fvg|amd|breaker|silver_bullet|london_reversal
setup_grade: A|B|C
scoring_profile: conservative|standard|aggressive
scoring_points: 8
session: asian|london_kz|london|ny_kz|ny
direction: long|short
entry: 1.17320
sl: 1.17160
tp1: 1.17638
tp2: 1.17800
tp3: 1.18492
lot: 0.63
risk_pct: 1.0
cost_R: -0.1
result_R: +2.1
rule_adherence: full
psychology_gate: calm
dxy_confluence: bearish
news_clear: true
notes: "..."
---
```

---

## 🎯 Algorithm — Покрокова інструкція

```
Крок 1: Weekly prep (понеділок ранок)
  → Розмітити Weekly/Monthly Open, PWH/PWL, Quarterly H/L
  → Daily profile classification для кожної пари

Крок 2: Daily prep (ранок перед London)
  → Перевірити news calendar → позначити ±30 хв no-trade вікна
  → Asian range mark-up (high/low)
  → H4/D bias для watchlist

Крок 3: Entry Context (H1)
  → POI (OB/FVG/breaker)
  → Ліквідність мапа (SSL/BSL)

Крок 4: Entry Trigger (15m/5m) — за обраною моделлю
  → Classic / Delayed / Inner FVG / AMD / Breaker / Silver Bullet / London Reversal
  → Sweep → BOS/ChoCH → inner FVG (якщо Model 3)

Крок 5: Pre-Trade Gate
  → 6-point checklist
  → AM I CALM?
  → DXY/yields confluence screenshot
  → News ±30 хв clear?

Крок 6: Confluence Scoring
  → Підрахунок балів
  → Порівняння з профілем (Conservative/Standard/Aggressive)
  → Risk size (1% / 0.5% / skip)

Крок 7: Execution
  → Entry, SL, TP1-3, lot
  → Записати у journal (повна schema)
  → Draw Trade Plan через Pine Script (див. tradingview_draw_workflow.md)

Крок 8: Management
  → Trailing SL: TP1→BE, TP2→TP1, between → 15m swing
  → Якщо invalidation rules триггеряться — close manually

Крок 9: Post-trade
  → Оновити journal з result_R, rule_adherence
  → Скріншот до/після
```

---

## 🔗 Пов'язані нотатки

- [[20-Trading/Strategies/smc-price-action-combo]] — v1 (legacy)
- [[20-Trading/Strategies/correlation-table]] — таблиця корів
- [[20-Trading/Backtest/README]] — бектест-процес
- [[20-Trading/Checklists/pre-trade-checklist]]
- [[20-Trading/Checklists/weekly-review-template]]
- [[20-Trading/Dashboards/live-stats]]
- [[20-Trading/Resources/trading-rules]]
- [[20-Trading/Resources/tradingview-mcp-workflow]]
- [[10-Work/Projects/trading/sessions/2026-04-21-strategy-v2-planning]] — origin session
- [[10-Work/Projects/trading/rollout-plan-strategy-v2]] — implementation plan
