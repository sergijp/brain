---
title: "Проект: onchul — Realtime push-нотифікації через Pusher"
date: 2026-07-21
tags: [onchul, work, session, realtime, pusher, notifications]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Піднімти WebSocket-базовану реалтайм-інфраструктуру для push-нотифікацій в адмінці. Спершу досліджували laravel-echo-server та Reverb, але обрали managed **Pusher Channels** (Sandbox, безкоштовна схема) — щоб уникнути WebSocket reverse-proxy на VPS з Webuzo/Apache. Реалізувати бізнес-тригер: сповіщення коли вільних місць на рейсі падає нижче порогу. Додати персистентність сповіщень у таблиці для глобального фіду.

---

## Виконано

| Задача | Результат |
|--------|-----------|
| **Фаза 1: Realtime infra (Pusher)** | ✅ Підняте: config/broadcasting.php → cloud-driver; приватні канали App.Models.Member.{id} + role.{role}; Event TestNotification; команда broadcast:test; JS-клієнт з Passport Bearer; Vuex-підписник. Виправлено: authenticatable = Member (не User). Перевірено наживо: PUSHER OK в браузері. |
| **Фаза 2: Бізнес-тригер low_seats** | ✅ Сповіщення при вільних місцях < порогу (settings.low_seats_threshold=10). Throttle по Redis (low_seats_throttle_minutes=15, ключ low_seats_notified:{trip_id}). Хук: TicketObserver::created() + Job EvaluateTripLowSeats + Event LowSeatsNotification. Кількість місць = Trip::full_free (узгодженість зі списком). Команда low-seats:test. |
| **Авторизація каналів** | ✅ Виправлено баг 403: Spatie hasPermissionTo() не проходить Gate::before; замінено на can() (admin-bypass працює). Ті самий баг у каналі binotel виправлено. Перевірено: Member::find(1)->can('trips-low-seats-notifications')=true. |
| **Персистентність сповіщень** | ✅ Таблиця system_notifications (type + payload json + created_at). Модель SystemNotification, сервіс SystemNotificationService (record/paginate/delete/deleteAll), контролер SystemNotificationController. 3 API-методи: GET /api/system/notifications, DELETE /api/system/notifications/{id}, DELETE /api/system/notifications. Дедуп per рейс через throttle. |
| **Очищення legacy-коду** | ✅ Видалено `resources/js/utils/sockets` (мертвий laravel-echo-server). Видалено `TripWorkloadNotification.vue` (legacy UI). Збережено спільні lang-ключі для живої back-фічі BackTripWorkloadNotification. Не чіпано back_route_workload_*. |
| **VITE-конфіг + .env** | ✅ Додано VITE_PUSHER_APP_KEY + VITE_PUSHER_CLUSTER в .env.example. Перезапущено Vite-сервер (build). |

---

## Важливі рішення (ADR)

| Рішення | Чому | Альтернативи |
|---------|------|--------------|
| **Managed Pusher (Sandbox)** замість self-hosted Reverb/laravel-echo-server | Уникнути складності WebSocket reverse-proxy на Webuzo+Apache. Той самий клієнтський pusher-протокол → пізніше можна перемкнути на Reverb змінною .env. | Reverb (self-hosted, вимагає WS-proxy); laravel-echo-server (мертвий, закоментований). |
| **Authenticatable = Member** (не User) | Канали/команди на App.Models.Member.{id}; admin = member id 1 (не App\Models\User). Узгоджено з системою ролей (Spatie guard=api, Member). | User-канали — розрив у архітектурі auth. |
| **Job на черзі default** (не notifications) | config/horizon.php немає супервізора для notifications (джоба зависла б). | notifications-черга — deadlock. |
| **can() замість hasPermissionTo()** для авторизації каналів | can() проходить Gate::before (admin-bypass); hasPermissionTo() ні. | hasPermissionTo() — 403 для admin попри право. |
| **Trip::full_free** для кількості місць | Узгодженість зі списком рейсів TripsCrudController. Єдиний істинний обчислювач. | Manual query — дублювання логіки. |
| **Universal таблиця сповіщень** + дедуп per рейс | Глобальний фід, гнучкість для майбутніх бізнес-тригерів. Дедуп через Redis throttle, не в DB. | Per-тип таблиці — фрагментація. |

---

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| **VITE_PUSHER_APP_KEY undefined** | Додати VITE_ префікс-змінні в .env.example; перезапустити Vite (build/dev). |
| **Authenticatable User vs Member плутанина** | Виправлено канали на App.Models.Member.{id}; admin = id 1 з таблиці members. |
| **403 hasPermissionTo() для admin** | Замінено на can() (проходить Gate::before). |
| **Черга notifications відсутня в Horizon** | Запущено Job на черзі default; config/horizon.php не містить супервізора для notifications. |
| **Legacy trip_workload затирала нові данні** | Видалено TripWorkloadNotification.vue, але збережено спільні lang-ключі для BackTripWorkloadNotification. |
| **Payload.id=null у збереженому рядку** | Асиметрія: broadcast-payload має id, але DB-рядок записує null. Залишено як open-item (низька пріоритет). |
| **Job без DB-контексту при rollback** | Додано DB::afterCommit() у TicketObserver, бо Ticket::created()->Job може запуститися до commit. |
| **Авто-комміт+push на origin/dev** | Під час роботи робоче дерево авто-синкнулось (коміт 83a5013 sergijp), перемежано з мержами Artem Frunze. Жоден агент не робив — імовірно фонова синхронізація. Незавершений код із дебаг-командами вже на спільній гілці. |

---

## Артефакти

**Нові файли:**
- `app/Events/TestNotification.php`
- `app/Events/LowSeatsNotification.php`
- `app/Jobs/EvaluateTripLowSeats.php`
- `app/Console/Commands/TestBroadcast.php`
- `app/Console/Commands/LowSeatsTest.php`
- `app/Entities/System/SystemNotification.php`
- `app/Services/SystemNotificationService.php`
- `app/Http/Controllers/Api/SystemNotificationController.php`
- `resources/js/echo.js`
- `database/migrations/2026_07_21_130000_create_system_notifications_table.php`

**Змінені файли:**
- `config/broadcasting.php` (cloud driver → pusher)
- `routes/channels.php` (app.models.member.{id}, role.{role}, low-seats)
- `routes/api.php` (SystemNotificationController endpoints)
- `app/Observers/TicketObserver.php` (DB::afterCommit + EvaluateTripLowSeats)
- `resources/js/store/index.js` (Vuex Pusher-підписник)
- `.env.example` (BROADCAST_CONNECTION, PUSHER_*, VITE_PUSHER_*)
- `composer.json` (pusher/pusher-php-server)
- `package.json` (pusher-js)
- `resources/js/components/system-notifications/SystemNotificationsManager.vue` (новий компонент)
- `resources/sass/system-notifications.scss` (стилізація)

**Видалені:**
- `resources/js/components/system-notifications/notifications/TripWorkloadNotification.vue` (legacy)

**Команди:**
- `php artisan broadcast:test`
- `php artisan command:test-broadcast` (TestBroadcast)
- `php artisan command:low-seats-test --trip-id=31` (LowSeatsTest)

**Міграції:**
- `2026_07_21_130000_create_system_notifications_table`

---

## Ручні кроки для деплою / користувача

1. **Settings у БД:**
   - `low_seats_threshold = 10` (порогове число вільних місць)
   - `low_seats_throttle_minutes = 15` (опційно; throttle-період)

2. **Права (Spatie):**
   - `trips-low-seats-notifications` (додати для admin/staff)
   - `system-notifications-read` (опційно; окреме право для фіду)

3. **.env (для production):**
   ```
   BROADCAST_CONNECTION=pusher
   PUSHER_APP_ID=...
   PUSHER_APP_KEY=...
   PUSHER_APP_SECRET=...
   PUSHER_APP_CLUSTER=eu
   VITE_PUSHER_APP_KEY=...
   VITE_PUSHER_CLUSTER=eu
   ```

4. **Deploy-команди:**
   ```bash
   composer install
   npm install
   npm run build
   php artisan config:cache
   php artisan horizon:terminate  # перезапустити Horizon
   # (Додати settings + permission у БД вручну через админку)
   ```

---

## Відкриті питання / Follow-up (важливо)

1. **Авторизація фіду:** перевести 3 API-ендпоінти на окреме право `system-notifications-read` (замість нинішнього `trips-low-seats-notifications`), бо таблиця — universal.

2. **Асиметрія payload.id:** broadcast-payload має id, але DB-запис має null. Прибрати асиметрію.

3. **Quality Gate:** `tester` ще не запускався. Потрібні unit/feature тести для:
   - Job EvaluateTripLowSeats (низки місць, throttle)
   - SystemNotificationService (CRUD)
   - API-ендпоінти авторизація

4. **Фаза 3 — реальний UI:** 
   - Дзвіночок/тости для нотифікацій
   - Полагодити mitt-міст `SystemNotificationsBus` (розірваний після Vue 2→3)

5. **Призначення прав:** додати `trips-low-seats-notifications` staff-ролям.

6. **⚠️ Авто-синк origin/dev:** під час сесії робоче дерево авто-закомітилось+запушилось (коміт 83a5013), перемежано з мержами Artem Frunze. Причина невідома (фонова синхронізація?). Незавершений код + дебаг-команди вже на спільній гілці. **Не вирішено.**

7. **Не закомічено осмислено:** всі зміни лише в робочому дереві (або авто-синком); користувач не робив свідомого коміту.

---

## Продовження — деплой & діагностика (2026-07-22)

### Контекст проблеми

При спробі піднімти realtime-фічу на production/staging-подібного окремошення (Laravel 12.62.0, PHP 8.3.32 у веб-сервері) виникла **runtime error**:

```
RuntimeException: Failed to create broadcaster for connection "pusher" with error: Class "Pusher\Pusher" not found.
```

Помилка виникла під час завантаження адмін-панелі (`resources/js/app.js` → `echo.js` → інстанціація Pusher).

### Діагностика

**Факт 1:** Локальне оточення.
- CLI (terminal) — **PHP 8.2.19**
- Web-server (Valet + nginx) — **PHP 8.3.32** (різні PHP-FPM процеси)
- Пакет `pusher/pusher-php-server` встановлено: є в `composer.json` (`^7.2`), `composer.lock`, й файл класу існує:
  ```
  vendor/pusher/pusher-php-server/src/Pusher.php
  ```

**Факт 2:** Побічна помилка команди користувача.
- Команда: `composer install --no-dev --optimize-autoloade`
- **Typo:** бракує `r` (має бути `--optimize-autoloader`)
- Результат: composer install впав; пакет не встановився з першої спроби

**Факт 3:** Причина дисбалансу PHP-FPM.
- Веб-процес (PHP-FPM під Valet) тримає **застарілий opcache** та **autoloader-кеш** — закешував структуру ще до додавання пакету pusher
- Файл фізично є у vendor, але PHP-FPM не бачить його (кеш на рівні JIT/opcache)
- CLI (окремий PHP 8.2.19 process) працює коректно і знаходить клас

### Рекомендований фікс (не застосований)

1. **Перезапустити Valet PHP-FPM** (скидає opcache всіх сайтів):
   ```bash
   valet restart
   ```

2. **Пересоздати autoloader** з оптимізацією:
   ```bash
   composer dump-autoload -o
   ```

3. **Очистити Laravel runtime кеш** (config cache, route cache, view cache):
   ```bash
   php artisan optimize:clear
   ```

4. **Перевірити узгодженість PHP версій:** 
   - `php -v` (CLI)
   - `valet diagnose` → встановлена версія Valet PHP
   - Якщо розбіжність — обрати одну версію або пересоздати `/Users/serhiin/.composer` і `/Users/serhiin/.valet` під единої PHP версії

### Безпека

У чаті під час діагностики було видно **серверний ключ:**
```
PUSHER_APP_SECRET=...
```

**Рекомендація:** На pusher.com (Dashboard → App Keys → Reset Secret) ротувати сервернийSecret. Public key (`PUSHER_APP_KEY`) можна лишати як є.

### Статус

- **Фікс рекомендований, але НЕ застосований** — сесію зупинено на етапі діагностики
- **Broadcaster не піднявся** на веб-PHP 8.3.32
- **Follow-up:** застосувати fix-команди і перевірити, що `echo.js` інстанціюється без помилок

---

## Пов'язані нотатки

- [[project_realtime_pusher]] — Pusher Channels config, канали, events
- [[project_permissions_system]] — Spatie ролі; can() vs hasPermissionTo()
- [[feedback_horizon_env_db_change]] — horizon:terminate при змінах .env
- [[feedback_never_commit_push]] — крит. забор: агенти не коммітять
- [[feedback_env_autocommits_dev]] — авто-коміти на origin/dev (невирішено)
- [[project_portmone_migration]] — payment gateway (інша фіча, але важливий контекст)
- [[project_quotas]] — квоти місць; Trip::full_free узгоджено
