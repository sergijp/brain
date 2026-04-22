---
title: "Correlation Table — Watchlist + Розподіл Ризику"
date: 2026-04-22
tags: [trading, correlation, risk-management, watchlist, v2]
category: trading
status: active
pinecone_indexed: false
---

# 🔗 Correlation Table — Watchlist v2

**Джерело коефіцієнтів:** TradingView "Correlation Coefficient" indicator (period 50, D1), середнє за 2023-2025.
**Правило:** Коефіцієнти перевіряти щоквартально (режими змінюються — напр. XAU/DXY може послаблюватись у ризикових фазах).

---

## 🧭 Як користуватись

1. **Перед входом** — дивись чи вже відкритий скорельований трейд.
2. Якщо |ρ| ≥ 0.7 у ту саму сторону ризику → **другий = 0.5% risk** (замість 1%)
3. Якщо |ρ| ≥ 0.85 → **не беремо другий зовсім** (надмірна концентрація)
4. Якщо ρ ≈ 0 або навіть негативна → два повноцінні 1% — OK (диверсифікація)
5. Якщо ρ високо негативна і трейди у **протилежних** сторонах → ефективно це **ТОЙ САМИЙ** ризик (напр. short EURUSD + long DXY = одне й те ж) → max 1% сумарно

---

## 📊 Основні кореляції (forex + metals + indices)

| Пара A | Пара B | ρ (середнє) | Трактування | Правило ризику |
|--------|--------|-------------|-------------|----------------|
| EURUSD | GBPUSD | **+0.85** | Майже дзеркало (обидва vs USD) | Other = 0.5%, НЕ брати третій |
| EURUSD | USDCHF | **-0.92** | Сильно обернено | Same-direction = skip (один ризик) |
| EURUSD | DXY | **-0.95** | Практично інверсія | Skip — це той самий трейд |
| EURUSD | AUDUSD | **+0.70** | Загальний USD-фактор | Other = 0.5% |
| GBPUSD | AUDUSD | **+0.72** | Риск-он/офф спільне | Other = 0.5% |
| USDJPY | US10Y yields | **+0.80** | Rates-driven | Other = 0.5% |
| USDJPY | Nikkei | +0.55 | Помірна | 1% OK |
| USDCAD | WTI Oil | **-0.75** | Oil drives CAD | Same-direction trades = skip |
| XAUUSD | DXY | **-0.70** | Класична inverse | Same-direction trades = skip |
| XAUUSD | US10Y real yields | **-0.80** | Opportunity cost | Skip-if-aligned |
| XAUUSD | XAGUSD | **+0.85** | Metals beta | Silver = 0.5%, НЕ третій metal |
| XAUUSD | EURUSD | +0.60 | Anti-USD загальне | 1% OK (не надто тісно) |
| GER40 | US500 | **+0.80** | Global equity risk-on | Other = 0.5% |
| US100 | US500 | **+0.90** | Дуже тісно | Other = 0.5%, НЕ третій index |
| GER40 | EURUSD | +0.40 | Слабка | 1% OK |

**Легенда:**
- **Жирний** (|ρ| ≥ 0.7) — активне обмеження ризику
- Звичайний — моніторинг, зазвичай не блокує

---

## 🧮 Алгоритм перед входом

```
setup_ready(pair_B, direction_B):
    for pair_A in open_trades:
        rho = lookup_correlation(pair_A, pair_B)
        risk_aligned = (direction_A == direction_B and rho > 0) or
                       (direction_A != direction_B and rho < 0)

        if risk_aligned:
            if abs(rho) >= 0.85:
                → SKIP (занадто концентровано)
            elif abs(rho) >= 0.70:
                → risk_B = 0.5%  (замість 1%)
        else:
            # фактично disersifying
            → 1% OK

        if total_correlated_exposure > 2%:
            → SKIP (hard cap)
```

---

## 🚨 Hard Caps (сумарні)

| Метрика | Ліміт |
|---------|-------|
| Max одночасних трейдів | 3 |
| Max сумарний risk | 2% рахунку |
| Max трейдів на одному USD-стороні (long USD або short USD) | 2 |
| Max трейдів на metals | 1 (gold + silver = беремо один) |
| Max трейдів на indices | 1 (S&P + NAS + DAX — один) |

---

## 🔄 Quarterly Review

Оновлювати таблицю наприкінці кожного кварталу:
1. Вивантажити корелят. коеф. з TradingView (period 50, D1) на останні 90 днів
2. Порівняти з попереднім кварталом — flag changes |Δρ| > 0.15
3. Якщо режим змінився (напр. XAU-DXY кореляція слабшає) → переглянути правила

**Останнє оновлення:** 2026-04-22 (ініціальне)
**Наступне планове:** 2026-07-01

---

## 🔗 Пов'язані

- [[Strategies/smc-playbook-v2]] — сек. "Risk Management" (A5 Correlation)
- [[Checklists/pre-trade-checklist]] — Hard Blocker "Correlation cap"
- [[Backtest/template-backtest-trade]] — поле `risk_usd` відображає розподіл (1% vs 0.5%)
