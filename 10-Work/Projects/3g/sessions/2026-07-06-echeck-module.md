---
title: "Проєкт: 3g — Діагностика echeck-джоб + модуль ECHECK (backend+frontend, на паузі)"
date: 2026-07-06
tags: [3g, work, session, echeck, fiscal]
category: session
project: 3g
status: in-progress
aliases: ["ECHECK module", "echeck пункт меню"]
pinecone_indexed: false
---

# 3g — ECHECK: діагностика + новий модуль (ПАУЗА)

Гілка: `driver`. HEAD: `29ea4123`. **Усе незакомічено, міграції НЕ запускались, frontend НЕ збирався.**

## Мета сесії
1. Розібратись, чому 21 `SendEcheckSmsJob` відкладаються до опівночі.
2. Зробити діагностичні роути (перевірка/відкриття зміни, відправка чеку по номеру квитка).
3. Спроєктувати і реалізувати повноцінний пункт меню **ECHECK** (за правами).

## Виконано

### A. Діагностика 21 завислої джоби (root cause)
- **Причина НЕ throttle і НЕ `force`.** У `SendEcheckSmsJob::handle()` (~рядки 74-86) shift-check: якщо `EcheckService::shiftStatus()['data']['status'] !== 'OPEN'` → `$this->release(Carbon::tomorrow()->addMinutes(5)->diffInSeconds())` → джоба відкладається до 00:05 наступної доби. Блок **не читає `force`** — тому висять і force=0, і force=1.
- **Корінь кореня:** зовнішній e-check API висить. `cURL error 28: timed out after 30004ms ... https://prod.e-check.com.ua/v2/open-api/shift/open`. Логін проходить (швидко), висне саме операція `/shift/open` (0 байт за 30с) → зовнішня недоступність e-check, не наш конфіг/креденшли.
- `EcheckService::requestApi` не мав timeout/retry, і токен не кешувався (кожен виклик — зайвий login). `shiftStatus()` йде тим самим шляхом → кожна спроба джоби блокує воркер до 30с × tries=10 × 21 джоба.
- **Що станеться природно:** доки зміна не OPEN — джоби щодоби о 00:05 знову відкладаються, витрачаючи по 1 attempt. Після 10 спроб → тихо у `failed_jobs` без SMS. **Ручне форсування score при закритій зміні лише палить бюджет retry** — НЕ робити.

### B. Модуль ECHECK — реалізовано 3 етапи (див. нижче «Стан файлів»)
Рішення замовника (ADR):
- Дії (відкрити/закрити зміну, відправити/скасувати чек) — **синхронно у попапі** (SweetAlert).
- Кандидати = scope `pendingEcheck` + окрема вкладка **sold**.
- Скасування чеку **скидає `echeck_id`** → дозволяє повторну відправку. Cancel можливий лише поки зміна відкрита (обмеження API).
- Права: **2** — `echeck-read` (перегляд), `echeck-manage` (дії).
- Фільтр кандидатів — за **датою поїздки** (`trips.date`).
- Крон `ShiftOpenJob`/`ShiftCloseJob` (00:00/23:59) **лишаємо**, але тепер вони теж логують зміни.

## Стан файлів (git status на момент паузи)

### Змінені (M)
- `app/Services/EcheckService.php` — `requestApi`/`requestLogin`: `connectTimeout(5)->timeout(20)`, `retry(2,300)` **ТІЛЬКИ для GET** (POST/DELETE фіскальні — без retry, щоб не дублювати чек/open-close). Увімкнено читання кешу токена `cache('token-Echeck')`.
- `app/Jobs/Echeck/ReceiptCancelJob.php` — після успішного `cancelEcheck` (перевірка `shiftStatus==OPEN` перед cancel) скидає `echeck_id/echeck_answer/echeck_sms_sent_at`; пише `EcheckReceipt(status=cancelled)`.
- `app/Jobs/Echeck/SendEcheckSmsJob.php` — ДОДАНО лише логування (існуюча логіка не змінена): `logReceiptCreated()` після createEcheck, `markReceiptSmsSent()` після SMS. try/catch — аудит не ламає echeck.
- `app/Jobs/Echeck/ShiftOpenJob.php`, `ShiftCloseJob.php` — крон тепер пише `EcheckShiftLog(source=cron)`.
- `routes/api.php` — прибрано всі небезпечні `test/echeck-*` (без auth!); додано групу `echeck` (див. нижче).
- `resources/js/api-bridge.js` — секція `Api.echeck.*`.
- `resources/js/router/sidebar-router.js` — пункт меню `echeck` (`permissions: 'echeck-read'`).
- `resources/js/router/custom-routes.js` — роут на `EcheckPage`.
- `lang/uk/base.php`, `lang/en/base.php` — ключ `base.echeck` (лейбл меню).

### Нові (??)
- `app/Entities/Tenant/EcheckShiftLog.php`, `EcheckReceipt.php` — Eloquent-моделі логів.
- `app/Http/Controllers/Api/System/EcheckController.php` — 8 endpoints.
- `database/migrations/2026_07_06_000001_create_echeck_shift_logs_table.php`
- `database/migrations/2026_07_06_000002_create_echeck_receipts_table.php`
- `database/migrations/2026_07_06_000003_add_echeck_permissions.php` — точковий insert `echeck-read`/`echeck-manage` (guard `api`), прив'язка до ролей `admin`/`superAdmin`. ⛔ НЕ сідер.
- `lang/{uk,en,ru}/echeck.php` — UI-переклади (laravel-vue-i18n, ключі `echeck.*`).
- `resources/js/views/base/echeck/` — 5 компонентів: `EcheckPage.vue` (4 таби), `EcheckShiftWidget.vue`, `EcheckCandidates.vue`, `EcheckShiftHistory.vue`, `EcheckReceiptsHistory.vue`. Options API (стиль сусідів), Swal + спінери, gate `hasPermission('echeck-manage')`.

### Endpoints (усі `/api/echeck`, `auth:api` + permission)
```
GET  /echeck/shift/status            echeck-read   {status,opened_at,closed_at,message}
GET  /echeck/shift/history           echeck-read
GET  /echeck/candidates?tab=pending|sold&date_from&date_to&q&page   echeck-read
GET  /echeck/receipts                echeck-read
POST /echeck/shift/open              echeck-manage  (Cache::lock, no-op якщо OPEN)
POST /echeck/shift/close             echeck-manage  (+z-report)
POST /echeck/candidates/{ticket}/send    echeck-manage  (SendEcheckSmsJob::dispatchSync force=true)
POST /echeck/receipts/{order}/cancel     echeck-manage  (ReceiptCancelJob::dispatchSync)
```

## Ключові технічні деталі / нюанси
- **Критерій «квиток підпадає»** = scope `Ticket::pendingEcheck()` (Ticket.php ~358-366): `(seat_payment=true OR status IN [booked,prebooked]) AND status!=sold AND checked=true`. `sold` фіскалізуються автоматично Portmone.
- **dispatchSync** блокує HTTP до ~20с при недоступному e-check — очікувано для синхронного режиму, фронт показує спінер, повертає `{success:false, message}` (не 500).
- **retry лише для GET** — свідоме рішення проти дублювання фіскальних POST.
- `user_id` FK → таблиця **`members`** (не `users`; Passport provider = Member).
- `echeck_receipts.order_id` = `cascadeOnDelete`.

## ⏭️ Що ще треба зробити (для продовження)
1. **Запустити міграції** (рішення власника): `php artisan migrate` — 3 нові міграції. Без них модуль недоступний (немає прав/таблиць). ⛔ БЕЗ `--seed`.
2. **Перевірити frontend build**: `npm run build` (або `dev`) — компоненти НЕ збирались, можливі помилки компіляції Vue/шляхів.
3. **CSS/стилі**: класи `echeck-*`, бейджі статусу, анімація спінера — зараз без стилів (виглядає сиро). Додати SCSS-партіал.
4. **Backend тести (PHPUnit feature)**: на 8 endpoints — happy path + edge (зміна закрита/timeout, немає прав, скасування→повторна відправка, дублікат number).
5. **Валідація параметрів** GET (`tab`, дати, `per_page`) — зараз інлайн/відсутня; додати Form Request або guard.
6. **Edge-кейси до тестів**: квиток без ордера; дублікати `number`; ордер із вже наявним `echeck_id` (idempotent-hit → новий receipt не пишеться); z-report повільніший за 20с.
7. **Опційно**: forget кешу токена при 401; глобальна серіалізація продажів (зараз send/cancel не під `echeck-shift` локом, покладаються на `echeck_id`+lockForUpdate).

## Пов'язані нотатки
- [[project_echeck_fiscal]] — базова система фіскальних чеків (T0-T10, dry-run)
- [[project_echeck_station_close_bug]] — pendingEcheck vs includedInEcheck
- [[project_sms_templates_refactor]] — TicketNotificationService, AlphaSms
