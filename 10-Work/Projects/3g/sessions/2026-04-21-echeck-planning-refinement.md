---
title: "Проект: 3g — Echeck план рефінансований (dedup, DB-lock, kill-switch)"
date: 2026-04-21
tags: [work, session, 3g, echeck, planning]
category: work
project: 3g
status: completed
pinecone_indexed: false
---

## Мета сесії

Продовження планування модуля фіскальних чеків. Перевірка покриття tasks.md, доповнення пропущених edge cases, узгодження рішень по критичних питаннях.

## Виконано

- Проаналізовано існуючий tasks.md — знайдено 8 непокритих/частково покритих проблем
- Узгоджено з користувачем 8 рішень
- Оновлено `docs/fiscal-receipts/README.md` і `docs/fiscal-receipts/tasks.md`
- Перевірено `EcheckService::createEcheck` — підтверджено що один чек на ордер, усі квитки в `products[]`, один URL
- Оновлено auto-memory `project_echeck_fiscal.md`

## Важливі рішення (ADR)

| # | Рішення | Альтернативи відкинуті |
|---|---------|------------------------|
| 1 | Guard у `OrderTicketsSold` mail (release(60) якщо `echeck_id` null) | Sync createEcheck у Portmone / email з Job |
| 2 | Shift CLOSED → release до 00:05 | Тихий return / throw в failed_jobs |
| 3 | `DB::lockForUpdate` на orders при створенні чеку | Unique-job пакет / SELECT FOR UPDATE вручну без transaction |
| 4 | Частково-checked ордер — документувати як "момент першого dispatch" | Відкладений dispatch / додавати tickets у існуючий чек |
| 5 | Feature-тести: T2.1 + T3.1 | Тільки smoke |
| 6 | Telegram на failed — НЕ потрібно | Додавати нотифікацію |
| 7 | Старі "неправильні" чеки — НЕ чіпаємо | Artisan audit command |
| 8 | env `ECHECK_ENABLED` kill-switch | Тільки members.echeck_enabled |
| 9 | SMS на всі унікальні телефони ордера (автоматика) + тільки обраний ticket (ручна) | Один телефон з ordered ticket |
| 10 | Portmone email: варіант B2 — `delay(5min)` + guard в mail | B1: dispatch email з Job |
| 11 | Dedup SMS: колонка `orders.echeck_sms_sent_at` (варіант B) | Варіант C: окрема таблиця echeck_sms_log |

## Проблеми й як вирішили

- **Race email без PDF** → guard release(60) в mail до 10 спроб, потім Log::warning і пропускає
- **Race між 2 воркерами** → DB lock на рядку orders під час createEcheck
- **Shift вікно 23:59→00:00** → release(until tomorrow 00:05)
- **SMS двічі (ручна потім автоматика)** → нова колонка `echeck_sms_sent_at`, автоматика перевіряє і виставляє, ручна ігнорує
- **Тести не покриті в плані** → додано T2.1 (Job) і T3.1 (endpoint) з переліком кейсів

## Відкриті питання (parked)

- **Хто отримує SMS при автоматиці?** усі телефони ордера чи тільки тих, чиї квитки в `includedInEcheck`? Узгодити перед імплементацією T2.

## Артефакти

- `docs/fiscal-receipts/README.md` — додана секція "Правило dedup SMS", "⚠️ Відкрите питання", оновлено flow Job з dedup і DB lock, failure modes таблиця розширена
- `docs/fiscal-receipts/tasks.md` — додано T0 (міграція), T2.1 (тести Job), T2.2 (kill-switch config), T3.1 (тести endpoint), T7.1 (mail guard); розширено T2 (dedup, lock, multi-SMS), T8 (детальна таблиця логів)
- `~/.claude/projects/-Users-serhiin-Data-Source-3g/memory/project_echeck_fiscal.md` — повністю переписано під новий стан плану

## Пов'язані нотатки

- [[2026-04-21-echeck-fiscal-receipts-review]] — первинний аналіз і перший план