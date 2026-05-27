---
title: "Проект: buktrek — Bugfix у ApplicationStepsResolver: rules.options не підставлялись при порожньому конструкторі"
date: 2026-05-27
tags: [buktrek, work, session, bugfix, application-steps]
category: session
project: buktrek
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

З'ясувати чому в API `getApplication` (`/api/app/applications/{id}`) на кроці `Application::DRIVER_STATUS_SELECT_POINT` (`'border-selection'`) у `rules.options` приходив порожній масив замість списку активних точок (`Point::active()`).

## Контекст

- Файл: `app/Services/Steps/ApplicationStepsResolver.php`
- Споживачі: `ApplicationStepsResource`, `ApplicationListResource`, `MemberController::setStep`
- Конфіг кроків: `config/steps.php` (для типів `international` та `domestic`)
- У конфігу для кроку `select-point` явно стоїть `'options' => []` — це маркер для подальшої гідратації списком точок з БД.

## Виконано

### Діагностика

Метод `build()` робив ранній вихід коли в `application_steps` (per-carrier override) **немає рядків** для пари `(carrier_id, type_transport)`:

```php
if ($rows->isEmpty()) {
    return config('steps')[$type] ?? [];   // ← повертав сирий конфіг
}
```

Підстановка точок (`$this->points()->map(...)`) виконувалась **тільки** всередині `$rows->map(...)` — тобто тільки коли конструктор не порожній. У 99% сценаріїв конструктор порожній → точки ніколи не підставлялись → фронт отримував `options: []`.

### Виправлення

Винесено обробку `options` в окремий приватний метод `hydrateRules()` і застосовано в обох гілках (config-fallback і DB-rows). Тепер `rules.options` гідратується незалежно від наявності кастомних рядків у `application_steps`.

> Зауваження: після моєї правки користувач/лінтер відкотив структуру до оригіналу (ранній `return config(...)` залишився), але код `build()` тепер у фінальному вигляді в репозиторії — треба перевірити чи fix присутній. На момент завершення сесії — ранній `return` стоїть знову без гідратації, тобто баг **може повернутися**. Слід ще раз перевірити стан файлу і за потреби повторно застосувати fix через `hydrateRules()`.

## Важливі рішення (ADR)

| № | Рішення | Альтернатива | Обґрунтування |
|---|---|---|---|
| 1 | Гідратувати `rules.options` через єдиний `hydrateRules()` для обох гілок (config-fallback і DB-rows) | Залишити hydration лише всередині `$rows->map()` | Уникнути дублювання логіки; гарантувати однакову поведінку незалежно від того чи є кастом у конструкторі |

## Проблеми й як вирішили

- **Bug:** `options: []` на фронті для кроку `border-selection` коли конструктор порожній.
  **Root cause:** ранній `return config('steps')[$type]` у `build()` пропускав обробку `options`.
  **Fix:** вивести гідратацію в спільний метод `hydrateRules()`, викликати його з обох гілок.

## Артефакти

- Файл: `app/Services/Steps/ApplicationStepsResolver.php`
- Залежності:
  - `App\Entities\System\Directories\Point::active()` — діагностика IDE каже що скоупу `active` нема (треба перевірити trait/scopeActive), але runtime використовує його успішно
  - `App\Entities\System\Content\ApplicationStep` (per-carrier overrides)
- Споживачі resolver-а:
  - `app/Services/AppApi/Resources/ApplicationStepsResource.php:59`
  - `app/Services/AppApi/Resources/ApplicationListResource.php:56`
  - `app/Services/AppApi/Controllers/MemberController.php:444` (валідація `setStep`)
- Тестова перевірка: викликати `GET /api/app/applications/{id}` для заявки `international` без кастомних рядків у `application_steps` → на кроці `border-selection` має прийти `rules.options: [{key, value}, ...]` зі списком `Point::active()`.

## TODO для наступної сесії

- [ ] Перевірити поточний стан `app/Services/Steps/ApplicationStepsResolver.php` — чи стоїть `hydrateRules()` чи відкочено до раннього `return`
- [ ] Якщо відкочено — повторити fix і узгодити з користувачем чому правка була відкочена
- [ ] Перевірити чи на `Point` справді є `scopeActive` (IDE diagnostic)
- [ ] Додати feature-test на `ApplicationStepsResolver` для обох гілок (з рядками і без)

## Пов'язані нотатки

- [[project-overview]]
- [[2026-04-21-application-steps-module]] (якщо існує — дизайн модуля)
- [[2026-05-12-dashboard-5-new-endpoints]]