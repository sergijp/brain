---
title: "Проект: 3G — Echeck dry-run режим та SMS шаблон"
date: 2026-04-22
tags: [work, session, 3g, echeck, fiscal]
category: work
project: 3g
status: completed
pinecone_indexed: false
---

## Мета сесії

Підготувати модуль фіскальних чеків (echeck) до тестування на лайві без створення реальних чеків. З'ясувати де зберігається і як редагувати SMS шаблон.

## Виконано

| Задача | Результат |
|---|---|
| Додано `ECHECK_DRY_RUN` env + `config/services.echeck.dry_run` | `config/services.php` |
| Dry-run логіка в `SendEcheckSmsJob` | Логує рішення, пропускає реальні API-виклики і SMS |
| Оновлено `.env.example` | `ECHECK_DRY_RUN=false` |
| З'ясовано де SMS шаблон | Таблиця `settings`, ключ `echeck_sms_template` |
| Оновлено auto-memory | `~/.claude/projects/.../memory/project_echeck_fiscal.md` |

## Важливі рішення (ADR)

| Рішення | Чому |
|---|---|
| Dry-run через env, не через аргумент Job | Глобальне вимкнення без зміни коду; легко перемикати на сервері |
| При dry-run логується `echeck_products_ready` з повним payload | Видно точно які квитки потрапили б у чек і чому |
| При shift CLOSED у dry-run — НЕ робить `release()` | Інакше б job завис у черзі; dry-run просто логує і виходить |

## Dry-run логи (що з'являється в `storage/logs/echeck.log`)

- `echeck_dry_run_mode` — задача запустилась, ticket_id, force
- `echeck_skipped_member_disabled` — member без `echeck_enabled` (раніше мовчки виходив)
- `echeck_no_included_tickets` — жоден квиток не пройшов фільтр (з усіма ID ордера)
- `echeck_products_ready` — повний payload чеку (ціна, статус, податок)
- `echeck_dry_run_skip_create` — замість реального API-виклику
- `echeck_dry_run_would_sms` — кому б пішли SMS (замасковані телефони, імена)

## SMS шаблон — де редагувати

Таблиця `settings`, ключ `echeck_sms_template`. **Запис ще не існує в БД** — є fallback у коді:
```
Шановний [client], Ваш фіскальний чек: [link]
```

Змінні: `[client]` = full_name, `[link]` = URL чеку.

Щоб з'явився в адмінці (`/settings`):
```sql
INSERT INTO settings (key, value) VALUES ('echeck_sms_template', 'Шановний [client], Ваш фіскальний чек: [link]');
```

## Як тестувати на лайві

```bash
# .env на сервері:
ECHECK_ENABLED=true
ECHECK_DRY_RUN=true

# Слідкувати за логом:
tail -f storage/logs/echeck.log
```

## Артефакти

- `config/services.php` — додано `dry_run`
- `app/Jobs/Echeck/SendEcheckSmsJob.php` — dry-run логіка
- `.env.example` — `ECHECK_DRY_RUN=false`

## Pending

- [ ] T9 — ручний smoke test на staging (`queue:work`, сценарії A/B/C, PDF у email)
- [ ] Вставити `echeck_sms_template` в таблицю `settings` (seeder або міграція)

## Пов'язані нотатки

- [[3g/project-overview]]
- [[3g/sessions/2026-04-22-echeck-implementation]] (попередня сесія — T0-T10)