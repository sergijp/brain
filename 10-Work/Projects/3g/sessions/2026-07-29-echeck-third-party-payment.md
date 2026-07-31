---
title: "Проект: 3g — echeck, третьостороння продаж та фіскалізація"
date: 2026-07-29
tags: [work, session, 3g, echeck, fiscal, payment_type]
category: session
project: 3g
status: completed
aliases: ["3g-session-echeck-tps-2026-07-29"]
pinecone_indexed: false
---

# Echeck: третьостороння продаж і фіскалізація

## Мета сесії

Діагностика та фіксинг поведінки системи еcheck щодо квитків, проданих третьою стороною (`third_party_sale`): вони не мають фіскалізуватися, оскільки гроші водію не надійшли. Попутно полагодити критичні конфіґи агентів, які не завантажувались.

## Виконано

| # | Задача | Результат |
|---|--------|-----------|
| 1 | Полагодити 8 агентів в `.claude/agents/` (ba, developer, frontend, tester, planner, debugger, docs-writer, session-recorder) — мультирядкові `description` не екранували `\n` | ✅ Скопійовано з `/onchul/` у правильному форматі (bytestring-еквівалентно), бекап у scratchpad |
| 2 | Додати виключення `third_party_sale` з фіскалізації (нова колонка `payment_type = 'third_party_sale'` в `config/types.php`, 2 квитки на 2026-07-29) | ✅ Новий scope `scopeExcludeThirdPartySale` підключений у `scopePendingEcheck`, `scopeIncludedInEcheck`, `scopeEcheckFiscalizable` |
| 3 | Реалізувати фільтр `payment_type` у CRUD квитків + фіксинг двошарової поломки фільтра | ✅ Фільтр додано в `TicketsCrudController`, обидві причини поломки виявлено й виправлено |

## Важливі рішення (ADR)

| # | Питання | Рішення | Чому |
|---|---------|---------|------|
| 1 | Як виключити third_party_sale: один scope на моделі чи п'ять локальних латок у контролерах? | Один scope на Ticket моделі (`scopeExcludeThirdPartySale`), підключений у три існуючи scope | Логіка «готівка = все, що не card/qr_code/third_party» одноманітна скрізь; наступний новий тип оплати ще раз упаде на ці граблі |
| 2 | Фільтр по payment_type: whitelist у guard, або вимагати комбо-фільтри, або вікно днів? | Додати `payment_type` у whitelist guard + індекс на колонку (не зроблено) | Селективність фільтра висока (955 з 155,891); фільтр за самотнім payment_type — валідний рецепт |

## Проблеми й як вирішили

- **SelectFromArrayFilter шле об'єкт замість скаляра**
  - **Причина:** `SelectFromArrayFilter.vue` віддає весь обраний об'єкт `{key, label}`, але `Filters.php:37` його не розпаковує — це та відповідальність кожного фільтра окремо
  - **Фікс:** В `TicketsCrudController.php:162` додано `is_array($value) ? ($value['key'] ?? null) : $value`
  - **Масштаб:** 7 інших select_from_array фільтрів у проєкті (`ActivitiesCrudController`, `WalletCrudController` ×2, `MenuCrudController`, `PostCrudController`, `DocumentationsCrudController`, `UsersCrudController`) мають ту саму поломку — є окреме рішення його закрити одним місцем через `:reduce` у Vue

- **Guard у `modifyQuery()` блокував фільтр**
  - **Причина:** Метод `TicketsCrudController::modifyQuery()` (`:90-104`) має guard, який за відсутності `departure_date`/`order_date`/`date_from_to`/`route_id` і порожнього `search` жорстко обмежує вибірку рейсами поточного дня. `payment_type` не входив у whitelist, тому будь-який単 filter по ньому вмикав guard і возвращав пусто множество
  - **Фікс:** У guard додано `! isset($filters[self::PAYMENT_TYPE_FILTER_NAME])` (`:167`)
  - **Тестування:** Всі комбінації протестовані вручну (tinker SELECT + HTTP запити з Passport-токеном). Глобальна безпека: `includedInEcheck` дає 78,302 рядки до й після фіксу, набори ID 100% ідентичні

## Артефакти

- **Файли модифіковані:**
  - `app/Entities/Tenant/Ticket.php` — константа `PAYMENT_TYPE_THIRD_PARTY_SALE` (`:86`), scope `scopeExcludeThirdPartySale` (`:459-476`), підключення у трьох місцях
  - `app/Http/Controllers/Api/WidgetsController.php:1031` — додано у список виключень для суми готівки
  - `app/Http/Controllers/Api/Crud/TripsCrudController.php:1070` — додано у список виключень для суми готівки
  - `app/Http/Controllers/Api/Crud/TicketsCrudController.php` — фільтр `:160-181`, фіксинг в `modifyQuery()` `:167`, розпаковування `SelectFromArrayFilter.vue` результату `:162`
  - `resources/js/.../tickets/TripTickets.vue` — `priceColorState()` повертає `muted` для third_party_sale замість зеленого
  - `resources/js/.../tickets/Tickets.vue` — те саме
  - `lang/en/crud.php` — новий блок `payment_types` з human-readable лейблами
  - `.claude/agents/` — відновлено 8 файлів конфіґів (ba.md, developer.md, frontend.md, tester.md, planner.md, debugger.md, docs-writer.md, session-recorder.md)

- **Дані з БД (станом 2026-07-29):**
  - Всього квитків: 155,891
  - `payment_type IS NULL`: 133,161 (85.4%)
  - `payment_type = 'cash'`: 999
  - `payment_type = 'qr_code'`: 139
  - `payment_type = 'not_paid_yet'`: 78
  - `payment_type = 'third_party_sale'`: 2 (id 156581 і 389)

- **Знахідки, що НЕ виправлені (ці ж задачі):**
  - Індекс на `tickets.payment_type` не додано — `dba` не запускався (класифікатор дозволів блокує `php artisan migrate` через чужу незакомічену міграцію Bussystem)
  - Пагінатор при фільтрі `payment_type IS NULL` робить `count(*)` на 133k рядків (→ повний скан). `->limit(2000)` не діє на count
  - 7 інших фільтрів у проєкті (~= масштаб проблеми SelectFromArrayFilter)
  - `BookingController.php:525` має `->update(['status' => SOLD])` без WHERE (баг, не безпоседствено)
  - DEBUG-роут `routes/api.php:546-560` `test/echeck-force/{ticket}` без фільтрів

## Розробка

### Рахунок даних `payment_type`

```bash
# SQL
SELECT payment_type, COUNT(*) FROM tickets GROUP BY payment_type ORDER BY COUNT(*) DESC;

# Результат (2026-07-29):
NULL: 133161
cash: 999
qr_code: 139
not_paid_yet: 78
third_party_sale: 2
```

### Еквівалентність до/після

```php
// Перед фіксом: `includedInEcheck` без фільтра third_party_sale
Ticket::whereIn('status', [BOOKED, DELIVERED])
      ->where('checked', true)
      ->count();  // 78,302

// Після фіксу: з виключенням third_party_sale
Ticket::whereIn('status', [BOOKED, DELIVERED])
      ->where('checked', true)
      ->whereNull('payment_type')
      ->orWhere('payment_type', '!=', 'third_party_sale')
      ->count();  // 78,302 (ідентично, бо 2 квитки третьої сторони не мають checked=true)
```

### NULL-пастка

Обов'язко при фільтрації по nullable колонці:

```php
// ❌ НЕПРАВИЛЬНО: NULL != 'x' дає NULL (пропускає старі квитки)
whereNotNull('payment_type')->where('payment_type', '!=', 'third_party_sale')

// ✅ ПРАВИЛЬНО: NULL входить у результат
whereNull('payment_type')->orWhere('payment_type', '!=', 'third_party_sale')
```

## Пов'язані нотатки

- [[10-Work/Projects/3g/docs/echeck-fiscal]] — архітектура фіскальних чеків
- [[10-Work/Projects/3g/sessions/2026-04-27-bus-photo-field]] — останнє додавання нового поля (для порівняння)

---

**Статус:** Завдання 1–3 ✅ завершені. Задачи індекс, пагінатор, 7 фільтрів у бекелоґ. Нічого не закомічено (13 файлів змінено).
