---
title: "Проект: buktrek — модуль «Розсилки» перевізникам/замовникам"
date: 2026-10-07
tags: [buktrek, work, session]
category: session
project: buktrek
status: completed
aliases: []
pinecone_indexed: false
---

# Модуль «Розсилки»

## Мета сесії
Новий пункт меню: тема + текст листа (HTML-редактор), вибір перевізників або замовників, Swal «Ви впевнені?» перед відправкою, права.

## Виконано
- Бекенд: `GET /api/system/mailings/recipients?type=carriers|customers` (`can:mailings-read`), `POST /api/system/mailings/send` (`can:mailings-send`) → `App\Http\Controllers\Api\System\MailingController`.
- `App\Services\Mailing\MailingService` — одне джерело списку для фронту і відправки: тільки `active = true`, сортування за `legal_name`, `parseEmails()` ділить поле email за `, ; пробіл` і бере лише валідні.
- `SendMailingJob` (Redis/Horizon, tries 3, backoff 60) — одна джоба на адресу; пише в `email_history` (`application_id = null`, тема `Розсилка (Тип): тема`) **після** успішної відправки.
- `MailingMail` + `resources/views/emails/mailing.blade.php`.
- Права `mailings-read`, `mailings-send` — міграція `2026_10_07_000001_add_mailings_permissions.php` (forceCreate) + запис у `PermissionsTableSeeder`, переклади в `lang/uk/permissions.php` (група «Розсилки»).
- Фронт: `resources/js/views/base/Mailings.vue`, пункт у `sidebar-router.js` (`icon-mailing`, `public/images/menu-icons/mailing.svg`), крихти, `Api.mailings.*`, переклади `lang/uk/mailings.php`.
- Перевірено: tinker з `Queue::fake` (відсів неактивних/без email/неіснуючих id, дедуп адрес), джоба з array-мейлером + запис історії, UI в браузері (перемикач, «Вибрати всіх», лічильник, Swal → Відміна).

- Друга ітерація «під наш стиль»: контролер наслідує `Controller`, тонкий, docblocks з маршрутами; вся логіка в `MailingService`; окремий `MailingRecipientsRequest`; `MailingRecipientResource`; стилі винесено в `resources/sass/mailings.scss` (токени з `variables.scss`, перемикач = вигляд таб-світчера дашборду), мобільний брейкпоінт у `media.scss`; поля обгорнуто в `field-wrapper`.
- Третя ітерація (відступи/шрифти): сторінка = `.list-view-manager` з шапкою в `.top` (як ListViewManager крутів → ті ж margin-top/gap 12px); пошук — розмітка `search-wrapper` з круту (лупа + хрестик), фільтр живий; список — картка `table-wrapper` з рядком-заголовком у стилі `th` (12px/500/uppercase/$btn-color): чекбокс «вибрати всіх видимих» + «Обрано N з M» замість підкреслених посилань; рядки 5px 10px, назва 14px, email 12px.
- Четверта ітерація: вибір одержувачів винесено в модалку `resources/js/components/mailings/MailingRecipientsModal.vue` (entity-wrapper/header/content/footer, «Відміна» + save-button «Застосувати», локальна копія вибору); на сторінці — картка з чипами (вигляд `.active-filter`) і кнопкою `crud-button > button.create` «Обрати/Змінити»; «Надіслати» = `save-button`; вкладення (до 10 файлів, разом ≤15 МБ — фронт і `SendMailingRequest`), multipart разом із відправкою, `MailingService::storeAttachments()` → `public/uploads/mailings/{md5}.ext`, `MailingMail::attachFromStorageDisk` з оригінальною назвою; `email_history.files` → text (міграція 2026_10_07_000002). `tp()` винесено в `resources/js/mixins/TranslateParams.js`.
- Пастка: всередині `.entity-view-manager` (і `.field-wrapper`) тег `<label>` отримує стиль підпису поля (нижній регістр) — рядки списку й кнопка вкладень зроблені `div`/`button`.
- «Uncaught (in promise)» у консолі є і на /directories — не наше.
- П'ята ітерація — історія: таблиця `mailings` (member_id, type, subject, body, files json, recipients json-знімок, emails_count; міграція 2026_10_07_000003) + `email_history.mailing_id`; `sent_count` = кількість рядків email_history (пишуться після успішної відправки) → «Надіслано N з M». `GET /api/system/mailings/history?page=` (`can:mailings-read`, 20 на сторінку, `has_more`), `MailingHistoryResource`. Фронт: кнопка `crud-button > create` «Історія розсилок» у `.top`, модалка `components/mailings/MailingHistoryModal.vue` на глобальних стилях `.email-history` (як вкладка історії в SendApplicationEmail), «Показати ще».
- Міграції об'єднано: лишилось дві — `2026_10_07_000001_add_mailings_permissions` і `2026_10_07_000002_create_mailings_table` (mailings + email_history.mailing_id + files→text). Задача розсилки йде в чергу `emails` (як app/Mail/*).
- Знахідка: `email_history.files` у реальних даних уже довше 191 символу (968 рядків листів по заявках, JSON з \uXXXX) — колонку колись розширили поза міграціями. Тому `down()` files назад не звужує (впаде з 1406 або обріже дані).
- **Фінал по даних (за рішенням користувача): розсилки повністю відв'язані від `email_history`** — це окрема історія листів по заявках. Уся розсилка в одній таблиці `mailings`: `emails_count`, `sent_count` (атомарний increment у `SendMailingJob::handle`), `failed_count` + `failed_emails` (у `failed()` після 3 спроб, під `lockForUpdate`). Міграція `2026_10_07_000002_create_mailings_table` створює лише `mailings`; `email_history` і `EmailHistory` не змінені. У модалці історії — «Надіслано N з M», «Не доставлено: K» і список адрес.
- **Наскрізна перевірка:** HTTP-стек (403 без прав на всі 3 ендпоінти, 422 на валідацію/ліміти/«немає email», нічого не ставиться в чергу); UI → черга redis → `queue:work` з log-мейлером (тимчасовий перевізник `@example.com`): лист з темою, HTML і PDF-вкладенням з кириличною назвою, `sent_count` 1/1, ретрай після збою спрацював; шлях збою (SMTP на :1) — 3 спроби по 60 с → `failed()` → `failed_emails`. Тестові дані прибрано. Знайдено/виправлено відмінювання: `trans_choice` для «:count лист|листи|листів» і `tpc()` у міксині для «одержувачу/одержувачам».
- Локальні нюанси: `MAIL_FROM_ADDRESS=null` у .env (листи падають «must have From»); у спільному redis у `queues:emails` лежать чужі задачі (OrderTicketsSold) — не обробляти; перший клік автоматизації після завантаження лише фокусує вікно.
- **Прод: лист завис у Pending (черга emails).** Діагностика на сервері: `horizon:status` running, `horizon:supervisors` порожньо; прод `APP_ENV=local` (Horizon мав блок лише `production`); два процеси `artisan horizon`; dev.buktrek.com і прод з `REDIS_PREFIX=null` в одній Redis DB → спільні `queues:*`, `queue:listen` dev забирає `default` прода. Фікс у коді: блок `local` у `config/horizon.php`. Далі на сервері: деплой → `horizon:terminate`, прибрати дубль Horizon, у dev задати власний `REDIS_PREFIX`.

## Важливі рішення (ADR)
| Рішення | Чому |
|---|---|
| Одна таблиця `mailings`, `email_history` не чіпаємо | `email_history` — історія листів по заявках, до розсилок не має відношення; доставку рахують лічильники в самій розсилці |
| Одна джоба на адресу | Погана адреса/збій SMTP не валить усю розсилку |
| Одна розсилка = один тип (перевізники АБО замовники) | Простіше і зрозуміліше; тип пишеться в тему журналу |
| Повторний відбір id на бекенді через той самий сервіс | В листи не потрапить неактивний/видалений запис |

## Проблеми й як вирішили
- `TranslationServiceProvider` перетворює `:count` → `{count}`, а `$t` laravel-vue-i18n їх не підставляє → у компоненті метод `tp()` з ручною заміною `{x}`.
- Глобальний `base.scss` ховає `input[type=checkbox]` без класу `style4` → чекбоксам клас `style4`.
- Store `noty` тримає одне повідомлення — дві нотифікації поспіль затирають одна одну; склеюємо в одну.
- Локально `MAIL_FROM_ADDRESS=null` → Symfony «must have From» (стосується і договорів, не модуля).
- Дані: 15 із 48 замовників без валідного email (null, `111@111`, `ukr.nеt` з кириличною «е»).

## Артефакти
Див. «Виконано». Не закомічено на момент запису.

## Пов'язані нотатки
- [[2026-09-15-direction-costs-crud]] — пастка з PermissionsTableSeeder
