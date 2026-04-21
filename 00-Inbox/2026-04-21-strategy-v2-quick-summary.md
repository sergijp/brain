---
title: "Quick Summary: SMC Strategy v2 — план розширення"
date: 2026-04-21
tags: [trading, strategy, summary, smc, v2]
category: trading
status: draft
pinecone_indexed: false
---

# 🚀 SMC Strategy v2 — коротке саммарі

**Повна сесія:** [[10-Work/Projects/trading/sessions/2026-04-21-strategy-v2-planning]]
**План впровадження:** `~/.claude/plans/joyful-twirling-yeti.md`

## 🎯 Що додали до стратегії

### Нові моделі входу (7 замість 1)
1. **Classic BOS retest** (v1)
2. **Delayed Entry** — чекати POI через alert
3. **Inner FVG after LTF BOS** — tighter SL, кращий RR
4. **AMD / Power of Three** — Asian range → KZ Judas sweep → distribution
5. **Breaker Block** — пробитий OB як entry у напрямку пробиття
6. **Silver Bullet** — 10:00-11:00 NY FVG fill
7. **London Reversal** — 10:00 UTC Judas-sweep

### Scoring profiles (3 режими)
| Профіль | A-setup (1%) | B-setup (0.5%) | Коли |
|---------|--------------|----------------|------|
| Conservative | ≥9 | 7-8 | Drawdown recovery, нова модель |
| Standard | ≥8 | 5-7 | Default |
| Aggressive | ≥6 | 4-5 | Trending market, high-conviction |

### Risk management (4 нових правила)
- Spread/commission у R (`cost_R` -0.1R)
- Trailing SL: TP1→BE, TP2→TP1, between — 15m swing
- Dynamic sizing: 3L → 0.5%, 2W → 1%, daily DD 3% → стоп
- Correlation table: другий скорельований = 0.5%

### Process (4 ритуали)
- Pre-trade 6-point checklist
- Daily bias log (NY close)
- Psychology gate "AM I CALM?"
- Weekly review (п'ятниця 18:00 Kyiv)

### Measurement (4 інструменти)
- Dataview dashboard (WR by pair/model/session)
- Model retirement (<40% WR на 30+ трейдів)
- Adherence tracking (ціль ≥90% full)
- A/B testing scoring profiles

## 📊 Бектест (4 етапи)
1. Manual Bar Replay 50+ трейдів
2. Pine Script `strategy()` для фільтрів
3. Paper forward 1 міс, 20+ трейдів
4. Go-live: expectancy >+0.3R, WR >40%, adherence ≥90%, DD <15%

**Timeline:** ~6-8 тижнів до go-live.

## ⏭️ Status

🔴 **План зафіксовано, не впроваджено.** Чекає команди "виконуй" для rollout.

## 🔗 Links
- [[10-Work/Projects/trading/sessions/2026-04-21-strategy-v2-planning]] — повна сесія
- [[20-Trading/Strategies/smc-price-action-combo]] — v1 (буде legacy)
