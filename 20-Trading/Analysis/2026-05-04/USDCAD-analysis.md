---
title: USDCAD Top-Down Analysis
date: 2026-05-04
tags: [USDCAD, TDA, bearish-strong, forex]
category: Analysis
project: Trading
status: analysis-complete
pair: USDCAD
strategy: boc-speech-fade-continuation
agent: analyst
pinecone_indexed: false
---

# USDCAD: Top-Down Analysis — 04.05.2026

> Snapshot: 05:32 UTC / 08:32 Kyiv. Spot **1.35920** (OANDA). Data freshness OK (last bar 05:10 UTC).
> ⚠️ **News blackout 19:00–20:00 UTC** — BoC Macklem speech 19:30 UTC. Будь-яка позиція має бути закрита/переведена в BE до 19:00 UTC.

## 🏛 Weekly (Тижневий графік)
W: **-1.27%**, 15W range `1.34197 – 1.47937`. Останні 5W closes: `1.38431 → 1.36934 → 1.36692 → 1.35938 → 1.35914` — **чітка серія LH/LL, weekly bearish continuation**. Ціна за 5 тижнів зробила 4 червоні свічки поспіль і знаходиться у нижній 12% W-діапазону. **HTF Bearish-Strong**.

![[img/usdcad_w.png]]

## 📅 Daily (Денний графік)
20D **-1.31%**, 100D range `1.34818 – 1.39670`. Останні 5D: `1.36842 → 1.36838 → 1.35822 → 1.35938 → 1.35914` — distribution під рівнем 1.3690, **D BOS вниз через 1.3582** на 3-й сесії. Ціна тестує локальний support 1.3590 (psych) перед потенційним протяжкою на 1.34818 (D liquidity нижче 100D-low).

![[img/usdcad_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 100b range `1.35501 – 1.38780`, **-1.64%**. Останні 5×4H: `1.35880 → 1.35938 → 1.35884 → 1.35902 → 1.35915` — **H4 swept low 1.35501** і робить **corrective bounce** до 1.3590-х. Це класична post-sweep accumulation перед продовженням або справжнім reversal. H4 swing high лишився `1.36360`. H4 OB зона `1.3610 – 1.3625` (last consolidation перед sell-off).

![[img/usdcad_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 **-0.33%** за останні 100h, range `1.35501 – 1.37111`. Останні 5h: `1.35900 → 1.35908 → 1.35856 → 1.35902 → 1.35915` — **tight coil 1.3585–1.3596**, формується EQH `1.35961`. Якщо ціна знесе EQH у London KZ — first target M15 short trigger у H1 OB 1.3610.

**SMT (USDCAD ↔ DXY):** USDCAD за тиждень -1.64% при відносно стабільному DXY → **це CAD-strength move**, не USD weakness. Корелят з нафтою (WTI вгору) пояснює тиск. Pre-BoC speech це додатково b​ullish для CAD (Macklem hawkish risk).

![[img/usdcad_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
M15 range `1.35501 – 1.35961`. Coil під EQH, потенційний liquidity grab.

Сценарії:
1. **Консервативно (SHORT continuation):** sweep EQH `1.35961` → ретест H1 OB `1.36050 – 1.36250` → CHoCH вниз → entry SHORT з ціллю 1.3578/1.3550.
2. **Агресивно (LONG fade pre-news):** sweep `1.35501` (H4 low) ще раз → CHoCH вгору на M5 → scalp до 1.3625 з обов'язковим виходом до 17:00 UTC.

![[img/usdcad_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план

### Власний edge: "Pre-BoC Speech Continuation Fade" (без шаблонної стратегії)

**Логіка edge:**
- USDCAD у явному 4-денному селл-офі від 1.3690 до 1.3550. Перед топ-tier подією (Macklem 19:30 UTC) ринок зазвичай робить **short-coverage squeeze у London open** і повертається до domінантного тренду в US-сесії.
- Це дає вікно `London KZ open (06:00–08:00 UTC влітку) → 17:00 UTC` для входу SHORT від відскоку, з обов'язковим виходом до blackout.
- Edge не з playbook бібліотеки — це **event-anchored mean-reversion fade у напрямку HTF bias**: ловимо squeeze у H1 OB, продаємо continuation до D-low.

**Plan (PRIMARY — SHORT continuation):**

- **Bias:** Bearish-Strong (W LL, D BOS вниз, H4 -1.64%) 📉
- **Entry Zone:** `1.36050 – 1.36250` (H1 OB + previous H4 imbalance)
- **Stop Loss:** `1.36400` (вище H4 swing high 1.3636 + 4 pip buffer) — 15–35 pts від ентрі (для midpoint 1.3615 → 25 pts)
- **TP1:** `1.35780` (M5/H4 sweep area) — RR **≈ 1.5** (від midpoint)
- **TP2:** `1.35501` (H4 absolute low) — RR **≈ 2.6**
- **TP3:** `1.34818` (D 100-day low / liquidity grab) — RR **≈ 5.3**
- **Lot Size:** `$100 / (25 pts × $7.36/pip) ≈ 0.54 lot` → округлення **0.5 lot**.
  - USDCAD pip value: `1 pip = $10 / quote ≈ $10/1.359 ≈ $7.36` за стандартний lot (перевірити брокер OANDA).
  - Ризик при 0.5 lot і SL 25 pts: ≈ $92.

**Час-контроль (CRITICAL):**
- 🟢 Window для входу: **08:00 – 18:00 UTC** (London open до US close-ish).
- 🔴 **Hard exit (close or BE) до 19:00 UTC** — за 30 хв до BoC Macklem speech.
- Якщо до 18:30 UTC ентрі-зона `1.3605–1.3625` не торкнулась → **PASS**, не переслідувати в blackout.

**ALT (LONG scalp pre-news, тільки якщо H4 закладає reversal CHoCH):**
- Entry: `1.35550 – 1.35650` (H4 OB після sweep low)
- SL: `1.35450`
- TP1: `1.35900` — RR ≈ 2.5; TP2: `1.36050` — RR ≈ 4
- Тільки на чітких bullish triggers (CHoCH M15 + sweep 1.3550). HTF проти, тому B-tier setup.

![[img/usdcad_m5.png]]

---

## ⚠️ Risk & News

| Перевірка | Статус |
|-----------|--------|
| Session window (London KZ 06:00–08:00 UTC summer) | Зараз 05:32 UTC — за 30 хв London KZ |
| Kyiv time entry rule (≥ 09:00) | 08:32 — **WARN: ще зарано**, чекати 09:00 Kyiv |
| News blackout (BoC Macklem 19:30 UTC ±30 min) | **HARD: позиція закрита/BE до 19:00 UTC** |
| RR TP2 ≥ 1:2 | ✅ 2.6 |
| Risk % | 1% ($100 з $10k) |
| SMT confirm | ✅ CAD-strength домінує, USDCAD проти кошика |

## 🧠 Коментар

USDCAD у чіткому 3-тижневому downtrend з фундаментальним підкріпленням (CAD-positive): нафта Brent +6% за тиждень, BoC очікувано hawkish. Технічно ринок дав sweep H4 low і робить класичний bounce — це **B+ short-continuation setup**, не reversal. **Edge** — комбо HTF bias × event-anchored timing window. Без BoC speech це був би стандартний trend-pullback; саме pre-news squeeze робить ентрі чистішим, бо great спрацює до US opening.

**Stand-aside conditions:**
- Якщо до 18:00 UTC ціна не дала ретест 1.3605
- Якщо H4 закриється вище 1.3640 (інвалідує bias)
- Якщо WTI закриється -2% або більше в US-сесії (CAD-strength розпалюється — refuse short)
