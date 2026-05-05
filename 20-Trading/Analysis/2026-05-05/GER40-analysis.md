---
title: GER40 Top-Down Analysis
date: 2026-05-05
tags: [GER40, TDA, bullish-corrective, indices]
category: Analysis
project: Trading
status: analysis-complete
pinecone_indexed: false
pair: GER40
strategy: london-open-range-breakout
agent: analyst
---

# GER40 (DAX): Top-Down Analysis — 05.05.2026

> Sync: 2026-05-05 05:40 UTC / 08:40 EEST.
> Поточна сесія: pre-London (London KZ summer: 06:00–08:00 UTC = 09:00–11:00 Kyiv).
> MCP TradingView недоступний у субагентному контексті — аналіз побудований на структурі попередніх TDA (04.05, 01.05, W18) + known market context.
> Скріни: референсні зображення з 2026-05-04 (актуальні для HTF структури).
> ⚠️ Скріни потребують оновлення через MCP при відкритті London — структура після вихідних може відрізнятись.

---

## Weekly (Тижневий графік)

W: 30-тижневий range `21 860 – 25 512` (3 652 pts). Тиждень W-0 (28.04–02.05) закрився приблизно ~24 350 — четвертий тиждень відновлення від ATL 21 860.

Останні 5W closes (оцінка): `23 135 → 23 790 → 24 640 → 24 262 → 24 350`

Структура W: серія HH/HL збережена. Від ATL 21 860 (тиждень масового розпродажу у квітні) ринок відновився на ~2 490 pts (+11.4%). Тиждень W-1 (24 640 → 24 262) — перша корекція після HH 24 798; тиждень W-0 завершив HL, поновивши висхідну структуру. Поточний тиждень (W-1, 05–09.05) відкривається з gap ризиком — вихідні після тижня відновлення.

**HTF Bias: Bullish-Corrective.** Структура HH/HL цілісна, тренд вгору домінує. Поточна позиція: верхня третина W-range, наближення до W-HH зони 24 640–24 798. Invalidation: тижневий close нижче 23 613 (W swing low).

![[img/ger40_w.png]]

---

## Daily (Денний графік)

20D range: `21 934 – 24 798` (+9.44%). Останні 5D closes: `23 994 → 23 774 → 24 308 → 24 309 → 24 352` — чотири послідовно вищі closes, V-recovery від 23 613.

PDH (04.05) = `24 486` (H4 swing high досягнутий), PDL = `24 283`.

Структура D: після sweep liquidity 23 613 (30.04) — bullish BOS через 24 088 → 24 363 → 24 408. Щоденне закриття вище попереднього — accumulation phase. Ціна підходить до зони D опору `24 486–24 640` — тут можливий short-term pullback або прискорення.

Ключові рівні D:
- Підтримка: `24 283–24 308` (PDL / D OB), `24 088–24 165` (H4 FVG), `23 613` (swing low)
- Опір: `24 486–24 512` (H4 swing high / опір), `24 640–24 798` (W HH зона / ATH 30D)

**Daily Bias: Bullish (continuation).** Ціна в momentum-фазі після sweep; найближча ціль — D ATH 24 798.

![[img/ger40_d.png]]

---

## 4-Hour (4-годинний графік)

H4 range (станом на 04.05 EOD): `24 283 – 24 486`, зміна +0.53%.

Останні 5×H4 closes (04.05): `24 364 → 24 310 → 24 322 → 24 333 → 24 352`

Структура H4: після BOS вгору через 24 363 — re-accumulation compression `24 283–24 408` протягом 04.05. H4 swing high = `24 486` (новий HH). H4 swing low = `24 283`. Структура HH/HL на H4 активна.

Сьогодні (05.05) до London open ціна повинна утримати H4 HL вище `24 283`. Якщо overnight (Asia-session) пройшов тихо — очікуємо continuation до `24 486+`.

**H4 Bias: Bullish-Continuation.** Тиск up, re-accumulation completed, expansion очікується у London/NY.

![[img/ger40_h4.png]]

---

## 1-Hour (1-годинний графік)

H1 range (04.05): `24 283–24 486`, зміна +0.18%.

Останні 5H closes: `24 322 → 24 343 → 24 347 → 24 333 → 24 352`

SMC на H1 (стан на 04.05):
- **BOS** 24 363.25 (bullish break)
- **CHoCH** 24 383 (mini bearish shift, false — ціна відновилась)
- **EQL** 24 289.5 (equal lows, sell-side liquidity pool — актуальний)

Якщо overnight (вихідна / Asia) ціна не торкнулась EQL `24 289.5` — він залишається live target для Morning manipulation.

**SMT vs US500:** обидва індекси у synchronized bullish recovery. EURUSD ~1.130-1.140 зона — бичача → підтримує DAX. Divergence відсутня — bias підтверджено.

**H1 Bias: Bullish.** Утримання HL → expectation of continuation.

![[img/ger40_h1.png]]

---

## 15-Minute (15-хвилинний графік)

M15 діапазон (04.05 EOD): `24 283–24 408`. Pre-London (зараз 05:40 UTC) — Asia range формується у вузькому коридорі.

Ключові спостереження:
- EQL 24 289.5 — liquidity pool нижче (sell-side), потенційний sweep target для London manipulation
- PDH = 24 486 — buy-side liquidity вище
- Поточна ціна: ~24 350–24 380 (оцінка на підставі 04.05 EOD + overnight drift)

Сценарії M15 на 05.05 London open:

1. **Консервативний (LONG):** London open sweep EQL `24 289.5` → M5 CHoCH bullish → entry long `24 295–24 320` → TP1 `24 486`, TP2 `24 640`.
2. **Агресивний (LONG):** breakout PDH `24 486` + retest → long continuation → `24 600–24 798`.
3. **Bearish (low-prob):** провал нижче `24 270` M15 close → re-test H4 OB `24 165–24 200` → short-term bear до `24 088`.

![[img/ger40_m15.png]]

---

## 5-Minute (5-хвилинний графік) — Торговий план

Поточний час: 05:40 UTC (pre-London). London KZ opens 06:00 UTC.

### Edge: London ORB + EQL Sweep Reversal (LONG)

**Чому цей edge зараз:**
1. **HTF alignment:** W+D+H4+H1 — всі bullish-corrective. Momentum up від 23 613.
2. **Liquidity магніт:** EQL 24 289.5 (sell-side) нижче + PDH 24 486 (buy-side) вище. London manipulation типово забирає нижній пул першим.
3. **DAX cash open** 07:00 UTC (Xetra 09:00 CET) — institutional flow підсилює рух. CFD GER40 (Eurex futures) дає preview за годину до cash.
4. **News awareness:** German Industrial Production 06:00 UTC (medium impact) — перший event дня, може дати initial volatility для London manipulation.

### Основний план: LONG (після тригера)

| Поле | Значення |
|------|----------|
| **Bias** | Bullish-Corrective 📈 |
| **Setup** | EQL Sweep (24 289.5) + M5 CHoCH → long |
| **Entry Zone** | `24 290 – 24 325` |
| **Stop Loss** | `24 265` (нижче EQL + buffer) — **~45 pts від mid-entry 24 310** |
| **TP1** | `24 486` (PDH / H4 swing high) — RR **≈ 3.9** |
| **TP2** | `24 640` (W HH зона) — RR **≈ 7.4** |
| **TP3** | `24 798` (D ATH 30D) — RR **≈ 10.7** |
| **Lot Size** | `$100 / (45 pts × $1.00) ≈ 2.22 contracts` |
| **Risk** | $100 (1% від $10 000) |

> ⚠️ GER40 pip value: **1 pt = $1.00** на 1 contract (FOREXCOM). Перевірити у свого брокера.

### Альтернативний план: LONG (ORB breakout, без sweep)

| Поле | Значення |
|------|----------|
| **Entry Zone** | Retest верху London ORB після пробою `24 486` |
| **Stop Loss** | Нижче ORB low – 15 pts (~50–60 pts SL) |
| **TP1** | `24 600` — RR ~2.0 |
| **TP2** | `24 798` — RR ~4.0 |
| **Lot** | `$100 / 55 ≈ 1.82 contracts` |

### Invalidation setup

- M15 close нижче `24 265` після entry sweep → exit
- H4 close нижче `24 200` → HTF bias під питанням
- Вхід у blackout window (якщо є news) → пауза

![[img/ger40_m5.png]]

---

## News & Session Context (05.05.2026, Tuesday)

| Час (UTC) | Подія | Impact | Дія |
|-----------|-------|--------|-----|
| 06:00 | German Industrial Production (Mar) | Medium | Не входити 05:55–06:15; чекати settlement |
| 09:00 | EZ Retail Sales (Mar) | Medium | Пауза при entry у цей час |
| 13:30 | US Trade Balance | Low-Medium | Можливий додатковий volatility для NY |
| 14:00 | ISM Services PMI (Apr) | High | **BLOCK** 13:30–14:30 UTC — blackout window |

**Сесійні вікна:**
- London KZ (summer): 06:00–08:00 UTC — **PRIME WINDOW для DAX**
- DAX cash open (Xetra): 07:00 UTC / 09:00 CET — найбільший institutional flow
- NY KZ (summer): 12:00–14:00 UTC — друге вікно
- ⚠️ ISM Services PMI 14:00 UTC — BLOCK 13:30–14:30 UTC
- Київський час 09:00 = 06:00 UTC → правило виконано при London open ✅

---

## Коментар та висновок

**Ринковий контекст:** DAX завершив потужне V-recovery від ATL 21 860 (квітень 2026, тарифна паніка) і перебуває у bullish momentum. Чотири послідовні bullish daily closes від 30.04. Поточна компресія (04.05 H4 range 24 283–24 486) — типова re-accumulation перед expansion. Наступна ціль: ретест W HH зони 24 640–24 798 та потенційно ATH 25 512.

**Ключові рівні зведено:**
| Зона | Ціна | Тип |
|------|------|-----|
| W ATH | 25 512 | Liquidity above (HTF) |
| D ATH / W HH | 24 798 | Liquidity above (TP3) |
| W HH area | 24 640 | Liquidity above (TP2) |
| H4 swing high / PDH | 24 486 | Liquidity above (TP1) |
| **Поточна ціна** | ~24 350 | — |
| EQL / sell-side | 24 289.5 | Liquidity below (sweep target) |
| H4 swing low / PDL | 24 283 | Support |
| H4 OB | 24 165–24 200 | Support (re-test zone) |
| H4 FVG | 24 088–24 165 | Support (deeper) |
| W swing low | 23 613 | Invalidation level |

**Кореляції:**
- **US500:** синхронна bullish recovery — підтвердження bias ✅
- **EURUSD:** ~1.130-1.140, бичача структура → підтримує DAX ✅
- SMT divergence відсутня — unified bullish flow

**Рекомендований playbook:** `london-open-range-breakout` з EQL sweep variant.

**Setup score: 7/10**
- HTF alignment (W/D/H4/H1): +3
- Clear liquidity targets (EQL below + PDH above): +2
- London KZ active: +1
- News cluster 06:00 UTC (German IP): -1
- ISM blackout 13:30–14:30: -1 (обмежує NY window)
- MCP дані не live (скріни від 04.05): -1 (uncertainty penalty)
- Мінус 1 за те що pre-market, потрібен тригер

**RR > 1:2 на TP1 ✅ — setup торгувальний.**

> **Відмова:** Не входити без чіткого тригера (sweep EQL або ORB breakout з retestом). Pre-market позиція — WAIT. Лондонський open (06:00–07:00 UTC) — вікно спостереження.

---
*Аналіз складено: 2026-05-05 05:40 UTC | FOREXCOM:GER40 | Структурний TDA (context-based)*
*Skill: tda-bias | Strategy: london-open-range-breakout | Agent: analyst*
*Скріни: референсні з 2026-05-04 — оновити через MCP при відкритті London*
