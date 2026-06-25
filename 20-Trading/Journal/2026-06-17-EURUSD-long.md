---
title: "EURUSD LONG — override paper-трейд (SMC/AMD, поза ASR)"
date: 2026-06-17
time_kyiv: "15:36"
time_utc: "12:36"
tags: [trading, journal, eurusd, smc-amd, risk-override, paper]
category: trading
pair: EURUSD
direction: long
strategy: discretionary-smc-amd
status: closed   # planned → open → closed
agent: journal-writer
risk_override: true
override_reason: "Команда dixie⇄kassandra радила SKIP (ASR F1 FAIL — вузький Asia range; RR на досяжних цілях ~1:1). Користувач свідомо взяв override як paper-трейд на демо-чарті."
paper: true
chart_position_id: "9jg9bX"
pinecone_indexed: false
---

# EURUSD LONG — 2026-06-17

> ⚠️ Risk override applied: команда dixie⇄kassandra радила SKIP (ASR дав F1 FAIL — вузький Asia range; RR на реально досяжних цілях ~1:1). Взято свідомо як **paper-трейд** на демо-чарті (серед 5 інших паперових позицій). Це **discretionary SMC/AMD сетап ПОЗА системою ASR**.

## Plan

| Field | Value |
|-------|-------|
| Entry | 1.16090 (retest-зона після AMD reclaim) |
| SL | 1.16028 (-6.2 pips, під swing low 1.16038) |
| TP1 | 1.16140 (+5.0 pips) |
| TP2 | 1.16175 (+8.5 pips) |
| TP3 | 1.16221 (+13.1 pips, тижнева BSL) |
| Lot | paper / демо (розмір не фіксується) |
| Risk | paper — реальний депозит не задіяний |
| RR planned | до TP3 ~1:2.1; на досяжних цілях ~1:1 |
| Strategy | discretionary SMC/AMD (поза [[Strategies/asr-orb-intraday-system]]) |
| Chart position id | 9jg9bX |

## Why

Логіка входу (discretionary, поза ASR):
- AMD-схема: accumulation → manipulation (sweep low) → distribution; вхід у retest-зоні після reclaim.
- Entry 1.16090 на ретесті після reclaim; SL 1.16028 під swing low 1.16038.
- Цілі: TP1 1.16140, TP2 1.16175, TP3 1.16221 (тижнева BSL як магніт).
- Це 3-й EURUSD-long того ж патерну за місяць (див. розділ для retro).

## Risk check

- Day risk used: 0% (paper-трейд, реальний депозит не задіяний)
- Correlation: n/a (демо, не входить у open_positions)
- News: НЕ CLEAR — насичений новинний день (деталі нижче). Команда дала SKIP/BLOCK.
- Session: London KZ / NY — вхід у робочому вікні, але новинний фон проти сетапу.
- Verdict команди: **SKIP / BLOCK** → користувач узяв **override** (paper).

## Kassandra challenge (resolved)

Конвергенції НЕ було — команда радила SKIP. Ключові претензії Kassandra:
1. **RR ілюзорний**: до TP3 ~1:2.1, але реально досяжні цілі (TP1/TP2) дають ~1:1 — нижче min RR 1.8.
2. **ASR неактивна сьогодні** — F1 FAIL (вузький Asia range), сетап поза основною системою.
3. **Повторюваний патерн**: 3-й EURUSD-long того ж типу за місяць (07.05, 12.05, 17.06) — попередні не спрацьовували чисто.
4. **Новинний ризик**: щільний календар (CPI×2, Lagarde, US Retail Sales, FOMC попереду).

**Висновок:** користувач прийняв ризик свідомо як демо-експеримент, щоб перевірити патерн форвардом. Команда залишилась при SKIP.

## Links

- Analysis: [[Analysis/2026-06-17/EURUSD-analysis]]
- Strategy (основна, дала SKIP): [[Strategies/asr-orb-intraday-system]]
- Попередні того ж патерну: [[Journal/2026-05-07-EURUSD-long]], [[Journal/2026-05-12-EURUSD-long-paper]]

## Execution log

- [x] Opened (paper) at 1.16090 — position id 9jg9bX
- [x] TP1 1.16140 торкнуто (хай 1.16148) — часткова фіксація **можлива** (керування користувача, факт фіксації не підтверджено)
- [ ] SL moved to BE — НЕ зафіксовано
- [x] Розворот вниз: DXY новий high 99.589 (інвалідація SMT-умови)
- [x] Closed: SL 1.16028 вибито (прокол низом 1.16008)

## Result (paper)

| Сценарій | Опис | Результат |
|----------|------|-----------|
| Якщо 50% знято на TP1 | +50% × ~+5пп зафіксовано, решта вибита по SL | близько до **BE / малий мінус** |
| Якщо TP1 НЕ фіксувалось | вся позиція вибита по SL | **повний −1R** |

> Чесна примітка: підсумок залежить від того, чи фіксувалась TP1 (ручне керування користувача). Факт часткового виходу на TP1 у джерелі **не підтверджено** — тому фіксую обидва сценарії, без єдиної цифри P&L.
>
> Сетап провалився **як і прогнозувала команда** (SKIP). Тег: #risk-override.

## Lessons (post-trade — для retro)

1. **Повторюваний патерн (3× за місяць)** — EURUSD-long того ж типу:
   - **07.05** — били за широкий SL, конвергенція тільки на tight-варіанті.
   - **12.05** — BLOCK через SMT → пішло у paper.
   - **17.06** — сьогодні, override → провал.
   - Kassandra прямо вказала на цей повторюваний патерн у дебаті. **Сигнал для retro: переглянути доцільність цього патерну на EURUSD-long.**
2. **Неповний новинний календар** — news-watcher вранці НЕ включив **Lagarde 13:50** та **EU CPI 12:00**. Календар був неповний → урок: перевіряти ForexFactory повторно перед входом у новинні дні.
3. **Новинний фон дня (для контексту):**
   - GBP CPI 09:00 — 2.8% (dovish)
   - EU CPI 12:00 — 3.2% (in-line) *(не було у ранковому звіті)*
   - Lagarde 13:50 — без реакції *(не було у ранковому звіті)*
   - US Retail Sales 15:30 — сильні 0.8% / 0.9% (але EUR проігнорував, не впав)
   - FOMC 21:00 — ще попереду
4. **Інвалідація через DXY**: новий high DXY 99.589 зламав SMT-умову — сигнал на негайний вихід був раніше, ніж спрацював SL.
5. **Override-дисципліна**: команда дала SKIP/BLOCK, результат негативний — підтверджує цінність risk-gate. Override виправданий лише як свідомий paper-експеримент, не на реальному рахунку.
