---
title: "Проект: BET — створення системи прогнозів і аналізу"
date: 2026-06-15
tags: [BET, work, session]
category: session
project: BET
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії
Структурувати ставки/прогнози в `/Users/serhiin/BET`: зберігати прогнози, звіряти
з результатами, аналізувати помилки, використовувати для майбутніх прогнозів.

## Рішення (вибір користувача)
| Питання | Вибір |
|---|---|
| Що трекаємо | Тільки точність прогнозів (win-rate, без грошей/ROI) |
| Формат | Гібрид: markdown прогнози + CSV-леджер |
| Зв'язок з vault | `BET/` — головне джерело правди, vault для нотаток |

## Виконано
- Створено структуру `/Users/serhiin/BET`: `predictions/`, `results/`, `ledger/`,
  `analysis/`, `scripts/`, `templates/` + `README.md`.
- `ledger/picks.csv` — 85 виборів залито з vault-прогнозів (60×1X2 + топ доп.ринки + 12 коеф-подій), усі `status=pending`.
- `ledger/accas.csv` — 5 експресів.
- `scripts/reconcile.py` — рахує win-rate загальний і по зрізах (ринок/впевненість/турнір/джерело) + acca hit-rate → `analysis/stats.md`. Перевірено sanity-тестом (2/3=66.7%).
- Шаблони prediction/result/retro.

## Джерело прогнозів
Перенесено з vault: `~/MyVault/BET/2026-06-15-wc2026-prognozy.md` та `-prognoz-z-koef.md`.

## Наступні кроки
- Внести реальні рахунки зіграних матчів у `results/...` + `status`/`actual` у `picks.csv`.
- Уточнити дати 12 коеф-подій (зараз порожні).
- Доп. ринки залито лише топ-вибори — за потреби добити повний набір (60×5).
- Після вибірки — перша ретроспектива за шаблоном `templates/retro.md`.

## Пов'язані
- [[2026-06-15-wc2026-prognozy]]
- [[2026-06-15-wc2026-prognoz-z-koef]]
