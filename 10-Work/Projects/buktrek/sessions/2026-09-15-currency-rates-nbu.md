---
title: "Проект: Buktrek — крут курсів валют і щоденний стяг з НБУ"
date: 2026-09-15
tags: [buktrek, work, session, currency, integration, schedule]
category: session
project: buktrek
status: completed
aliases: ["currency_rates", "НБУ", "rates:fetch"]
pinecone_indexed: false
---

# Buktrek — курси валют до гривні + інтеграція з НБУ

## Мета сесії

Крут курсів валют відносно гривні (USD, EUR, з можливістю додавати інші), щоденна джоба о 09:00, примусовий запуск з UI і добір історичних курсів за період.

## Джерело даних — НБУ

Відкриті дані, **ключ не потрібен**, база котирувань — саме гривня. Обидва ендпоінти перевірені живцем перед тим, як писати код.

```
# на дату
https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date=YYYYMMDD&json
→ [{"rate":44.618,"cc":"USD","exchangedate":"15.09.2026"}]

# за період
https://bank.gov.ua/NBU_Exchange/exchange_site?start=YYYYMMDD&end=YYYYMMDD&valcode=usd&sort=exchangedate&order=asc&json
→ додатково віддає rate_per_unit і units
```

## Виконано

| Задача | Результат |
|---|---|
| Таблиця | `currency_rates`: `currency_id` FK, `date`, `rate` decimal(18,6), `unique(currency_id, date)` |
| Модель | `CurrencyRate` + `scopeBetween()`, accessor `currencyCode` |
| HTTP-клієнт | `App\Services\Currency\NbuRatesService` — `fetchForDate()` / `fetchRange()` |
| Джоба | `FetchCurrencyRatesJob` (`ShouldQueue`, `tries=3`) |
| Команда | `rates:fetch {--date=} {--from=} {--to=} {--sync}` |
| Розклад | `dailyAt('09:00')->withoutOverlapping()` |
| Крут | `CurrencyRateCrudController` + фільтри date_range і валюта |
| Кнопки | «Оновити зараз» / «Стягнути за період» через `FetchRatesOperation` |
| Права | 6 прав, включно з `currency_rates-fetch` |
| Тести | `CurrencyRatesTest` — 15 тестів / 23 асерти |

## Важливі рішення

| Рішення | Чому |
|---|---|
| НБУ, а не платний FX-API | Потрібні курси саме **до гривні**, а НБУ — першоджерело для них. Безкоштовно, без ключа, без лімітів |
| Список валют із `currencies`, а не константа | «Можуть ще додаватись» працює само: додав валюту в довідник, зробив активною — джоба підхопила |
| Один шлях для розкладу, команди і кнопок | Усі троє диспатчать ту саму `FetchCurrencyRatesJob`. Немає розбіжності в поведінці між cron і ручним запуском |
| `updateOrCreate` + `unique(currency_id, date)` | Ідемпотентність: повторний стяг за той самий період не плодить дублів. Критично, бо черга повторює джобу при збої (`tries=3`), а користувач може перекрити вже стягнутий діапазон |
| `syncLatestRate()` у `currencies.exchange` | Це поле вже використовує решта системи — інакше довелося б переписувати інші місця |
| Порожня відповідь ≠ помилка | У вихідні та свята НБУ курс не публікує. `failed()` теж повертає порожній масив, а не виняток |
| Стеля `MAX_FETCH_RANGE_DAYS = 366` | Щоб кнопка «Стягнути за період» не запустила стяг за десять років |
| URL у `config/services.php` | Не захардкоджений, через env — можна підмінити на тесті чи дзеркалі |

## Перевірка на живих даних

```
rates:fetch --sync                              → USD 44.618, EUR 51.5231, exchange оновився
rates:fetch --from=2026-09-01 --to=2026-09-14   → двічі поспіль = 30 рядків (15 днів × 2 валюти), дублів немає
schedule:list                                    → 0 9 * * * php artisan rates:fetch
route:list --name=currency_rates                 → 11 роутів
```

Тести — на `Http::fake` і `Bus::fake`, без походів у мережу.

## Артефакти

Нові файли:
- `database/migrations/2026_09_15_000004_create_currency_rates_table.php`
- `database/migrations/2026_09_15_000005_add_currency_rates_permissions.php`
- `app/Entities/System/Directories/CurrencyRate.php`
- `app/Services/Currency/NbuRatesService.php`
- `app/Jobs/FetchCurrencyRatesJob.php`
- `app/Console/Commands/FetchCurrencyRates.php`
- `app/Crud/Operations/FetchRatesOperation.php`
- `app/Http/Controllers/Api/Crud/Directories/CurrencyRateCrudController.php`
- `app/Http/Requests/CRUD/Directories/CurrencyRateRequest.php`
- `resources/js/crud/base/buttons/CrudFetchRatesButton.vue`, `CrudFetchRatesRangeButton.vue`
- `tests/Feature/CurrencyRatesTest.php`

Змінені: `config/services.php`, `app/Console/Kernel.php`, `routes/api.php`, `lang/uk/{crud,permissions}.php`, `PermissionsTableSeeder.php`, `ButtonManager.vue` + чотири файли фронт-реєстрації круту.

## Правка за фідбеком: рядок = дата

Перша версія круту показувала рядок на кожну пару «валюта + дата». Треба було інакше: **один рядок — одна дата, курси всіх валют у колонках**. Плюс замість Swal і нативного `<input type="date">` — власні компоненти проєкту.

### Як розв'язано

`CurrencyRateDay` — модель «дня» над тією самою таблицею `currency_rates`. Ключова ідея: **id обчислюється з дати** (`Ymd` → `20260915`). Він лишається цілим числом, тому штатні роути `edit(int $id)` / `update(int $id)` / `delete(int $id)` працюють без окремої таблиці й без зміни схеми.

Контролер більше не покладається на штатні операції — `search` / `edit` / `store` / `update` / `delete` перевизначені:

- `search()` — сторінка це набір **дат** (`distinct` + `forPage`), далі `pivot()` розкладає курси по колонках; `LengthAwarePaginator` збирається вручну
- `store()` / `update()` — upsert по всіх валютах дня; **порожнє значення видаляє курс цієї валюти**, а не пише нуль; зміна дати переносить день цілком
- `delete()` — прибирає всі курси за дату

Колонки й поля будуються динамічно з активних валют, тому нова валюта з'являється в круті сама — так само, як її вже підхоплює джоба.

### Свої компоненти замість Swal

| Було | Стало |
|---|---|
| `Swal.fire` з двома `<input type="date">` | `FetchRatesManager.vue` на `EntityWrapper` / `EntityHeader` / `EntityContent` / `EntityFooter` + `Loader` |
| нативний date-інпут | `vue-datepicker-next` з `range` — той самий, що в `DateRangeFilter` |
| `Swal` toast на відповідь | глобальний перехоплювач `axios`, який показує `NotyResource` |

Модалка підключена як повноцінна крут-операція: `FETCH_RATES_OPERATION` у `operations.js` + маршрут у `crud/config/index.js`, кнопка відкриває її через роут (за взірцем `CrudCountCreateButton`).

### Формат дати

У списку — `DD.MM.YYYY` (формат проєкту), у формі редагування — `Y-m-d`, бо саме з нього `datepicker` розбирає дату однозначно.

### Пастки, на які натрапив

- `edit`/`update`/`delete` у крут-операціях типізовані як `int $id` — саме тому «дата як id» не спрацювала б рядком, і знадобився `Ymd`.
- Фільтри приходять як `['date_from_to' => [...]]` (ключ → значення), а не списком `[{name, value}]`. Спершу зібрав тест із неправильною формою і отримав 500 у `Filters::applyFiltersQuery`.

## Що лишилось

- **Перевірити, що на сервері стоїть cron на `schedule:run`.** `Kernel::schedule()` до цього був порожній, тобто розкладом у проєкті ще не користувалися — є ризик, що крон просто не налаштований і щоденний запуск буде мертвий.
- Роздати права `currency_rates-*` ролям, крім `admin`.

## Пов'язані нотатки

- [[2026-09-15-direction-costs-crud]]
- [[2026-09-15-application-commission-fields]]
