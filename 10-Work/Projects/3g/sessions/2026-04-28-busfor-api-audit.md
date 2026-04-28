---
title: "Проект: 3g — Аудит Busfor API провайдера"
date: 2026-04-28
tags: [work, session, 3g, busfor, api, audit, refactoring]
category: work
project: 3g
status: completed
pinecone_indexed: false
---

# Аудит Busfor API провайдера

## Мета сесії
Пройтись по всіх методах Busfor API провайдера у `app/Services/Api/v1/Busfor/`, перевірити коректність та швидкодію, потім порівняти реалізацію з офіційною специфікацією Busfor (PDF, 62 сторінки).

## Виконано

### 1. Загальний код-аудит → `app/Services/Api/v1/Busfor/refact.md`
- Проаналізовано всі 5 контролерів, 9 Form Request'ів, 9 Resource'ів, middleware і провайдер роутів
- Знайдено **36 знахідок**, класифіковано за серйозністю:
  - 🔴 9 критичних багів (runtime errors, undefined variables, namespace mismatch)
  - 🟠 6 проблем безпеки (`env()` поза config, `any()` HTTP методи, SSL логіка)
  - 🟡 8 швидкодії (N+1, запити в Resources, відсутні транзакції)
  - 🔵 13 якості коду

### 2. Порівняння spec.pdf ↔ реалізація → `app/Services/Api/v1/Busfor/docs_refact.md`
- Користувач надав спеку у `app/Services/Api/v1/Busfor/spec.pdf`
- Витягнуто текст через `pypdf` (встановлено через `pip3 install --user --break-system-packages`)
- Проаналізовано всі 12 endpoint-ів зі spec
- Знайдено **12 значущих розбіжностей**:
  - 🔴 9 критичних (порушення контракту API)
  - 🟠 5 серйозних
  - 🟢 3 розширення коду поза spec
- Підготовлено **10 ready-to-apply патчів** (A-J)

### 3. Скасовано одну претензію
`dates: [[...]]` у `/route` — це **відповідає specifікації** (вкладений масив у прикладі spec'у), не баг.

### 4. Шаблон як писати API-документацію → `app/Services/Api/v1/Busfor/docs_example.md`
- 17 розділів: філософія, структура, метадані, headers, формат помилки, шаблон endpoint-у, чек-лист, глосарій, changelog, антипатерни (15 пар ❌/✅), pre-publish чек-лист
- Конкретний мінімальний приклад для Busfor
- §16 — TODO: створити **сидер `BusforDocumentationSeeder`** для наповнення таблиці `documentations` (тип `busfor`) усіма 12 endpoint-ами
- §17 — TODO: **тестування у 3 шари** — cURL smoke-script, Laravel Feature tests, опційно Postman/Newman collection

### 5. Знайшов готову інфраструктуру документації в проекті
- Модель `App\Entities\System\Directories\Documentations` + таблиця `documentations`
- Тип `TYPE_BUSFOR = 'busfor'` уже зареєстровано (модель + `config/crud.php:238-242`)
- Маршрут `/documentation/{type}` рендерить через `DocumentView.vue` + `AccordionPage.vue` (HTML/v-html, тобто WYSIWYG-контент)
- Admin CRUD: `/admin/directories/documentations`
- **Висновок:** наповнити можна або через UI, або через сидер. Сидер краще (12 endpoint-ів = багато ручної роботи).

### 6. Додатковий функціонал (TODO у refact.md)
Зафіксовано 3 функціональні дороботи поза рамками контракт-фіксу:
- **TODO 1:** зручності автобуса (Wi-Fi, туалет, розетки, AC, USB, ремені, TV, ковдра) — модель `Bus` не має цих полів
- **TODO 2:** застосування знижки при `/reservate` — у `/trip` знижки повертаються, але `seats.*.discount_id` не валідується і ціна не перераховується
- **TODO 3:** фільтр рейсів `arrival < departure` у `TripsService::getTrips` — зараз можуть повертатись рейси з некоректним часом (крос-добові, інші часові пояси)

## Важливі рішення (ADR)

| Рішення | Альтернатива | Вибір | Чому |
|---------|--------------|-------|------|
| Як читати PDF | poppler-utils (`brew install poppler`) | Python `pypdf` | Користувач відмовився від brew |
| Структура звітів | один файл | два файли (`refact.md`, `docs_refact.md`) | різні перспективи: код-якість vs контракт |
| Формат знахідок | список багів | таблиця з пріоритетами + патчі | щоб можна було швидко застосувати |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Google Docs за `WebFetch` недоступний (auth) | Користувач поклав spec.pdf у репо |
| `pdftoppm` (Read tool для PDF) і `pdftotext` не встановлені на macOS | `pip3 install pypdf` через `--break-system-packages`, далі Python-скрипт екстрактував текст у `/tmp/busfor_spec.txt` |
| PEP 668 блокував pip install | додав `--break-system-packages` |

## Ключові знахідки

### 🔴 Контрактні розбіжності зі spec
- `/login` — поле `user` у spec, `login` у коді
- `/login` — формат помилки `{"message":...}` vs `{"error":{...}}`
- `/cancel`, `/buy` — повертають `id` замість `orderId`
- `/retinfo` — `percId='full'` (string) замість integer для full_refund
- `/retinfo` — у `to.id` для трансферу записується **назва** замість `id` (явний баг)
- `/status` — повертає `CANCELLED` (з двома L) замість `CANCELED` зі spec
- `/status` — `PREBOOKED` витікає у відповідь, хоч у spec такого статусу немає
- `/status` — `NOT_FOUND` повертається як error замість `state: "NOT_FOUND"`
- `/trips` — `lang` помилково обовʼязкове, у spec optional
- `/point_connect_success` — endpoint у spec, але роут **закоментовано** в `BusforApiProvider.php:29` + опечатка `pointConnectSucces`

### 🔴 Runtime баги
- `Middleware/ExternalAuthToken.php` — namespace `External\Middleware`, файл у `Busfor/Middleware/`
- `TripListResource.php:43` — `$trip->back_route` (undefined variable, має бути `$this->back_route`)
- `TripListResource.php:62` — undefined `$transfer` коли не трансфер
- `OrderController.php:99` — `$seat['parent_ticket_id']` замість `$ticket['parent_ticket_id']`
- `TicketsController.php:99-120` — `returnInfoTicket` без `ticket`/`buyid` повертає перший Order у БД

### 🟡 Швидкодія
- N+1 у Resources: `TripListResource` робить 2 запити `Station::find()` на КОЖЕН рейс
- `->get()->count() > 0` замість `->exists()` у трьох Resource'ах
- `OrderController::reject/sell` — N+1 update без транзакцій
- `TicketsController::returnTicket` — без транзакцій, кілька save()
- `getAllStations` — без кешу і пагінації

### 🟢 Розширення коду поза spec (треба задокументувати або прибрати)
- Уся логіка трансферних рейсів (`is_transfer`, `bus_transfer`, `wait_time_minutes`...)
- Поля `discount`, `gender`, `transfer_number`, `prebooking` у `/reservate`
- Endpoint-и `/ping`, `/stops`

## Артефакти

- `app/Services/Api/v1/Busfor/spec.pdf` — спецификація (надана користувачем)
- `app/Services/Api/v1/Busfor/refact.md` — загальний код-аудит з 36 знахідками + 3 функціональні TODO
- `app/Services/Api/v1/Busfor/docs_refact.md` — порівняння spec vs реалізація з патчами A-J
- `app/Services/Api/v1/Busfor/docs_example.md` — шаблон як писати API-документацію (17 розділів) + TODO сидер + TODO тестування
- `/tmp/busfor_spec.txt` — витягнутий текст PDF (тимчасовий)

## Команди використані
```bash
pip3 install --user --quiet --break-system-packages pypdf
python3 -c "import pypdf; r=pypdf.PdfReader('spec.pdf'); ..." > /tmp/busfor_spec.txt
```

## Наступні кроки (для майбутніх сесій)

### Контракт API
1. **Швидкі фікси (~30 хв):** patches A, B (orderId), E (lang), I (POST методи)
2. **Контракт (~1 год):** patches C, D (login), F (status mapping), G, H (retinfo), J (point_connect_success)
3. **Документація (~2 год):** узгодити spec з реалізацією трансферів, прибрати/задокументувати `/ping`, `/stops`
4. **Локалізація (~1 день):** реалізувати реальне використання `lang` у всіх endpoint-ах

### Тестування (`docs_example.md` §17)
5. **cURL smoke-script** на dev — швидкий ручний прогін усіх 12 endpoint-ів
6. **Laravel Feature tests** у `tests/Feature/Busfor/` — для CI/регресії (потребує перевірки фабрик)
7. **Postman/Newman collection** — опційно для QA-команди

### Наповнення публічної документації (`docs_example.md` §16)
8. Створити `database/seeders/BusforDocumentationSeeder.php` — наповнити `documentations` (тип `busfor`) усіма 12 endpoint-ами **після застосування патчів A-J**
9. Перевірити на `/documentation/busfor`

### Додатковий функціонал (`refact.md` TODO 1-3)
10. **TODO 3 (швидко):** фільтр рейсів `arrival < departure` у `TripsService::getTrips` (+ опційно artisan-команда `trips:audit-times`)
11. **TODO 2:** валідація і застосування знижки при `/reservate` (поле `seats.*.discount_id` + перерахунок ціни в `BookingService`)
12. **TODO 1:** зручності автобуса (модель `Bus` + міграція + Resources) — потребує погодження формату з frontend-командою

## Пов'язані нотатки
- [[2026-04-23-infobus-sync-transfer-fix]] — попередня робота над трансферними квитками (BookingService було відкочено)
- [[2026-04-28-performance-n1-fixes]] — також аудит N+1, цього разу для Busfor API