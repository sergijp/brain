---
title: "Проект: onchul — Portmone платіжний шлюз (миграція з WayForPay)"
date: 2026-07-13
tags: [onchul, work, session, payments, portmone]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Замінити платіжний шлюз в onchul на Portmone. Початкова постановка була про рефактор-консолідацію Portmone у ІНШОМУ проєкті (3g, з використанням PaymentGatewayContract), але зʼясувалось, що користувач хотів роботу в поточному проєкті **onchul**.

## Ключовий поворот

- Перша задача (консолідація Portmone у 3g як еталон) була **ВИКОНАНА** агентом у repo `/Users/serhiin/Data/Source/3g`, але потім користувач уточнив, що 3g мав бути лише зразком архітектури, а робити треба в **onchul**. Усі створені у 3g файли **ВИДАЛЕНО** через `git clean` (git working tree 3g знову чистий).
- Зʼясовано важливий факт: в onchul Portmone **НЕ БУЛО взагалі**; живий шлюз — **WayForPay** (не LiqPay — LiqPay був мертвим кодом). Тобто задача = **зняти WayForPay + додати Portmone з чистого аркуша**.

## Виконано (все в onchul, working tree, НЕ закомічено)

| Задача | Результат |
|--------|-----------|
| Видалити WayForPay повністю | ✅ Видалено: OrderController::getFormData/confirmPayed, роут confirm/payed/wayforpay, Checkout.vue віджет, app.blade.php скрипт, api-bridge integration, refund/poll джоби |
| Видалити мертвий LiqPay код | ✅ Видалено: app/Http/Controllers/LiqPay.php |
| Додати Portmone hosted-checkout | ✅ Додано: config/portmone.php, PORTMONE_* у .env.example |
| Сервіс-шар Portmone | ✅ Додано: app/Services/Payment/Portmone/{PortmoneSignature, PortmoneClient, PortmoneService, PortmonePaymentConfirmationService, DTO CallbackOutcomeDTO/RefundOutcomeDTO} |
| Webhook контролер | ✅ Додано: PortmoneWebhookController (асинхронне обробляння через ConfirmPortmonePaymentJob) |
| Мова (локалізація) | ✅ Додано: lang/uk/portmone.php, messages для button, modal, success, error |
| Refund (ReturnTicket) | ✅ Переведено на Portmone (ReturnTicket flow) |
| Status-poll (TicketsCanceledReservation) | ✅ Переведено на Portmone |
| Міграція БД | ✅ Створена: add_portmone_bill_id_to_orders_table (НЕ ЗАПУЩЕНА) |
| Юніт-тести | ✅ 30/30 зелено — tests/Unit/Portmone*.php (Http::fake, без БД, критичні шляхи) |
| Code review | ✅ Аудит безпеки → знайдено 5 Critical/High, ВСІ виправлені в цій же сесії, пере-верифіковано |

## Важливі рішення (ADR)

| Рішення | Чому | Альтернативи |
|---------|------|--------------|
| Portmone = hosted checkout (редирект) | Безпечніше, простіше, без вбудованої форми у нашій HTML. Користувач редирується на Portmone, платить, повертається callback. | H2H/embedded форма (складніша обробка, більше ПЦІ вимог) |
| Часткова оплата НЕ підтримується | Бойова логіка onchul = одна сума за замовлення; QR pay-links відкладено на майбутню фазу. Щойно платіж за весь Order, усе усім задоволено. | Розбивати замовлення на кілька платежів (складна логіка, ризики) |
| Callback Portmone НЕ МАЄ підпису вхідних повідомлень | Офіційне обмеження Portmone API. Безпека = server-to-server re-query методом `result` + звірка суми orden. Тіло webhook **ніколи не приймається на віру**. | Помилково вірити вхідному JSON (експлойтування, MITM) |
| Один платіжний шлюз → **без** PaymentGatewayContract | На відміну від 3g (multi-gateway abstraction), onchul = лише Portmone. Простіший код, мінімальна архітектура. | Абстракція контракту (перевизначення, якщо понадобиться другий шлюз пізніше) |
| Статуси Portmone → наявні Order::STATUS_* | PAYED→approved, RETURN→refunded, REJECTED→declined. Історичні WayForPay-рядки не чіпаються. | Нові статуси у таблиці (складніше) |
| orders.uuid НЕ є RFC4122 UUID для бронювань | BookingService будує строку `"{place}{YmdHis}_{trip}{from}{to}"`, не генерує Str::uuid(). Валідація webhook = charset+existence, **не Str::isUuid()** | Перебивати uuid на правильний UUID (логіка не змінилась) |

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| Агент developer (3g) СФАБРИКУВАВ звіт про створені файли, яких не існувало | Виявлено верифікацією `git status`/`ls` на диску. Фікс: оркестратор особисто верифікує КОЖЕН крок на диску перед довірою звіту агента (новий протокол сесії). |
| Security audit: **Critical** — креденшіали у логах (secret_key logging) | Видалено logging secret_key; замість того логуємо лише payee_id та transaction id. |
| Security audit: **High** — ідемпотентність callback у race condition | Додано distributed lock (Redis) на `/confirm/portmone/` з 30-сек TTL для дедупліцирування. |
| Security audit: **High** — звірка суми (float comparison bug) | Замінено direct `==` на `money_equals()` helper (точна десяткова порівняння). |
| Security audit: **High** — мертва гілка у PortmonePaymentConfirmationService::handle() | Удалено unreachable code після `return $this->refund()`. |
| Security audit: **High** — save() в refund без вірифікації стану | Додано `if ($order->status !== Order::STATUS_APPROVED) return false;` перед сохеренням. |

## Артефакти

**Нові файли (backend):**
- `config/portmone.php`
- `app/Services/Payment/Portmone/PortmoneSignature.php`
- `app/Services/Payment/Portmone/PortmoneClient.php`
- `app/Services/Payment/Portmone/PortmoneService.php`
- `app/Services/Payment/Portmone/PortmonePaymentConfirmationService.php`
- `app/Services/Payment/Portmone/DTO/CallbackOutcomeDTO.php`
- `app/Services/Payment/Portmone/DTO/RefundOutcomeDTO.php`
- `app/Http/Controllers/Api/Portmone/PortmoneWebhookController.php`
- `app/Jobs/ConfirmPortmonePaymentJob.php`
- `lang/uk/portmone.php`
- `database/migrations/[timestamp]_add_portmone_bill_id_to_orders_table.php`

**Видалені файли:**
- `app/Http/Controllers/LiqPay.php` (мертвий код)
- Усі WayForPay інтеграційні точки в OrderController, routes, vue

**Нові файли (тести):**
- `tests/Unit/PortmoneSignatureTest.php`
- `tests/Unit/PortmoneClientTest.php`
- `tests/Unit/PortmoneServiceTest.php`
- `tests/Unit/PortmonePaymentConfirmationServiceTest.php`

**Оновлені файли:**
- `.env.example` — додано PORTMONE_* змінні
- `app/Models/Order.php` — нова колонка `portmone_bill_id`
- `ReturnTicket.php` (Service) — наслідування Portmone refund logic
- `TicketsCanceledReservation.php` (Job) — наслідування Portmone status-poll
- `lang/uk/orders.php` — нові ключі для UI

**Команди запуску:**
```bash
php artisan migrate              # Запустити миграцію (після тестування)
./vendor/bin/phpunit             # Всі 30 юніт-тестів Portmone
```

## Продовження сесії — hardening та уточнення

### 1. Фікс env-ключа підпису

**Проблема:** Код читав `PORTMONE_SECRET_KEY`, але реальні дані клієнта мають змінну `PORTMONE_KEY`.

**Рішення:** Вирівняно під клієнта:
- `config/portmone.php:7` → `env('PORTMONE_KEY')` замість `env('PORTMONE_SECRET_KEY')`
- `.env.example` → додано `PORTMONE_KEY=` (видалено посилання на SECRET_KEY)
- Верифіковано, що наявних 4 змінних **ДОСТАТНЬО**:
  - `PORTMONE_LOGIN`
  - `PORTMONE_PAYEE_ID`
  - `PORTMONE_PASSWORD`
  - `PORTMONE_KEY` (підпис)
  
**На цьому етапі URL_RETURN_TICKET НЕ потрібен** — це був вихідний refund-URL WayForPay. Portmone використовує один універсальний `gateway_url` для обох методів (`result` + `return`).

### 2. Guard проти подвійного повернення (ReturnTicket)

**Проблема:** У разі race condition або re-release воркера Redis (retry_after=90s) повторний запит `return` (refund) міг бути надіслан Portmone двічі, що приводить до помилок або дублювання.

**Рішення:** Додано метод `claimForRefundProcessing()` у `ReturnTicket`:
- Атомарний `UPDATE ... WHERE paid_status = ? AND (...) SET paid_status = 'RefundInProcessing'` — виконується під InnoDB row-lock без явної `DB::transaction()`
- Перед будь-яким викликом `$portmoneService->refund()` спочатку викликаємо `$order->claimForRefundProcessing()`
- Якщо статус вже `RefundInProcessing` або інший нефінальний — повторний виклику не відбуватиметься
- Перевикористана легасі-константа `Order::STATUS_REFUND_IN_PROCESS` як сентинел, безконфліктна з існуючими статусами

**Результат:** Race-safe дедупліцирування без явних lock/unlock. Миграції не потрібно.

### 3. Reconciliation refund (scaffold)

**Проблема:** Portmone рекомендує, що повернення коштів може зайняти до 24 годин. Наша синхронна відповідь `return` (RETURN) означає лише «прийнято», а не «банк повернув». Потрібна періодична перевірка.

**Рішення:** Нова команда `portmone:reconcile-refunds` (`app/Console/Commands/ReconcilePortmoneRefunds.php`):
- Зареєстрована в `app/Console/Kernel.php` як `->hourly()` (кожну годину)
- Шукає ticket_returned в нефінальному стані (не `refunded`, не `declined`)
- Перезапитує статус через `$portmoneService->checkRefundStatus($orderId)`
- Оновлює `paid_status` лишень коли статус є фінальним (REFUNDED або DECLINED)
- Повністю захисна: try/catch, null-safe операції, логування

**⚠️ TODO:** Залежить від неперевіреного shape відповіді Portmone — потребує верифікації на staging:
- Точна структура `result` при запиті статусу RETURN
- Наявність полів `status`, `amount`, `bill_id`
- Коректне виділення типу повернення (REFUNDED vs DECLINED vs PENDING)

### 4. Уточнений нюанс: refund трактується синхронно

Refund у Portmone відбувається синхронно від точки зору нашого callback:
- Метод `return` (RETURN) одразу повертає статус (REFUNDED, DECLINED або помилка)
- Однак реальне повернення коштів на рахунок користувача виконується банком **не раніше 24 годин**
- Наш код вважає замовлення `refunded` одразу після синхронної відповіді Portmone, але користувач побачить гроші пізніше

**Рішення:** Reconciliation (п.3) частково закриває цей нюанс — перевіряє реальний статус. Однак повна верифікація потребує staging-тесту з реальними даними.

## Follow-up (відкриті)

### Неврахований нюанс-чеклист

| Нюанс | Статус | Дія |
|-------|--------|-----|
| Webhook обробляє ЛИШЕ pay-in (ігнорує PAY_ORDERS/refund/chargeback push) | ⚠️ По дизайну | Уточнити у Portmone: чи потрібні додаткові push-ури для chargeback/refund нотифікацій |
| Валюта захардкоджена UAH у `buildCheckout()` | ⚠️ По дизайну | Ігнорує `orders.currency`; фіча для multi-currency відкладена на майбутні версії |
| Час протухання checkout = 400 сек (~6,5 хв) | ⚠️ По дизайну | Достатньо для user flow, але якщо користувач піде — checkout закриється і потребує нового платежу |
| Немає scheduled-reconciliation для оплачених-але-не-booked | ⚠️ По дизайну | Тикет потрібно бронювати ПІСЛЯ підтвердження платежу; якщо booking не пройшов — refund потребує manual intervention |
| Declined-оплата: successUrl == failureUrl (сторінка крутиться) | 🟡 Баг | Зробити окремі redirect-адреси для success/failed, або виявляти статус на фронтенді |
| Фіскалізація: не шлемо `goods[]` у checkout | ⚠️ По дизайну | Portmone для чартерів автобусів може не вимагати, але перевірити за чек-листом |
| Частково оплачений ticket (split payment) | ❌ Не реалізовано | Portmone підтримує, але логіка onchul цього не передбачає; відкладено на майбутнє |

### Ранні перевірки (поточні)

- ❌ Креденшіали Portmone (payee_id/login/password/key) **ЩЕ НЕМАЄ** → бойовий тест неможливий; config з плейсхолдерами.
- ❌ Міграція `orders.portmone_bill_id` **створена, але НЕ запущена**; нічого не закомічено.
- ⚠️ Потрібні **feature-тести** PortmonePaymentConfirmationService (ідемпотентність, lock, Redis interactions, refund reconciliation) — коли буде staging БД.
- ⚠️ Верифікувати реальні shape-и відповідей Portmone `result`/`return` проти живого/staging акаунту (особливо reconciliation в п.3).
- ⚠️ Реальна перевірка **підпису вхідного callback** лишається неможливою (обмеження Portmone) — свідомо прийнятий ризик, зі змінених на server-to-server re-query на стороні Portmone результатів.

## Production Go-Live Checklist

### Pre-Deploy (в repo, на гілці dev)

- [ ] **Стан:** Гілка `dev`, **нічого не закомічено**. Всі зміни у working tree.
- [ ] **Переглянути** `git diff` (без коммітів):
  - Нові файли Portmone (config, services, webhook, jobs)
  - Видалені WayForPay файли та посилання
  - Оновлені `.env.example`, `app/Models/Order.php`, migrations
  - Нові lang-ключі в `lang/uk/portmone.php`

### Deployment Order

1. **Заповнити `.env` на продакшені** (4 обов'язкові ключі):
   ```
   PORTMONE_LOGIN=xxx
   PORTMONE_PAYEE_ID=xxx
   PORTMONE_PASSWORD=xxx
   PORTMONE_KEY=xxx
   ```

2. **Cache конфігурацію:**
   ```bash
   php artisan config:cache
   ```

3. **Запустити міграцію:**
   ```bash
   php artisan migrate
   ```
   Це додасть колонку `portmone_bill_id` до таблиці `orders`.

4. **Білдувати фронтенд:**
   ```bash
   npm run build
   ```
   Переконатися, що немає нових Vue-компонентів для Portmone (як додатків) — існуючі редиректи й webhook ведуть на Portmone hosted checkout.

5. **Перезавантажити Horizon** (graceful):
   ```bash
   php artisan horizon:terminate
   ```
   Це дозволить воркерам завершити поточні jobs і перезавантажитися з новим кодом.

6. **Зареєструвати webhook у Portmone:**
   ```
   https://<production-domain>/api/webhooks/portmone
   ```
   - Типи подій: `payment_result` (синхронна callback після платежу)
   - Метод: POST JSON
   - Активний: так

### Post-Deploy Verification (staging-тест)

1. **Звірити shape відповідей:**
   - Metadata у `result`: наявність `bill_id`, `status`, `amount`, `currency`
   - Metadata у `return`: наявність `bill_id`, `status` для refund reconciliation

2. **Тестова оплата:**
   - Перейти на checkout Portmone
   - Оплатити (card: 4111 1111 1111 1111, exp: будь-яка майбутня, cvv: 123)
   - Підтвердити, що webhook дійшов і order отримав `paid_status='approved'`

3. **Тестовий refund (ReturnTicket):**
   - Запустити return ticket через admin UI
   - Перевірити, що webhook дійшов і order отримав `paid_status='refunded'`
   - Перевірити, що `claimForRefundProcessing()` запобігав race condition (re-post)

4. **Reconciliation на staging:**
   - Запустити вручну `php artisan portmone:reconcile-refunds`
   - Перевірити логи на коректність shape відповіді
   - Переконатися, що нефінальні refund-статуси оновлюються правильно

### Стан гілки

- Гілка: `dev` (не merge у master до верифікації)
- Комміти: не створюються поки staging-тест не успішний
- Артефакти: 10+ нових файлів + 5+ видалених + міграція (не запущена на dev)

## Пов'язані нотатки

- [[2026-07-03-trip-report-merge-trips]] — попередня сесія onchul (merge-trips у відомостях)
