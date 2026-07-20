---
title: GBPUSD Top-Down Analysis
date: 2026-07-20
tags: [GBPUSD, TDA, bullish-strong, forex, ASR]
category: Analysis
project: Trading
pair: GBPUSD
strategy: asr-orb-intraday-system
agent: analyst
status: analysis-complete
pinecone_indexed: false
---

# GBPUSD: Top-Down Analysis — 20.07.2026

> Час аналізу: 06:06 UTC / 09:06 Київ (понеділок). Депозит $10 000, ризик 1%.
> News: ЧИСТО — жодного high-impact по USD/GBP, blackout немає.
> ⚠️ **Скріншоти недоступні цього прогону.** MCP залочений на tab index 0 (GBPUSD 1W — дані двигуна коректні), але передній видимий tab у вікні TV показує EURUSD 15m, і Chromium throttle-ить рендер бекграунд-таба → CDP-скрін повертав заморожений EURUSD-кадр. Виводити tab 0 на передній план = `tab_switch`, що заборонено Tab Lock Policy під час аналізу. Аналіз побудований на підтверджених числових OHLCV-даних GBPUSD.

## 🏛 Weekly (Тижневий графік)
W +1.88%. 15W range `1.20997 – 1.38700`. Останні 5W closes: `1.31974 → 1.33536 → 1.34021 → 1.34522 → 1.34664` — чиста серія вищих закриттів, впевнене bullish momentum від бази 1.21. Ціна у верхньо-середній частині W-range, під swing high 1.38700. **HTF Bullish (momentum).**

## 📅 Daily (Денний графік)
20D +0.44%, range `1.31402 – 1.36578`. Останні 5D: `1.33914 → 1.35390 → 1.34793 → 1.34522 → 1.34663`. Сильний імпульсний день до 1.35582 (swing high), далі 2–3-денний неглибокий pullback до 1.34262, зараз відскок. Daily формує **HL ~1.343** — bullish continuation, дискаунт для лонгу.
Ключові D-рівні: resistance/BSL **1.35582** → **1.36578**; support/demand **1.34262** → **1.33802**.

## ⏱ 4-Hour (4-годинний графік)
H4 range `1.31804 – 1.35582`, +1.97%. Імпульс 1.318 → 1.35582 (**BOS up**), відкат до 1.34262–1.34283 (**HL**), відновлення до 1.3466. Bullish-структура HH/HL збережена.
H4 swing high **1.35582** (BSL / ціль). H4 swing low / HL **1.34262**. H4 demand-зона **1.343**.

## 🕐 1-Hour (1-годинний графік)
H1 +0.82%. Останні 5H: `1.34543 → 1.34592 → 1.34607 → 1.34664 → 1.34664` — щільна акумуляція в азійську сесію під Asia high. H1 OB/FVG для ретесту: **~1.345**, глибше **1.343**.
**SMT (vs EURUSD / DXY):** DXY 100.73 м'яко слабкий (-0.03%), EURUSD 1.1439 flat, EURGBP вниз → **GBP сильніший за EUR**. Фунт веде проти долара — bullish-конфлюенс для лонгів GBPUSD, без ведмежої дивергенції.

## 🎯 Asia Range & ASR-сетап (ядро системи)
- **Asia High ≈ `1.34688`** (BSL зверху)
- **Asia Low ≈ `1.34389`** (SSL знизу)
- Ширина азійського діапазону ≈ **30 pips**
- Поточна ціна `1.34662` — біля **верхньої межі** Asia range (~26p над Asia low, ~2–3p під Asia high).

**Вікно ASR:** 09:00–13:00 Київ, London open 10:00 Київ (07:00 UTC), flat 17:45. Зараз 09:06 Київ — вікно щойно відкрилось, до London ~54 хв.

**Стан:** сетап ще НЕ тригернутий (pre-London, свіп/reclaim не відбувся). Пріоритет напрямку — **LONG** (HTF bull + GBP relative strength).

Сценарії ASR:
1. **A — Asia-low sweep + reclaim (пріоритетний, найкращий RR).** London робить Judas-провал під Asia low `1.34389` (свіп SSL) → швидкий reclaim назад у діапазон → **M15 close вище 1.344** → LONG.
2. **B — Break & retest Asia high.** Пробій і утримання над `1.34688` на London-моментумі → ретест 1.3462–1.3469 → LONG-continuation до 1.35582.
3. **Контр-сценарій (низький пріоритет, лише при сильному rejection+CHoCH):** свіп Asia high `1.34688` і фейл назад → short. Йде проти HTF — тільки як реакція, не базовий план.

## ⚡ Торговий план (LONG-пріоритет)

- **Bias:** Bullish (long, momentum) 📈
- **Entry Zone A (ASR reclaim):** `1.34390 – 1.34450` (свіп Asia low + M15 reclaim)
- **Entry Zone B (continuation):** `1.34620 – 1.34690` (ретест після пробою Asia high)
- **Stop Loss:** `1.34240` (нижче Asia low sweep та H4 HL 1.34262)
  - для Zone A (~1.3442): **≈18 pips**
  - для Zone B (~1.3466): **≈26–32 pips**
- **TP1:** `1.34809` (M15 high / найближча ліквідність) — швидка ціль
- **TP2:** `1.35582` (D/H4 swing high, BSL) — основна ціль, ~90–116p
- **TP3:** `1.36578` (20D high) — розширення (частково поза інтрадей-досяжністю)
- **RR:** Zone A ≈ **1:6** (SL 18p → TP2), Zone B ≈ **1:2.9** (TP2)
- **Lot:** Zone A `100 / (18 × $10) ≈ 0.55 lot`; Zone B `100 / (32 × $10) ≈ 0.31 lot` (GBPUSD: 1 pip = $10/lot — перевірити брокер OANDA)

## 📊 Підсумок
- **Setup score: 7/10** — HTF bull узгоджений W/D/H4, GBP relative strength (SMT bull), news чисто, Asia range визначено, ASR-long дає тісний SL + великий RR. Мінус: тригер ще не відбувся (pre-London), ціна в середині структури — потрібне підтвердження свіп+reclaim на London open.
- **Recommended playbook:** `asr-orb-intraday-system` (ASR — Asia Sweep & Reclaim). GBPUSD — core ASR-пара. Напрямок: LONG.

**Коментар:** Інтрадей, закриття до 17:45 Київ. Найкраще вікно — London KZ (07:00–08:00 UTC) + NY KZ. TP2 1.35582 досяжний за трендовий London/NY день. Чекати London-реакцію на Asia range: пріоритет — лонг на reclaim Asia low або пробій-ретест Asia high. Контр-шорт лише при явному rejection Asia high з CHoCH.
