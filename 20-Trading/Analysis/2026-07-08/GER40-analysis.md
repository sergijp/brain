---
title: GER40 Top-Down Analysis
date: 2026-07-08
tags: [GER40, TDA, bullish-corrective, indices]
category: Analysis
project: Trading
pair: GER40
strategy: asr-orb-intraday-system
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GER40 (DAX): Top-Down Analysis — 08.07.2026

> Час аналізу: 06:17 UTC / 09:17 Kyiv. Дані TV свіжі (last bar 06:15 UTC). Ціна ~25 382.
> Pre-open: Xetra/Frankfurt open ~10:00 Kyiv (07:00 UTC). ASR-вікно з 10:05 Kyiv, ORB-30 = 10:00–10:30 Kyiv.

## 🏛 Weekly (Тижневий графік)
W: +14.52% за 15 тижнів, range `21 934 – 25 923`. Останні 5W closes: `24 671 → 24 997 → 24 642 → 25 806 → 25 380` — серія HH/HL, минулого тижня зроблено новий ATH **25 923**, після чого верхній wick і закриття на 25 380 (rejection від ATH). **HTF Bullish**, короткостроково — corrective відкат від хаїв.

![[img/ger40_w.png]]

## 📅 Daily (Денний графік)
20D +5.54%, range `23 950 – 25 923`. Останні 5D closes: `25 604 → 25 806 → 25 827 → 25 464 → 25 382` — після ATH 25 923 два дні розподілу вниз (25 827 → 25 464 → 25 382). Класичний 2-денний pullback у висхідному тренді. PDH `25 531`, PDL `25 363`. Ціна тестує нижню межу відкату. Тримає 25 363 → продовження вгору; sweep 25 363 імовірний на відкритті.
**D bias: Bullish (pullback у демандну зону).**

![[img/ger40_d.png]]

## ⏱ 4-Hour (4-годинний графік)
H4 range `24 887 – 25 923`, +1.25%. Останні 5×4H closes: `25 538 → 25 464 → 25 506 → 25 459 → 25 382` — низхідний corrective-канал (LH: 25 674 → 25 552 → 25 531 → 25 474). Ціна на EMA, щойно протестувала H4-low `25 363`. Нижче — H4 OTE/demand `24 400–24 900` (глибший відкат). **H4: bearish-corrective всередині D-uptrend.** Поки 25 363 тримається — це кінцева фаза відкату, а не розворот.

![[img/ger40_h4.png]]

## 🕐 1-Hour (1-годинний графік)
H1 -1.1%, range `25 363 – 25 706`. Овернайт грінд вниз від 25 706 у sell-side ліквідність `25 363`. Остання H1 закрилась 25 385 після тесту 25 363.5. H1-supply `25 460–25 517` (найближчий LH-кластер). H1 короткостроково bearish, але це протяжка в HTF-demand.
**SMT:** перевірити US500/US100 у момент входу — США закрились біля ATH, risk-on цілий, ведмежої розбіжності овернайт немає → підтверджує bull HTF.

![[img/ger40_h1.png]]

## 🎯 15-Minute (15-хвилинний графік)
Pre-open консолідація `25 363 – 25 517`, ціна на "Weak Lo" 25 363. Frankfurt open (~10:00 Kyiv) — тригер.
Сценарії:
1. **Консервативно (LONG — основний):** Xetra open робить sweep `25 363` (Asian/overnight low + PDL + H4-low), M15 reclaim-свічка закривається назад над 25 363 → **ASR LONG** до 25 460 → 25 517 → 25 680.
2. **Агресивно (SHORT — альт):** пробій 25 363 з імпульсом + ретест 25 460 як supply тримає → продовження H4-відкату до OTE `24 900`. Проти D-bias — тільки з чітким CHoCH вниз.

![[img/ger40_m15.png]]

## ⚡ 5-Minute (5-хвилинний графік) — Торговий план (preliminary, ASR)

- **Bias:** Bullish-corrective (long на sweep-reclaim) 📈
- **Setup:** ASR (Asia Sweep & Reclaim) — sweep 25 363 → reclaim
- **Entry Zone:** `25 365 – 25 385` (reclaim свеп-лоу після Frankfurt open)
- **Stop Loss:** `25 325` (під sweep-low + буфер) — **~50 pts**
- **TP1:** `25 460` — RR ~1.9 (H1-supply / часткова фіксація)
- **TP2:** `25 517` — RR ~2.8 (M15-range high)
- **TP3:** `25 680` — RR ~6.1 (OTE / рух до Strong High 25 806)
- **Lot Size:** `$100 / (50 pts × $1) ≈ 2 контракти` (GER40: 1 pt = $1/контракт — перевірити брокер)
- **Ризик:** $100 (1% від $10 000)

### 🅱 ORB (Xetra ORB-30) — сателіт
- Діапазон формується **10:00–10:30 Kyiv** (07:00–07:30 UTC).
- Торгувати **після 10:30 Kyiv**: breakout за межу ORB-діапазону з ретестом.
- HTF bull → пріоритет **long-breakout вгору** (над ORB-high). Short-breakout нижче ORB-low — тільки якщо 25 363 вже зламано і ASR-long інвалідовано.
- Статус: ORB live заблоковано до вересня 2026 → сьогодні **signal/forward-only**.

![[img/ger40_m5.png]]

---
## 🔑 Ключові рівні
| Рівень | Ціна | Тип |
|--------|------|-----|
| Liquidity above / ATH | 25 923 | Weekly high (BSL, Weak High) |
| Strong High / D-supply | 25 806–25 841 | D OB (prev closes) |
| Intraday supply | 25 460–25 517 | H1/M15 LH-кластер |
| **Поточна ціна** | ~25 382 | — |
| **Key support / SSL** | 25 363.5 | PDL = H4-low = Weak Lo (sell-side liquidity) |
| H4 OTE / deep demand | 24 400–24 900 | H4 demand (глибший відкат) |

## 📌 Коментар
- **HTF bull + короткостроковий відкат у SSL 25 363** — ідеальна конфігурація для ASR-long на Frankfurt open (sweep-reclaim買 в бік старшого тренду).
- Триггер обов'язковий: без reclaim-підтвердження 25 363 — це "ніж", не входити.
- День CLEAR. High-impact лише **FOMC Minutes 18:00 UTC (21:00 Kyiv)** — після інтрадей-flat (17:45 Kyiv), у вікно ASR/ORB не потрапляє, blackout немає.
- Session: найкраще вікно GER40 — Frankfurt/London open 10:00–13:00 Kyiv. Правило входу ≥09:00 Kyiv виконано. Flat до 17:45 Kyiv.
- **Setup score: 7/10** — HTF-конфлюенс сильний, але потрібне підтвердження reclaim; короткостроково структура ще bearish.
- ⚠️ На графіку присутні індикатор "Entry Points: EMA+RSI+MACD" і зонні малюнки (OTE/Weak Hi/Lo) — не чіпав, лише аналіз.
