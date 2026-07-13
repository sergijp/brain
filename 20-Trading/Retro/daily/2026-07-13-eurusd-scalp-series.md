---
title: "Retro daily — EURUSD scalp-series (PAPER/BACKTEST) 2026-07-13"
date: 2026-07-13
period: daily
tags: [trading, retro, daily, backtest, paper, scalp-series, eurusd]
category: trading
pair: EURUSD
agent: retro
mode: paper-backtest
real_account_touched: false
trades_count: 5
filled_count: 3
win_rate: 0.0
paper_pnl_usd: -299
paper_pnl_pct: -2.99
pinecone_indexed: false
---

# Retro daily — EURUSD scalp-series (PAPER / BACKTEST) — 2026-07-13

> ⚠️ **PAPER / BACKTEST-серія.** Усі позиції — plan-drawings на графіку (tv-position), форвард/бектест.
> Реальний депозит **НЕ задіяно** ($0 real). `_risk-state.json`: real `consecutive_losses=0`, day 0% / week 0%.
> Вікно: London-сесія, ~10:00–11:00 Київ (07:00–08:00 UTC).

## Контекст ринку

- HTF bias: **bearish** (W/D corrective, H4 BOS 1.1412) — ранковий TDA-пайплайн дав swing-short.
- АЛЕ London-сесія відкрилась чистим **bullish displacement / continuation**: ~1.1408 → high **1.14458** (+50 pips) майже без відкату.
- Тобто LTF-потік (M5/M15) весь час дивився ВГОРУ, поки HTF bias тримав нас у ведмежій упередженості. Класичний конфлікт HTF-anchor vs LTF-flow.

## Summary

- Планів на графіку: **5** (4 SHORT + 1 LONG). Заповнено фактично: **3** (усі SHORT).
- Результат filled: **0W / 3L / 0BE** → win rate **0%**.
- LONG: напрямок правильний, але **missed fill** (ліміт занадто глибоко в FVG) → $0.
- 5-й SHORT: **інвалідований до входу** → NO-TRADE (правильно не взято) → $0.
- **Paper P&L: −$299 (−2.99% від $10000).**
- Paper-drawdown серії ≈ денний ліміт 3% — якби це був live, ми б впритул підійшли до `BLOCK` за day-risk.
- Paper consecutive losses цієї серії: **3 поспіль** (swing → scalp#1 → scalp#2, усі fade проти потоку).

## Хронологія та розбір

| # | Сетап | Напрям | Entry | SL | TP | Результат | Paper P&L |
|---|-------|--------|-------|----|----|-----------|-----------|
| 1 | Swing (ранковий TDA) | SHORT | 1.1407 | 1.1428 | 1.1384 / 1.1355 / 1.1330 | SL 1.1428 (ціна вгору) — **LOSS** | −$99 (0.99%) |
| 2 | Scalp#1 range-fade верху | SHORT | 1.1408 | 1.1414 | 1.1387 | SL одразу (імпульс 1.14222) — **LOSS** | −$100 (1%) |
| 3 | Scalp#2 failed-breakout fade | SHORT | 1.1420 | 1.1424 | 1.1401 | SL (continuation, sweep-high утримався) — **LOSS** | −$100 (1%) |
| 4 | LONG-continuation (розворот на потік) | LONG | 1.1420 (limit у FVG) | 1.1415 | 1.14280 / 1.14440 | Ліміт **НЕ заповнився** (мін 1.1423, high 1.14432, −8p від TP2) — **MISSED FILL** | $0 |
| 5 | SHORT-conditional (fib 1.618 @1.1444) | SHORT | 1.1438 | 1.1446 | 1.1410 | Інвалідований: high 1.14458 без CHoCH-тригера (M5 close <1.14342) — **NO-TRADE** | $0 |
| | | | | | | **РАЗОМ** | **−$299 (−2.99%)** |

## Best / Worst

- 🟢 **Best (за рішенням):** крок #4 LONG — Dixie **правильно визнав continuation** і розвернувся на потік. Напрямок був точний (ціна дійшла на −8p від TP2). Помилка лише в **execution**, не в аналізі.
- 🟢 **Дисципліна:** крок #5 — коректно **НЕ взято** short без тригера (high оновився без CHoCH). Механічний фільтр спрацював як треба.
- 🔴 **Worst (кластер):** кроки #1–#3 — три fade поспіль проти чистого bullish displacement. Це і є ключова помилка дня.

## Recurring errors — патерн 3× fade проти displacement

Що спільного в усіх трьох програшних SHORT:

1. **Фейд проти LTF-потоку під час активного displacement/CISD.** Ринок показував continuation (HH/HL на M5), а ми щоразу шукали розворот верху. Fade у трендовий імпульс = ловити падаючий ніж навпаки.
2. **HTF-anchor bias засліпив LTF-reality.** Ведмежий W/D bias змусив тримати short-упередженість, попри те що London відкрито дав displacement вгору. Bias ≠ вхід: HTF дає напрям тижня, але не дозволяє фейдити чистий intraday-потік.
3. **Немає підтвердження розвороту перед входом.** Жоден із 3 shorts не чекав CHoCH / зміни структури на LTF — входили «в рівень», а не «в підтверджений розворот». (Іронія: саме крок #5, де тригер CHoCH був обов'язковим, врятував від 4-го лоссу.)
4. **Тісні SL у зоні високого моментуму.** SL 4–6 pips (scalp#1: 6p, scalp#2: 4p) під час +50p impulse-руху — статистично мали бути вибиті. Momentum «з'їдає» тісні контр-трендові стопи миттєво.

**Корінь:** боротьба з ринком. Три спроби продати силу = три донати (paper).

## Що спрацювало / урок про execution (крок #4)

- Dixie правильно **перемкнувся з fade на with-flow** — це вірний висновок.
- АЛЕ вхід-ліміт 1.1420 поставлено **надто глибоко в FVG** (класичний повний FVG-fill). У сильному displacement ціна **не дає глибокого ретесту** — мінімум був лише 1.1423, і потік поніс далі.
- **Урок execution:** на momentum-continuation ретести **дрібніші**, ніж класичний FVG-fill. Треба:
  - вхід по **мілкому ретесту / 50% FVG** або по **micro-BOS + retest** ближчого рівня, а не по дну імпульсної зони;
  - або **market/stop-entry по підтвердженню continuation**, а не пасивний глибокий ліміт;
  - прийняти трохи ширший SL заради заповнення — краще filled з RR 1:2, ніж «ідеальний» ліміт, що не тригернув.

## Правило-висновок для стратегії

> **Коли на LTF є чистий CISD / displacement — НЕ фейдити. Торгувати з потоком.**
> - Ознака displacement: великий imbalance-свічковий рух + серія HH/HL (long) без відкату, sweep-high утримується.
> - Fade верху/низу дозволено **лише** після LTF-**CHoCH/зміни структури** (як у фільтрі кроку #5), не «в рівень».
> - На momentum-continuation entry: **мілкий ретест (≤50% FVG) або stop-entry по підтвердженню**, НЕ глибокий FVG-fill-ліміт.
> - HTF bearish bias **не дає права** шортити чистий bullish intraday-потік — чекати, поки потік вичерпається (sweep + CHoCH), тоді вхід за bias.

→ Кандидат на додавання в `smc-price-action-combo.md` (секція «Anti-pattern: fade проти displacement») та в ASR-фільтри (F: no-counter-trend-fade під час London displacement).

## Risk discipline (PAPER)

- Real-рахунок: **недоторканий** ($0, real `consecutive_losses=0`, day 0% / week 0%).
- Paper-drawdown серії: **−2.99%** — практично впритул до денного `BLOCK`-ліміту 3%. Урок: навіть у paper 3 fade поспіль «вибрали» б увесь денний ризик за годину.
- Paper consecutive losses: **3 поспіль** — у live це = `BLOCK` за правилом max 3 consecutive losses → зупинка до retro. **Механічно серію треба було зупинити після 2-го лоссу.**
- Overrides: 0. NO-TRADE #5 — коректна дисципліна.

## Repeated-focus — EURUSD PAIR-HEAT ⚠️

- EURUSD **знову** в центрі уваги. `_risk-state.json` вже фіксує **7 спроб/0 wins** за тиждень (07-08 pair-heat) + `EURUSD-long-AMD` ACTIVE-BLOCK-WATCH (4 attempts/0 clean wins за 30 днів).
- Сьогоднішня серія додає ще **3 filled attempts** у парі → сукупно **7+ дотиків за місяць** без чистого win.
- **Флаг:** EURUSD — гарячий, real-вхід у пару потребує **чистого win або бектесту** (performance-analyst) перед будь-яким live.
- Дзвіночок: більшість спроб — контр-трендові до intraday-потоку. Пара «карає» саме за fade.

## Lessons

1. **Не продавай силу.** Чистий bullish displacement на London = with-flow only; fade без CHoCH — донат (3/3 підтвердили).
2. **HTF bias — це напрям, не тригер.** Ведмежий W/D не скасовує bullish London-потік; чекай sweep+CHoCH, тоді входь за bias.
3. **Execution на momentum: мілкий ретест, не глибокий FVG-fill.** Крок #4 мав правильний напрям і програв лише через занадто консервативний ліміт.
4. **Стоп-серії: після 2 лоссів поспіль — пауза.** Механічний `BLOCK` після 3 існує не просто так; у paper 3 fade ≈ денний ліміт 3%.
5. **EURUSD pair-heat реальний** — 7+ дотиків/0 wins за місяць; пара під підвищеним гейтом.

## Action items for next period

- [ ] Додати в `smc-price-action-combo.md` anti-pattern «no fade проти London displacement без CHoCH».
- [ ] Формалізувати momentum-continuation entry (мілкий ретест ≤50% FVG / stop-entry по підтвердженню) — окремий чек-ліст.
- [ ] Ввести hard-стоп серії: **пауза після 2 fade-лоссів поспіль** в один бік проти потоку (paper теж).
- [ ] EURUSD → **performance-analyst бектест** counter-trend fade vs with-flow на London displacement (pair-heat 7+/0 вимагає даних перед live).
- [ ] У ранковому TDA додати перевірку: «чи London вже дав displacement?» — якщо так, swing-short bias ставиться на паузу до вичерпання потоку.

## Pair-specific notes

- **EURUSD:** сьогодні класичний «bias-trap» — HTF bearish, а London поніс +50p вгору. Пара стабільно карає за fade верху під час displacement. PAIR-HEAT активний. Найкраще вікно London KZ дало саме bullish continuation — with-flow long-логіка була б прибутковою, fade — ні.

## Пов'язані

- Risk state: `~/MyVault/20-Trading/Journal/_risk-state.json`
- Watch: `EURUSD-long-AMD` (ACTIVE-BLOCK-WATCH), `EURUSD-pair-heat-2026-07-08`
- Стратегія: [[Strategies/smc-price-action-combo]], [[Strategies/asr-orb-intraday-system]]
- Попередня ретро: [[Retro/weekly/2026-06-21]]
