---
title: "Trading — реєстр ADR"
date: 2026-09-07
tags: [trading, adr, index]
category: adr
project: trading
status: active
aliases: ["adr-trading-index", "Реєстр рішень trading"]
pinecone_indexed: false
---

# Trading — реєстр архітектурних рішень (ADR)

> Кожне рішення, що впливає на правила ризику, статуси стратегій або конструкцію пайплайну, фіксується окремим файлом за шаблоном `~/MyVault/templates/Project-Decision-ADR.md`.
> Сесійні нотатки посилаються сюди wiki-лінком замість inline-таблиці рішень.

| Дата | ADR | Суть | Статус |
|------|-----|------|--------|
| 2026-10-08 | [[decisions/2026-10-08-no-breakeven-stop]] | **Беззбиток не ставиться**: стоп після входу не рухається до SL/TP. Підстава — шорт EURUSD 08.10 переніс стоп у БУ на 2.11R, знято о 08:15 у 0R, початковий стоп не брали (запас 1.1 п), далі MFE 4.46R | accepted |
| 2026-09-16 | [[decisions/2026-09-16-ab-swing-exception-rule-0]] | AB Storyline отримує **іменний виняток із Правила 0** (intraday only) і переноситься на swing (X=D1, SL-якір H4). Крок 0 інтрадей — FAIL, Крок 0-B swing — PASS (RR медіана 3.66, 2.8 сетапів/міс). Виняток не поширюється на інші ТС | accepted |
| 2026-09-07 | [[decisions/2026-09-07-min-rr-ta-status-playbook]] | `Min RR 1.8` не змінювати (зафіксувати рішенням, не мовчанням); `smc-price-action-combo` лишається `active`; `daily-start` опційний; тікет «TP = найближчий H1 OB» — високий пріоритет | accepted |

## Умовні позначення

- **accepted** — чинне рішення
- **superseded** — замінене пізнішим ADR (поле `superseded_by` у frontmatter)
- **deprecated** — скасоване без заміни

## Пов'язані

- [[10-Work/Projects/trading/project-overview]]
- Сесії: `10-Work/Projects/trading/sessions/`
