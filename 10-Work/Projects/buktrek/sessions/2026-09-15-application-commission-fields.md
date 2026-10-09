---
title: "Проект: Buktrek — комісія, витрати на митницю і комісія перевізника в applications"
date: 2026-09-15
tags: [buktrek, work, session, applications, backend]
category: session
project: buktrek
status: completed
aliases: ["commission", "customs_cost", "carrier_commission"]
pinecone_indexed: false
---

# Buktrek — три нові поля в `applications`

## Мета сесії

Додати в заявки **комісію**, **витрати на митницю** і **комісію від перевізника** плюс валюту для комісії.

Явне обмеження від користувача: **тільки база і логіка, фронт він робить сам**. Тому поля у `setupCreateOperation()` і колонки у `setupListOperation()` свідомо не додавалися.

## Виконано

| Задача | Результат |
|---|---|
| Міграція | `commission`, `customs_cost`, `carrier_commission` — `decimal(10,2)` nullable; `commission_currency_id` + FK на `currencies` `nullOnDelete` |
| Модель | `$fillable` ×4, casts `decimal:2` ×3, relation `commissionCurrency()`, accessor `getCommissionCurrencyAttribute()`, 3 поля в `logOnly()` |
| API-payload | 5 нових ключів в `ApplicationResources` |
| Логіка збереження | `ApplicationsCrudController::updateCommissionFields()`, викликається з `updateApplication()` |
| Валідація | правила в `AppliceationRequest` + inline-валідатор в `updateCommissionFields()` |
| Права | 8 прав міграцією + ключі в `lang/uk/permissions.php` |
| Тести | `ApplicationCommissionFieldsTest` — 7 тестів / 16 асертів |

## Контракт для фронта

`POST /api/system/application/{id}/update`, усередині `value`:

```json
{
  "commission_currency": { "amount": 310.40, "value": 3 },
  "customs_cost": 88.10,
  "carrier_commission": 12.75
}
```

- `commission_currency` повторює форму `amount_currency` / `freight_currency` — `{value, translation_key, label, clear, amount}` на читанні.
- **Ключ, якого немає в payload, не перезаписується.** Форма, що не шле поле, не затре збережене значення.
- Явний `null` очищає поле.
- На читанні суми приходять рядками (`"150.50"`) через cast `decimal:2`.

## Важливі рішення

| Рішення | Чому |
|---|---|
| Одна валюта, тільки для комісії | Вибір користувача. `customs_cost` і `carrier_commission` — без валюти |
| `can()` замість `hasPermissionTo()` для перевірки прав | `hasPermissionTo()` кидає `PermissionDoesNotExist`, якщо права ще немає в БД, і **не** проходить `Gate::before`, тому навіть роль `admin` була б заблокована |
| Не перезаписувати відсутні ключі | Форму робить користувач окремо; проміжний стан не має знищувати дані |
| Валідація прямо в `updateCommissionFields()` | `updateApplication()` працює з сирим `$request->get('value')` без FormRequest — нечислове значення впало б 500-кою на рівні MySQL |
| Відкотив `pint` на трьох старих файлах | Файли не були pint-форматовані; прогін роздув диф зі 62 до 167 рядків суто форматуванням |

## Проблеми й як вирішили

**1. Колізія імен accessor ↔ relation.**
`getCommissionCurrencyAttribute()` і relation `commissionCurrency()` зводяться до одного studly-імені, тому `$this->commissionCurrency` усередині аксесора повертався в сам аксесор → `Undefined property`. Розв'язано явним `$this->getRelationValue('commissionCurrency')`.

Сусідні аксесори цієї пастки уникли випадково: `getDowntimeCurrencyAttribute()` читає relation `downtimeCostCurrency` (інша назва), `getAmountCurrencyAttribute()` — `currency`.

**2. `request()->user()` порожній у тестах.**
Поза HTTP-стеком `auth:api` не відпрацьовує. У тесті resolver довелося виставити вручну: `request()->setUserResolver(fn () => $member)`.

**3. Знайдено баг, не чіпав (картка в Backlog).**
`updateApplication()` викликає `hasPermissionTo('applications-driver-status-edit')`, а такого права в БД немає — є лише `...-read`. Тобто будь-який апдейт із непорожнім `driver_status` валиться 500-кою. Поруч другий дефект: `getFreightCurrencyAttribute()` читає `$this->currency` (це `amount_currency_id`), тобто фрахт показує валюту суми; relation `freightCurrency()` не існує.

## Артефакти

Нові файли:
- `database/migrations/2026_09_15_000002_add_commission_fields_to_applications_table.php`
- `database/migrations/2026_09_15_000003_add_application_commission_permissions.php`
- `tests/Feature/ApplicationCommissionFieldsTest.php`

Змінені:
- `app/Entities/System/Content/Application.php`
- `app/Http/Controllers/Api/Crud/Content/ApplicationsCrudController.php`
- `app/Http/Requests/CRUD/Content/AppliceationRequest.php`
- `app/Http/Resources/ApplicationResources.php`
- `lang/uk/crud.php`, `lang/uk/permissions.php`

Нові права: `applications-commission-{read,edit}`, `applications-commission-currency-{read,edit}`, `applications-customs-cost-{read,edit}`, `applications-carrier-commission-{read,edit}`.

## Що лишилось

- Фронт: поля у `setupCreateOperation()` і колонки у `setupListOperation()` — за користувачем.
- Роздати нові права ролям, крім `admin`, через крут «Права».

## Пов'язані нотатки

- [[2026-09-15-direction-costs-crud]]
- [[project-overview]]
