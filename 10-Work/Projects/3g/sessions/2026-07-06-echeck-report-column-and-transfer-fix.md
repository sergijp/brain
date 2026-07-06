---
title: "Проєкт: 3g — Echeck-звіт: колонка echeck_id + фікс зникнення трансферних квитків"
date: 2026-07-06
tags: [3g, work, session, echeck, reports, transfer-tickets]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

# Echeck-звіт: колонка echeck_id + фікс зникнення трансферних квитків

## Мета сесії
1. Додати новий стовпчик **echeck_id** до нового типу звітів **echeck** (`admin/reports`). Значення = поле `fiscalId` з JSON `echeck_answer`, що зберігається в `Order`.
2. Розібратися, чому в звітах пасажир, який має два квитки на різні рейси (трансферний + звичайний), виводиться лише з **одним** квитком.

## Виконано

### 1. Колонка `echeck_id` в echeck-звіті
- Echeck-звіт — це **не окремий Resource з фронтенд-колонками**, а Excel-export клас, що віддає і `.xlsx`, і прев'ю. Фронтенд (`ReportForm.vue`) рендерить прев'ю generic-но (заголовок = перший рядок) → **фронтенд змінювати не треба**, нова колонка з'являється автоматично.
- Додано заголовок `__('crud.echeck_id')` та дані після `payment_type` у `EcheckTicketsExport`.
- `fiscalId` дістається **null-safe** через приватний helper, який не залежить від Eloquent-касту:
  ```php
  private function echeckFiscalId($echeckAnswer): ?string
  {
      $data = is_array($echeckAnswer) ? $echeckAnswer : json_decode((string) $echeckAnswer, true);
      return is_array($data) ? data_get($data, 'fiscalId') : null;
  }
  ```
- N+1 немає — `order` вже eager-loaded у `ReportsController::getTickets()`.
- Переклад `echeck_id => 'Фіскальний номер'` додано в `lang/uk/crud.php` і `lang/en/crud.php`.

### 2. Фікс зникнення трансферного квитка (echeck-звіт)
- Корінь — фільтр у `ReportsController::getTickets()` (рядки 183-189), який був dedup-фільтром трансферів:
  - лишав тільки: **A** (parentTicket + `is_transfer=true`) або **B** (без parent + `is_transfer=false`);
  - дропав: **C** (без parent + `is_transfer=true`) і **D** (parent + `is_transfer=false`).
- **Реальні дані по двох номерах** (read-only SELECT):
  - `0806260951297117` (id 141691): `parent_id=NULL`, `is_transfer=0` → стан **B** → показувався;
  - `080626095122075` (id 141693): `parent_id=141691`, `is_transfer=0` → стан **D** → **зникав**.
- Зниклий = **child-сегмент трансферу**, створений через `BookingService::bookTransfer()`: ставиться `parent_id`, але `is_transfer` лишається `0` (default в `Order.php:104`).
- **Масштаб (агрегат БД):** стан D — **21 493 рядки** (домінантний механізм трансферів), стан A (під який писався фільтр) — лише **11 рядків**. Фільтр писався під рідкісний випадок.
- **Фікс (тільки для echeck):** обгорнули весь dedup-`where` у `->when(! $onlyEcheck, ...)`. `$onlyEcheck` — наявний 6-й параметр `getTickets()`, echeck-звіт ідентифікується через `type_report=echeck` → `buildExport()` → `getTickets(..., $onlyEcheck=true)`.
  - Інші звіти (`default`, `qr`) — поведінка **байт-у-байт незмінна**.
  - echeck — dedup вимкнено, сегменти трансферу проходять, обмежені наявним echeck-фільтром (`order.echeck_id NOT NULL` + `trip_station.checked_at`). Дублів немає: сегменти трансферу — різні рейси/ордери, окремі фіскальні події.

## Важливі рішення (ADR)

| # | Рішення | Чому |
|---|---------|------|
| 1 | Читати `fiscalId` через ручний `json_decode` в export-класі, **без** Eloquent-касту на `echeck_answer` | Каст `=> 'array'` зачепив би запис/читання поля по всьому коду (`OrderController`, `SendEcheckSmsJob`). Обрали мінімальний scope — нуль впливу на інший код. |
| 2 | Фікс dedup застосувати **тільки для echeck** (`->when(! $onlyEcheck, ...)`) | Інші звіти навмисно дедуплять трансфер в 1 рядок; echeck (фіскальні чеки) має показувати кожен реально проданий сегмент зі своїм чеком. |
| 3 | Для echeck **повністю пропустити** dedup, а не додавати гілки C/D | Дані показали, що дропаються обидва стани (C=11, D=21493). Пропуск dedup — мінімальна зміна, що покриває обидва. |

## Проблеми й як вирішили
- **Хибна початкова гіпотеза (стан C):** спершу припустили, що зникає кореневий квиток трансферу (стан C). Read-only SELECT по реальних номерах спростував — насправді це стан **D** (child з `is_transfer=0`). Урок: звіряти гіпотезу реальними даними перед фіксом.
- **Ризик касту:** агент спершу додав каст `echeck_answer => 'array'` на `Order`. Відкотили за рішенням користувача — надто широкий scope.

## Артефакти

**Змінені файли (не закомічено):**
- `app/EXCELExports/Reports/EcheckTicketsExport.php` — колонка `echeck_id` + helper `echeckFiscalId()`
- `app/Http/Controllers/Api/System/ReportsController.php` — dedup-`where` (183-189) обгорнутий у `->when(! $onlyEcheck, ...)`
- `lang/uk/crud.php`, `lang/en/crud.php` — ключ `echeck_id => 'Фіскальний номер'`

**Read-only SQL для діагностики:**
```sql
SELECT id, number, trip_id, parent_id, is_transfer, status, order_id
FROM tickets WHERE number IN ('080626095122075','0806260951297117');

SELECT is_transfer, (parent_id IS NULL) AS no_parent, COUNT(*)
FROM tickets GROUP BY is_transfer, (parent_id IS NULL);
```

**Ключові точки коду:**
- `ReportsController::getTickets()` — dedup-фільтр (183-189), echeck-фільтр (~194), `$onlyEcheck` 6-й параметр
- `ReportsController::reportParams()` (~79) — `type_report`, `self::$TYPE_ECHECK`
- `BookingService::bookTransfer()` — механізм трансферу (child з `is_transfer=0`)

## Пов'язані нотатки
- [[2026-07-06-echeck-module]]
- [[2026-05-14-echeck-cash-payment]]
- [[2026-06-30-echeck-station-close-booked-bug]]
- [[2026-06-23-qr-payment-reports]]
- [[2026-05-19-busfor-api-transfer-fixes]]
