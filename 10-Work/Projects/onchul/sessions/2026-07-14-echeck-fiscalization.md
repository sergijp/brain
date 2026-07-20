---
title: "Проект: onchul — E-check фіскалізація (site-квитки)"
date: 2026-07-14
tags: [onchul, work, session, echeck, fiscalization, portmone]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Дослідити, як зроблено e-check фіскалізацію в проєкті 3g, і реалізувати аналог у onchul: фіскалізувати ТІЛЬКИ квитки, куплені через сайт; чек генерується після підтвердженої оплати Portmone і надсилається на email; автоматичне відкриття/закриття зміни.

## Виконано

| Задача | Результат |
|--------|-----------|
| Дослідження 3g echeck (integration-architect) | ✅ Провайдер e-check, EcheckService, джоби (SendEcheckSmsJob/Shift/Cancel), shift-cron, site-vs-admin розрізнення через CLIENT_EMAIL member |
| Реалізація config/services.php, .env.example | ✅ ECHECK_ENABLED=false, ECHECK_DRY_RUN=true; лог-канал |
| EcheckService (login/token-cache, shift, receipt, Z-звіт) | ✅ app/Services/Echeck/EcheckService.php; transportGuardResponse |
| Джоби (SendReceipt, ShiftOpen/Close, Cancel) | ✅ app/Jobs/Echeck/; reconcile-command |
| Entities (EcheckReceipt, EcheckShiftLog) + міграції | ✅ Створено; НЕ запущені (待 креденшіали) |
| Хук: Portmone→EcheckSendReceiptJob | ✅ PortmonePaymentConfirmationService::confirm() + afterCommit(); site-only gate |
| Сторно: EcheckReceiptCancelJob на ReturnTicket | ✅ Успішна refund → CancelJob::dispatch() |
| Scheduler (00:05 open / 23:55 close) + Cache::lock | ✅ Імплементовано |
| Quality Gate (tester + reviewer + security-scanner) | ✅ 13 юніт EcheckService, Http::fake; раунд фіксів |
| Раунд фіксів (C1, H1, M1-2, I2-4) | ✅ Частковий refund, ключ-шлях, Z-звіт, fillable, dry-run guard, race-lock, reconcile |
| Парити-аудит 3g↔onchul | ✅ Перенесення нюансів підтверджено; відкриті пункти документовані |
| Runtime-верифікація (boot/wiring/dry-run/route/schedule) | ✅ 43/43 тестів PASS; міграції --pretend не застосовані |
| Документація (PORTMONE.md, ECHECK.md) | ✅ 17KB + 24KB; кореневі файли проєкту |

## Важливі рішення (ADR)

| Рішення | Чому | Альтернативи |
|---------|------|--------------|
| E-check — окремий акаунт для onchul (не спільний з 3g) | Ізоляція; легше тестувати/скидати без впливу на іншу систему | Спільний акаунт (складніше управляти) |
| Фіскалізація ТІЛЬКИ site-замовлень (member_id === CLIENT_EMAIL member) | Нема адмін-кабінету/водія; нема sense фіскалізувати внутрішні операції | Фіскалізувати всі канали (надто широко) |
| Чек — після підтвердженої оплати Portmone; EMAIL-доставка | В ончулі нема SMS; чек = доказ платежу клієнту | SMS (у 3g; у onchul неможливо) |
| Одна каса (як 3g); зміна авто по cron | Спрощена логіка; нема потреби в ручному UI в даний момент | Багато кас; ручне open/close |
| Inert за замовчуванням: ECHECK_ENABLED=false + ECHECK_DRY_RUN=true | Двійний guard; безпека при розроблянні; не атакує реальну касу | Live за замовчуванням (небезпечно) |

## Проблеми й як вирішили

| Проблема | Статус | Рішення / Follow-up |
|----------|--------|-------------------|
| 🔴 **Трансферні квитки (fiscal_price)** | Открытый/Потребует проверки | onchul не має fiscal_price accessor (3g має); трансфер-друге-плече = окремий Order з price=0 → zero-filter відкидає. Безпечно ЛИШЕ якщо ціна першого плеча = повний through-fare. **ПОТРІБЕН ТЕСТ трансфер-бронювання.** |
| Частковий refund: дубль vs. сторно | Interim (деferred) | Чек на замовлення, сторно на квиток → інтерим (не анулювати весь чек при частковому; `partial_return_deferred`). Повне рішення потребує верифікації API. |
| Успадкований риск дубля чека | Documented | createReceipt ок, save падає до запису echeck_id → ретрай дублює. Потрібен idempotency-key або remote-check (待 staging-тест). |
| Немає ручного open/close адмін-UI | Scheduled | Лише cron 00:05/23:55. (3g має EcheckController для manual.) Раунд 2: UI за потребою. |
| Джоби/reconcile без feature-тестів | Documented | Лише 13 юніт на EcheckService. **Feature-тести**: трансфер-ціна, dry-run cancel, reconcile, webhook→SOLD→echeck. |

## Follow-up до продакшену

1. **Креденшіали e-check** → окремий акаунт; ключ у `storage/app/echeck/` (НЕ public) → `.env` → `config:cache`
2. **Міграції** → `php artisan migrate` (3 нові: echeck_receipts, echeck_shift_logs, orders-cols)
3. **Feature-тести** → трансфер-ціна, dry-run cancel, reconcile-reconcile, Portmone webhook → SOLD → echeck
4. **Staging-тест** → ECHECK_DRY_RUN=false, ENABLED=true → повна verifikacija
5. **Портмоне-міграція** теж чекає креденшіали (див. попередню нотатку [[2026-07-13-portmone-gateway-migration]])

## Артефакти

**Нові файли (working tree, dev branch, НЕ закомічено):**
- `app/Services/Echeck/EcheckService.php`
- `app/Jobs/Echeck/EcheckSendReceiptJob.php`
- `app/Jobs/Echeck/EcheckShiftOpenJob.php`
- `app/Jobs/Echeck/EcheckShiftCloseJob.php`
- `app/Jobs/Echeck/EcheckReceiptCancelJob.php`
- `app/Console/Commands/ReconcileEcheckReceipts.php`
- `app/Mail/Echeck/EcheckReceiptMail.php`
- `resources/views/emails/echeck/receipt.blade.php`
- `app/Entities/EcheckReceipt.php`
- `app/Entities/EcheckShiftLog.php`
- `database/migrations/XXXX_XX_XX_create_echeck_receipts_table.php`
- `database/migrations/XXXX_XX_XX_create_echeck_shift_logs_table.php`
- `database/migrations/XXXX_XX_XX_add_echeck_columns_to_orders_table.php`
- `config/services.php` (echeck-блок)
- `tests/Unit/EcheckServiceTest.php` (13 юніт)
- `PORTMONE.md` (17KB)
- `ECHECK.md` (24KB)

## Пов'язані нотатки

- [[2026-07-13-portmone-gateway-migration]] — Portmone — база, куди хукається фіскалізація; webhook → PortmonePaymentConfirmationService::confirm() → EcheckSendReceiptJob
