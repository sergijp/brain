---
title: "Проект: onchul — чистка ролей і прав + ReportForm"
date: 2026-06-15
tags: [onchul, work, session, permissions, roles, spatie, crud]
category: session
project: onchul
status: completed
aliases: []
pinecone_indexed: false
---

# onchul — чистка ролей, прав та ReportForm

## Мета сесії
Навести лад у системі доступів: лишити мінімум ролей, повикидати «мертві» та непотрібні права з сідерів/перекладів, гарантувати, що адмін завжди має повний доступ, і почистити форму звітів `ReportForm`.

## Виконано

### 1. Ролі — лишилось рівно 5
Прибрано `superAdmin`, `manager`, `driver`. Залишилось: **admin, agent, operator, api, client**.
- `database/seeders/RolesTableSeeder.php` — оновлено мапу ролей (`admin` → всі права, решта порожні).
- Туди ж додано **ідемпотентне призначення ролі `admin` користувачу `admin@visson.com`** — щоб після обнулення `model_has_roles` адмін не втрачав доступ.

### 2. Механізм «адмін має все»
`app/Providers/AuthServiceProvider.php:32` — `Gate::before(fn($member) => $member->hasRole('admin') ? true : null)`. Будь-який юзер з роллю `admin` проходить усі перевірки. Тому ключове — щоб адмін-юзер мав роль `admin` (це й робить RolesTableSeeder).

### 3. Канонічне джерело прав
`PermissionsTableSeeder` будує права з `lang/uk/permissions.php` (фільтр `is_string`, ігнорує вкладені `group`/`role`). Тому чистка прав = редагування `lang/uk/permissions.php` (+ `lang/en` для перекладів). `MemberTableSeeder` — legacy, у `DatabaseSeeder` НЕ викликається.

### 4. Видалені права (з lang uk+en)
- **9 груп фіч** (раніше): agencies, bus-owners, carriers, dashboard, discount-routes, documentations, fuel-tariffs, outside-systems, social-networks + `full_refund`.
- **11 мертвих trips-прав**: trips-management(+station-uncheck/add-ticket/change-ticket-status), trips-tab-activities, routes-tab-activities, trips-tab-trip-agents-close, trips-delay, trips-passengers-list, trips-report-driver, trips-send_all_sms.
- **6 «робочих» trips-прав** (фічі не потрібні): trips-copy, trips-toggle-active, trips-toggle-archive, trips-send-all-ticket-to-email, routes-download-excel-price, trips-download-excel-price.
- **Уся група tickets-cancelled-*** (10 ключів — фіча взагалі не реалізована) + `tickets-only-sold` + `tickets-send-ticket-sms`.
- **Системні сповіщення** (`system_notifications-*`, 4 ключі + group).
- **Експрес бронювання** (`simplebooking`, `simplebooking-show` + group) — `booking` лишено.
- **Тарифи** (`tariffs-*`, 5 ключів + group) — повністю нереалізована фіча.
- **Звіти**: весь мертвий блок `reports-generate-types-*` + `reports-generate-visible-*` (uk 12, en 10). `reports-generate` і `reports-read` лишено (живі).
- **Драйверські**: `drivers-dashboard-send-btn`, `drivers-finish-station` (мертві).

**Підсумок:** з ~308 прав лишилось **252**.

### 5. Фронтенд-навігація (раніше)
Прибрано роут `documentations` з `crud-routes.js` і 7 записів у `breadcrumbs.js` (fuel-tariffs, outside-systems, bus-owners, carriers, social-networks, agency, documentations). Бекенд (контролери/entities) свідомо НЕ чіпали — фічі недосяжні з UI.

### 6. ReportForm.vue — почищено
Залишилось лише: **вибір дати, вибір маршруту, checkbox «Оплата при посадці», кнопки** (+ таблиця прев'ю). Прибрано 3 типові dropdown-и (`types`, `types_client`, `types_route`), відповідні `data()` props, метод `getTypes()` + виклик у `mounted()`, і параметри `type/type_client/types_route` з payload `getReport`/`getPreviewReport`. Бекенд `ReportsController::generate` має дефолти (`type='default'`, `type_client='default'`, `types_route=null`), тож звіт працює як «Звичайний».

## Важливі рішення (ADR)

| Рішення | Чому |
|---------|------|
| Ролі тільки 5 | Спрощення моделі доступів |
| Призначення `admin`-ролі в RolesTableSeeder | Щоб ресет не позбавляв адміна доступу |
| Чистити права через `lang/uk/permissions.php` | Це канонічне джерело для `PermissionsTableSeeder` |
| Видаляти лише lang-ключі, код кнопок/методів лишати | За домовленістю з користувачем — код не чіпаємо, кнопки ховаються бо право не сідиться |
| ReportForm: не слати type-параметри, покластись на бекенд-дефолти | Мінімальна зміна, звіт лишається робочим |

## Метод дослідження «де і на що впливає»
Ключове — **динамічна збірка прав**:
- Кнопки CRUD: `ButtonManager.vue` → `${crud}-${permission||type}` (літералу в коді може не бути).
- Таби: `EntityMixin.js` → `permissionTabs` (⚠️ бекенд його НЕ заповнює → усі таби видно всім, гейтинг `*-tab-*` мертвий).
- Поля/колонки: перевіряють `field.permission` напряму.
Тому grep по точному ключу часто нічого не знаходить — треба грепати й часткові підрядки + дивитись контролер/Vue.

## Ресет-флоу (повторюваний)
```bash
php artisan tinker --execute="
use Illuminate\Support\Facades\{DB,Schema};
Schema::disableForeignKeyConstraints();
collect(['role_has_permissions','model_has_roles','model_has_permissions','roles','permissions'])->each(fn(\$t)=>DB::table(\$t)->truncate());
Schema::enableForeignKeyConstraints();
app(\Spatie\Permission\PermissionRegistrar::class)->forgetCachedPermissions();
"
php artisan db:seed --class=PermissionsTableSeeder
php artisan db:seed --class=RolesTableSeeder
```

## Артефакти
- `database/seeders/RolesTableSeeder.php` — мапа ролей + призначення admin-юзеру
- `lang/uk/permissions.php`, `lang/en/permissions.php` — чистка прав
- `resources/js/router/crud-routes.js`, `resources/js/config/breadcrumbs.js` — навігація
- `resources/js/components/reports/ReportForm.vue` — спрощена форма звітів

## Відомі залишки / ризики
- Висячі breadcrumb-и/посилання на видалені фічі (`tariffs.list`, `simplebooking`, `LoginForm` редіректи) — код не чіпали.
- Бекенд-методи `copyEntity/toggleActive/toggleArchive`, кнопки SMS/excel-price — лишилися, але кнопки сховані (права не сідяться).
- ⚠️ Системний баг: гейтинг табів через `permissionTabs` не реалізований у бекенді — усі таби видно всім (фікс відклали).
- `tickets-can-add-from-another-user` — РОБОЧЕ право (поле «інший користувач» у `BookPlacesForm.vue:101`), лишили.

## Пов'язані нотатки
- [[onchul]]
