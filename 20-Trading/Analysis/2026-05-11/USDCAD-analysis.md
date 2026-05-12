---
title: USDCAD Top-Down Analysis
date: 2026-05-11
tags: [USDCAD, TDA, bearish-corrective, forex]
category: Analysis
project: Trading
pair: USDCAD
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# USDCAD: Top-Down Analysis — 11.05.2026

> Аналіз виконано: 06:42 UTC / 09:42 Kyiv. Поточна ціна **1.36780**. Last bar M5: 2026-05-11 06:40 UTC — дані свіжі (Mon, London open щойно стартував).

## Weekly (Тижневий графік)

W: **−0.41%** (open 1.37344 → close 1.36782). 52W range `1.34197 – 1.47937` — ціна у нижній третині (~19% від low). Останні 5W: `1.36934 → 1.36692 → 1.35938 → 1.36764 → 1.36782` — серія LL з sweep лоу `1.35501` і двома bullish-corrective свічками відновлення. **HTF Bias: Bearish-Corrective.** Макро-тренд bearish (LH/LL з ATH 1.4794), але локально формується HL → bear-flag/reaccumulation у зоні `1.355–1.370`. Key W-resistance — кластер `1.371–1.377` (попередні swing lows тепер як supply).

![[img/usdcad_w.png]]

## Daily (Денний графік)

20D range `1.34818 – 1.39670`, close `1.36780`, change −0.7%. Останні 5D: `1.36203 → 1.36336 → 1.36650 → 1.36764 → 1.36780` — м'який bullish stair-step (HH/HL) з лоу `1.35781`, але momentum затухає (тіла свічок ~25–40 пунктів — низький impulse). D-bias: **Bullish-Corrective пуллбек у W bearish trend.** Поточна ціна тестує D-supply `1.3690–1.3710` (відкат у попередню зону розподілу). PDH `1.36951` (sweep сьогодні вже відбувся в Asia → потенційний SSL refill вниз).

![[img/usdcad_d.png]]

## 4-Hour (4-годинний графік)

H4 range останніх 100 барів `1.35501 – 1.37146`, change −0.18%. Останні 5×H4: `1.36896 → 1.36764 → 1.36836 → 1.36942 → 1.36782` — формується **M-pattern** з double-top `1.36944/1.36951`. H4 swing high `1.36951`, swing low `1.36761`. **Структура: початок CHoCH вниз** — остання H4 свічка закрилась нижче midpoint попередніх діапазонів (bear engulfing на BSL sweep `1.36951`). H4 OB-supply: `1.36880 – 1.36945` (close попередньої bullish свічки + sweep wick).

![[img/usdcad_h4.png]]

## 1-Hour (1-годинний графік)

H1 100-bar range `1.35781 – 1.37104`, change +0.41%. Останні 5H: `1.36876 → 1.36890 → 1.36942 → 1.36924 → 1.36782` — bearish closure (-16 pips на останньому H1) після BSL sweep `1.36951`. **H1 BOS вниз через `1.36784`** (попередній HL). H1 OB-supply: `1.36880 – 1.36924` — last bullish OB перед impulse down. H1 demand нижче: `1.36428 – 1.36540` (свіжий M15 demand зона), потім `1.35781`.

**SMT з DXY:** USD-кошик зараз у консолідації. Якщо DXY формує LH, а USDCAD намагається пробити нагору → divergence → користь bears (поточна ситуація co-confirms — USDCAD rejected від 1.3695, DXY теж rejected).
**Cross-check з EURUSD / GBPUSD:** обидві мейджори — bullish-corrective сьогодні. Якщо USD взагалі слабшає → USDCAD продовжить вниз.

![[img/usdcad_h1.png]]

## 15-Minute (15-хвилинний графік) — сценарії

Останні 5×M15: `1.36930 → 1.36924 → 1.36798 → 1.36768 → 1.36782` — **M15 BOS вниз** через попередній HL ~`1.36830`. Зараз pullback вгору від лоу `1.36761`.

**Сценарії:**
1. **Консервативно (SHORT) — PRIMARY:** ретест зони `1.36850 – 1.36920` (H1+M15 supply OB) + M5 CHoCH вниз → SHORT до `1.36540`, потім `1.36420`. Це класичний *Sweep + OB Rejection + Retest* (SMC+PA primary pattern).
2. **Альтернативно (LONG, contra-trend):** sweep лоу `1.36540` (M15 demand) + M5 CHoCH вгору → LONG до `1.36900`. Менша ймовірність — проти H4 CHoCH.
3. **Інвалідація bearish сетапу:** H4 close > `1.36955` → bias повертається до bullish-corrective, чекати на pullback до D-demand `1.36650`.

![[img/usdcad_m15.png]]

## 5-Minute — Торговий план (SHORT, PRIMARY)

- **Bias:** Bearish (corrective continuation у W-trend, після H1 BOS down)
- **Playbook:** `smc-price-action-combo` — Sweep BSL `1.36951` + H4 OB rejection + M15 BOS down + retest
- **Entry Zone:** `1.36870 – 1.36920` (H1 OB-supply, M15 imbalance fill)
- **Trigger:** M5 bearish CHoCH у зоні (нижче `1.36850`) + close під 1.36850
- **Stop Loss:** `1.36975` (вище H4 BSL sweep high 1.36951 + 25pt буфер) — **~95 pts від mid-entry 1.36895**
- **TP1:** `1.36700` — RR ≈ **2.05** (H1 mid, найближчий PD-level)
- **TP2:** `1.36540` — RR ≈ **3.74** (M15 demand top — частковий fix)
- **TP3:** `1.36420` — RR ≈ **5.0** (D swing low cluster, цільовий intraday фікс)
- **Lot Size:** `$100 / (95 × $10) ≈ 0.105 lot` (OANDA: 1pt = $10 на 1 lot для USDCAD при USD-account — перевірити брокер; для USDCAD pip value насправді = `$10 / USDCAD`, тобто ~$7.31, тоді lot ≈ 0.144)

⚠️ **Pip value caveat:** для USDCAD pip-value в USD = `1 / quote × контракт`. На 1 standard lot (100 000 CAD) = `100000 × 0.0001 / 1.36780 ≈ $7.31` за пункт. Перерахунок: `$100 / (95pt × $7.31) ≈ 0.144 lot`. Перевірити з брокером перед входом.

![[img/usdcad_m5.png]]

---

## Підсумок

| Параметр | Значення |
|----------|---------|
| HTF (W) bias | Bearish-Corrective |
| Daily bias | Bullish-Corrective пуллбек (резистанс) |
| H4 structure | M-pattern, початок CHoCH вниз |
| H1 structure | BOS down після BSL sweep |
| Market regime | **Reversal / Trend-continuation вниз** (W-bear + H4-CHoCH) |
| Playbook | `smc-price-action-combo` (PRIMARY: Sweep+OB+Retest) |
| Direction | **SHORT** (intraday) |
| Setup score | **7/10** |

### Ключові POI на сьогодні

| Тип | Рівень | Призначення |
|-----|--------|-------------|
| H4/H1 OB-supply | `1.36870 – 1.36945` | SHORT entry zone |
| BSL (свіжий sweep) | `1.36951` | Stop reference |
| H1 demand | `1.36540 – 1.36428` | TP2/TP3 |
| D swing low (target) | `1.36420 – 1.36340` | TP3 / intraday max |
| W invalidation level | вище `1.37150` | Bias flip до bullish |

### Коментар

- **Сесія:** Markdown пишеться на старті London KZ (07:00–09:00 UTC влітку, але DST → London KZ 06:00–08:00 UTC). Зараз 06:42 UTC — **активна London KZ**, оптимальне вікно для USD-major.
- **Best session для USDCAD:** NY KZ (CAD-driven), але London часто дає manipulation move. Сьогодні очікувати retest у London → impulse у NY.
- **News risks (перевірити ForexFactory):** дивитись CAD CPI / BoC / US ISM на сьогодні. Якщо є high-impact CAD event у NY → почекати завершення blackout.
- **Intraday правило:** позиція має бути закрита до кінця дня. TP3 досяжний за London+NY, але якщо до 20:00 Kyiv ціна стоїть — закрити вручну на whatever RR.
- **Risk:** на $10000 депозит, 1% = $100 ризик. SL 95pt → 0.14 lot. **Не входити раніше 09:00 Kyiv** — зараз 09:42 → OK.
- **Не торгувати:** якщо M5 close > 1.36975 без retest — bias invalidated, скип.

---
**Файл:** `~/MyVault/20-Trading/Analysis/2026-05-11/USDCAD-analysis.md`
**Скріни:** `~/MyVault/20-Trading/Analysis/2026-05-11/img/usdcad_*.png` (6 PNG: w, d, h4, h1, m15, m5)
