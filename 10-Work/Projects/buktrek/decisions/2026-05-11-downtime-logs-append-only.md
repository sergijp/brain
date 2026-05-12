---
title: "ADR-2026-05-11 — append-only downtime_logs замість полів на Application"
date: 2026-05-11
tags: [buktrek, adr, downtime]
category: adr
project: buktrek
status: accepted
aliases: ["adr-buktrek-downtime-logs-append-only"]
pinecone_indexed: false
---

# ADR-2026-05-11 — append-only `downtime_logs` замість полів на `Application`

**Status:** accepted
**Date:** 2026-05-11
**Стейкхолдери:** sergijp (тех. рішення на основі use-case)

## Контекст

V1 реалізації лімітів простою (комі­т `f948ce4`) рахувала "використання" безпосередньо з полів `applications.downtime_started_at` / `applications.downtime_hours_proposed`. Сервіс `DowntimeUsageService`:

```sql
SELECT hours, COUNT(*) FROM applications
WHERE driver_id = X
  AND downtime_started_at >= NOW() - INTERVAL 14 DAY
GROUP BY downtime_hours_proposed;
```

**Виявлений обхід:** у `MemberController::setStep()` поля `downtime_started_at` і `downtime_hours_proposed` обнуляються при будь-якій зміні статусу. Сценарій:

1. Водій → `POST /set-downtime hours=45` → ліміт 45h ВИЧЕРПАНО.
2. Водій → `POST /set-step step=in_road` → `downtime_started_at = NULL`.
3. Сервіс знову бачить 0 використань → ліміт 45h ВІЛЬНИЙ.
4. Водій знову може взяти 45h в той самий день.

Це порушувало бізнес-правило "1×45h за 14 днів".

## Рішення

Створити окрему **append-only таблицю `downtime_logs`** — журнал кожного епізоду простою. Сервіс рахує ліміти з неї, поля на `Application` зберігаються лише для існуючого UI ("поточний простій").

Структура:
```
downtime_logs(
  id, driver_id, member_id, application_id, hours,
  started_at, released_at, released_by_step,
  created_at, updated_at
)
```

- INSERT — у `MemberController::setDowntime` (всередині `DB::transaction`).
- UPDATE `released_at`+`released_by_step` — у `MemberController::setStep` (тільки open-лог цієї заявки).
- DELETE — не виконується з продакшен-коду.

## Альтернативи (відкинуті)

| Варіант | Чому відкинули |
|---------|----------------|
| **Залишити підрахунок з `applications` + заборонити `setStep` обнуляти поля при скасуванні простою** | Ламає існуючий UI: DriverStatusDowntimeField на фронтенді бачить заявку як "у простої" поки `downtime_started_at != NULL`, незалежно від `driver_status`. Це довелося б рефакторити в декількох Vue-компонентах. |
| **Soft-delete поля replays через `deleted_at` на applications** | applications вже має `SoftDeletes` — конфлікт семантик. Поля простою — окрема історія. |
| **Зберігати `downtime_history` як JSON-колонку на Application** | Незручно для агрегацій (треба JSON_EXTRACT), нема індексів, неструктуроване. |
| **Окрема таблиця тільки для випадку перевитрат (логувати лише зловживання)** | Робить аналітику складною ("чому вирахувано Х, а в логах Y?"), не дає звітів типу drivers-downtime. |

## Наслідки

**Позитивні:**
- Чесний 14-денний підрахунок — скасування не повертає ліміт.
- Розблоковано аналітику: можна показати "хто простоює зараз", "сумарні години за тиждень", "коли водій скасував і чому".
- Динаміка по годинам (додання нового набору в `downtime_limits` не потребує SQL-правок) працює і для лімітів, і для звітів.
- Open-лог (`released_at IS NULL`) — природний source-of-truth для "активних простоїв" на дашборді.

**Негативні / трейдофи:**
- Дублювання даних: `applications.downtime_started_at` синхронізується з `downtime_logs.started_at`. Якщо одне з двох оновиться без іншого (баг або ручний UPDATE) — розсинхрон.
- Додаткова транзакція (`DB::transaction`) у `setDowntime`/`setStep`. Для нашого трафіку — несуттєво.
- Закриття open-логу при `setStep` робиться через `ORDER BY id DESC LIMIT 1` — якщо інваріант "один open per application" порушено, закриється тільки найновіший, інші залишаться "висіти". Інваріант поки не fence-d на рівні унікального індексу — потенційний follow-up.

## Follow-up (поки не зроблено)

- Унікальний партіальний індекс `WHERE released_at IS NULL` на `(application_id)` — MySQL не підтримує partial indexes; може робитись через тригер або генерована колонка.
- Якщо потрібно — наприкінці місяця прибрати поля `applications.downtime_started_at` / `downtime_hours_proposed` після рефакторингу UI на `downtime_logs`.
- Cron/cleanup для дуже старих логів (>1 рік) — поки не пріоритет.

## Пов'язані

- [[10-Work/Projects/buktrek/docs/downtime]]
- [[10-Work/Projects/buktrek/sessions/2026-05-11-downtime-limits-and-dashboard-reports]]
