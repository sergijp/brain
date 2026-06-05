---
title: "mono-system — Додавання фільтрів на сторінці Reports"
date: 2026-06-05
tags: [mono-system, work, session, reports, excel, filters]
category: session
project: mono-system
status: done
aliases: [mono-system-reports-filters-2026-06-05]
pinecone_indexed: false
---

## Мета сесії

Додати два нові фільтри на сторінці Reports:
1. Мультиселект статусів квитків (`status`)
2. Мультиселект статусів явки (`status_ticket`)

При застосуванні фільтри мають впливати на вміст згенерованого Excel-файлу.

## Виконано

| Задача | Результат |
|--------|-----------|
| Додано мультиселект статусів квитка у `ReportForm.vue` | ✅ |
| Додано мультиселект статусів явки (`status_ticket`) у `ReportForm.vue` | ✅ |
| Передача нових параметрів `statuses` і `status_tickets` у payload | ✅ |
| Фільтрація по `statuses` у `ReportsController::getTickets()` | ✅ |
| Фільтрація по `status_ticket` у основному запиті | ✅ |
| Фільтрація по `status_ticket` у UNION-частині (повернені квитки) | ✅ |

## Важливі рішення

| Рішення | Причина |
|---------|---------|
| Статуси квитка (`status`) — мультиселект, якщо порожньо — дефолтний набір | Не ламає існуючу поведінку |
| Явка — поле `status_ticket`, мультиселект | Спочатку розглядалось `checked` (bool), але правильне поле — `status_ticket` |
| `!is_null()` замість `count()` не використовується | `status_ticket` — масив, тому `count()` правильно |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| `Undefined variable $statusTicket` (двічі) | В UNION-частині запиту залишився старий `$statusTicket` — виправлено вручну, `replace_all` пропустив через різний відступ |
| `Undefined variable $checked` | Аналогічно — залишок після перейменування в UNION-блоці |

## Артефакти

- `resources/js/components/reports/ReportForm.vue` — +2 v-select, +нові data-поля, оновлений payload
- `app/Http/Controllers/Api/System/ReportsController.php` — `getTickets()`: +2 параметри, +2 `->when()` в основному запиті та UNION

## Статуси у селектах

**Статус квитка (`status`):** sold, booked, returned, prebooked, cancelled, annulled

**Статус явки (`status_ticket`):** showed_up, not_showed_up, planned, postponed, cancelled, canceled, bought_office, handset_up, handset_not_up
