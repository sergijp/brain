---
title: "Narrative Log — денний шаблон"
date: 2026-09-16
tags: [trading, checklist, narrative-layer, journal]
category: trading
status: active
pinecone_indexed: false
---

# Narrative Log — денний запис

Заповнюється **щодня до відкриття London**, навіть якщо торгувати не плануєш.
Два останні поля дописуються **після 19:00 UTC**.

```yaml
date: 2026-09-__
pair: EURUSD

# --- до сесії
narrative_A: ""          # на що ціна реагує зараз: "D1 [+SNR] 1.0840"
narrative_B: ""          # КУДИ: "W1 Fractal High 1.1020"  | null якщо немає
direction: none          # long | short | none
why: null                # теза: чому ціна несправедлива. null якщо немає
market_state: expansion  # expansion | overextension | compression
verdict: SKIP            # GO | WARN | SKIP

# --- після сесії (обов'язково, навіть без трейду)
ts_traded: none          # ts-2 | ts-3 | ns | none
outcome_R: null
day_available_move: 0.0  # max(hi−open, open−lo) 07:00→19:00 UTC, у пунктах
b_reached: null          # true | false | null (якщо B не заявлялась)
```

## Як заповнювати

**`narrative_B`** — найважливіше поле. Якщо не можеш назвати конкретний рівень — пиши `null` і `verdict: SKIP`. «Подивимось по ходу» = `null`.

**`why`** — одна фраза, чому поточна ціна несправедлива. Не «бо SNR», а «ринок переоцінює ймовірність підвищення ставки». Немає тези → `null` → `verdict: WARN`, але торгувати можна.

**`market_state`** — рахується механічно з учорашнього дня:
- діапазон вчора > 1.5 × ATR_D(14) → `overextension`
- вчора inside day **або** (ATR_D < медіани за 60 дн **і** діапазон вчора < 0.7 × ATR_D) → `compression`
- решта → `expansion`

> ⚠️ Стан **нічого не блокує** — теза першоджерела спростована на 423 днях ([[nl-market-state-2026-09-16]]). Поле логується, щоб перевірити на більшій вибірці.

**`b_reached`** — чи ціна торкнулась заявленої B до 19:00 UTC. Це **головна метрика шару**: рішення на 60-му дні приймається саме по ній.

**`day_available_move`** і **`b_reached`** заповнюються і в `SKIP`-дні. Інакше не буде з чим порівнювати — фільтр, який не рахує, що відрізав, завжди виглядає корисним.

## 🔗

- [[narrative-layer]] — специфікація шару
- Журнал: `20-Trading/Journal/narrative-log.md`
