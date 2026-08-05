---
title: "3g — Modularization Design (варіант b)"
date: 2026-08-05
tags: [3g, work, architecture, modules]
category: architecture
project: 3g
status: draft
aliases: ["3g-modularization", "3g-modules"]
pinecone_indexed: false
---

# 3g — Modularization Design

Детальний дизайн розбиття 3g на **базову систему (CORE) + модулі** за варіантом **(b) — власний легкий реєстр**.

**Версія:** 0.1 (дизайн, реалізація не почата)
**Статус:** draft → implementation Fase-0
**Посилання на детальний план:** `/Users/serhiin/Data/Source/3g/Extraxct_Modules.md`

---

## Обраний варіант: Легкий реєстр (b)

| Критерій | Оцінка |
|----------|--------|
| Залежність від фреймворку | Мінімальна (власний PHP код) |
| Контроль CRUD/sidebar/lang | Повний |
| Простота вимкнення модуля | Так (disable в config) |
| Поштучна міграція | Так |
| Складність реалізації | ~40-60 годин Fase-1 |

**Альтернативи (відхилено):**
- **(a) nwidart/laravel-modules** — не розуміє CRUD-фреймворк, sidebar, DB-переклади
- **(c) composer monorepo** — важкий tooling, розсипання репо
- **(d) feature-flags** — можливий як Fase-0 (швидкий прототип без структури)

---

## Структура модуля app/Modules/{Name}/

```
app/Modules/Echeck/
├── ModuleServiceProvider.php          # Реєстрація в ядру
├── module.php                         # Маніфест (назва, опис, версія, залежності)
├── Entities/
│   ├── EcheckTicket.php              # Eloquent модель
│   └── EcheckSession.php
├── Http/
│   └── Controllers/
│       └── EcheckCrudController.php   # CRUD-розширення
├── Crud/
│   └── ... (поля, операції)          # CRUD-конфігурація (якщо не в Controller)
├── Services/
│   ├── EcheckService.php
│   └── EcheckReportService.php
├── Jobs/
│   ├── SendEcheckSmsJob.php
│   └── EcheckHeartbeatJob.php
├── Events/
│   └── EcheckSessionCreated.php
├── Observers/
│   └── EcheckTicketObserver.php
├── Commands/
│   └── TestEcheckConnectionCommand.php
├── Listeners/
│   └── HandleEcheckEvent.php
├── lang/
│   ├── uk/echeck.php                 # trans('echeck::echeck.field_name')
│   └── en/echeck.php
├── resources/                         # Vue компоненти, стилі
│   └── js/components/
│       └── EcheckReport.vue
├── routes/
│   └── api.php                        # registerRoutes(Router $router) функція
├── database/
│   ├── migrations/
│   │   └── 2026_08_05_create_echeck_sessions_table.php
│   └── factories/
│       └── EcheckSessionFactory.php
├── tests/
│   ├── Unit/EcheckServiceTest.php
│   └── Feature/EcheckCrudTest.php
├── config/
│   └── echeck.php                     # config('modules.echeck.*')
└── README.md                          # Модульна документація
```

### ModuleServiceProvider (обов'язковий)

```php
namespace App\Modules\Echeck;

use Illuminate\Support\ServiceProvider;

final class ModuleServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        // 1. Реєстрація маршрутів
        if (function_exists('registerRoutes')) {
            registerRoutes(new Router());
        }

        // 2. Перекладання
        $this->loadTranslationsFrom(__DIR__.'/lang', 'echeck');

        // 3. Міграції
        $this->loadMigrationsFrom(__DIR__.'/database/migrations');

        // 4. CRUD-контролери
        $this->registerCrudControllers();

        // 5. Меню-елементи (sidebar)
        $this->registerSidebarItems();

        // 6. Спостерігачі моделей
        EcheckTicket::observe(EcheckTicketObserver::class);
    }

    public function register(): void
    {
        // Сервіси як singleton
        $this->app->singleton(EcheckService::class);
    }

    private function registerCrudControllers(): void
    {
        ModuleRegistry::registerCrudController(
            EcheckTicket::class,
            EcheckCrudController::class
        );
    }

    private function registerSidebarItems(): void
    {
        ModuleRegistry::registerSidebarItem([
            'icon'   => 'icon-receipt',
            'label'  => trans('echeck::menu.fiscal_checks'),
            'route'  => 'crud.echeck.index',
            'policy' => 'echeck-read',
        ]);
    }
}
```

### module.php (маніфест)

```php
return [
    'name'        => 'Echeck',
    'description' => 'Fiscal electronic checks integration',
    'version'     => '1.0.0',
    'author'      => '3G Team',
    'enabled'     => env('MODULE_ECHECK_ENABLED', true),
    'dependsOn'   => ['notifications'], // Модулі-залежності
    'provides'    => [
        'echeck'    => EcheckService::class,
        'echeck-db' => EcheckRepository::class,
    ],
];
```

---

## ModuleRegistry — центральна точка управління

### config/modules.php

```php
return [
    'auto_discovery' => true,  // Автопошук у app/Modules/*/ModuleServiceProvider.php

    'modules' => [
        'echeck' => [
            'enabled'    => env('MODULE_ECHECK_ENABLED', true),
            'dependsOn'  => ['notifications'],
        ],
        'surveys' => [
            'enabled'    => env('MODULE_SURVEYS_ENABLED', true),
            'dependsOn'  => [],
        ],
        // ...
    ],

    'registered' => [], // Заповнюється на runtime ModuleRegistry
];
```

### ModuleRegistry (singleton в app/Services/)

```php
namespace App\Services;

use Illuminate\Support\Collection;

final class ModuleRegistry
{
    private static ?self $instance = null;
    private Collection $modules;
    private Collection $crudControllers;
    private Collection $sidebarItems;

    private function __construct()
    {
        $this->modules = collect();
        $this->crudControllers = collect();
        $this->sidebarItems = collect();

        $this->discover();
    }

    public static function getInstance(): self
    {
        return self::$instance ??= new self();
    }

    public function discover(): void
    {
        $config = config('modules.modules', []);

        foreach ($config as $name => $settings) {
            if ($settings['enabled'] ?? true) {
                $this->validateDependencies($name, $settings['dependsOn'] ?? []);
                $this->modules->put($name, $settings);
            }
        }
    }

    private function validateDependencies(string $moduleName, array $dependsOn): void
    {
        foreach ($dependsOn as $dep) {
            if (!($config['modules'][$dep]['enabled'] ?? false)) {
                throw new ModuleDependencyException(
                    "Module [$moduleName] requires [$dep] to be enabled."
                );
            }
        }
    }

    public function registerCrudController(string $modelClass, string $controllerClass): void
    {
        $this->crudControllers->put($modelClass, $controllerClass);
    }

    public function getCrudController(string $modelClass): ?string
    {
        return $this->crudControllers->get($modelClass);
    }

    public function registerSidebarItem(array $item): void
    {
        $this->sidebarItems->push($item);
    }

    public function getSidebarItems(): Collection
    {
        return $this->sidebarItems;
    }

    public function isEnabled(string $moduleName): bool
    {
        return $this->modules->get($moduleName, false);
    }
}
```

### Наслідки вимкнення модуля (disable у config)

| Компонент | Поведінка |
|-----------|-----------|
| **Маршрути** | 404 Not Found |
| **CRUD** | Не зареєстровується в CrudApi |
| **Меню** | Пунктът видаляється зі sidebar |
| **Перекладання** | Ключі ('echeck::*') виводяться як підпис |
| **Джоби** | Не диспатчаться (guard у dispatch) |
| **Дані в БД** | Лишаються (без auto-delete) |
| **Маршрути ядра** | Не впливають |

---

## Одноразові зміни ядра (app/, routes/)

1. **app/Services/ModuleRegistry.php** — singleton з auto-discovery
2. **config/modules.php** — конфіг enable/disable + dependsOn
3. **app/Http/routes(Router)** — типізована сигнатура для реєстрації модульних маршрутів
4. **routes/api.php** — цикл по ModuleRegistry::modules() + registerRoutes()
5. **resources/js/app.js** (/bootstrap) — import.meta.glob('../../app/Modules/*/resources/js/**') + auto-регістрація Vue компонентів
6. **app/Http/Middleware/AuthorizeModule.php** — проверка дозволів перед доступом до CRUD-операцій
7. **app/Crud/CrudController.php** — $this->getModuleContext() для поточного модуля
8. **lang/uk/crud.php** — резервні ключі для лейблів (якщо модульна локаль не завантажена)
9. **app/Events/ModuleDisabledEvent.php** + listener — hook для cleanup при вимкненні
10. **app/Console/Commands/ModulesCommand.php** — `php artisan modules:list`, `modules:enable`, `modules:disable`

---

## Vue SPA інтеграція

### resources/js/bootstrap/modules.ts (нова)

```typescript
// Автоматична реєстрація Vue компонентів з модулів
const moduleComponents = import.meta.glob(
    '../../app/Modules/*/resources/js/**/*.vue',
    { eager: true }
);

const modules: Record<string, any> = {};

Object.entries(moduleComponents).forEach(([path, component]: [string, any]) => {
    const match = path.match(/\/Modules\/(\w+)\//);
    const moduleName = match?.[1];

    if (!moduleName) return;

    if (!modules[moduleName]) {
        modules[moduleName] = { enabled: true, components: {} };
    }

    const componentName = path.split('/').pop()?.replace('.vue', '');
    modules[moduleName].components[componentName] = component.default;
});

// Передавати у Vuex або window.moduleRegistry
window.__modules = modules;
```

### resources/js/app.js (оновлення)

```javascript
import { createApp } from 'vue';
import './bootstrap/modules';  // ← завантажити модулі

const app = createApp({...});

// Реєстрація глобальних компонентів
Object.entries(window.__modules || {}).forEach(([moduleName, config]: [string, any]) => {
    Object.entries(config.components || {}).forEach(([name, component]) => {
        app.component(`Module${moduleName}${name}`, component);
    });
});

app.mount('#app');
```

### Меню/sidebar — серверна генерація

```php
// routes/api.php
Route::get('/bootstrap', function (Request $request) {
    return response()->json([
        'modules' => ModuleRegistry::getInstance()->getModules(),
        'sidebar' => ModuleRegistry::getInstance()->getSidebarItems()
            ->filter(fn ($item) => $request->user()?->hasPermissionTo($item['policy']))
            ->values(),
        'config' => config('app'),
    ]);
});
```

---

## CORE-склад (базова система)

**Не розділяється на модулі** — це константа для всіх проектів.

- **Authentication:** Passport + Spatie Permission + Roles
- **Framework:** Laravel 10 CRUD-фреймворк (CrudController, Operations, Fields)
- **Entities:**
  - Route, Trip, TripStation, TripVehicleAssignment
  - Booking, Ticket, TicketSeat, Order
  - Bus, Driver, Carrier, Station
  - User, Role, Permission
  - Currency, Language, Setting
- **Services:**
  - BookingService (ядро, трансферні логіки)
  - TripsService, RoutesService
  - TicketService, OrderService
  - PaymentService (abstract, провайдери мають конкретизовувати)
  - NotificationService (абстрактна — конкретні: SMS, Email, Telegram)
- **Jobs:** WorkerObserver (для базових моделей)
- **Queue:** Redis + Horizon
- **File storage:** S3 + local
- **Internationalization:** DB-backed lang loader (lang/uk/, lang/en/)
- **Activity logging:** Activity model + observer
- **Reporting:** Excel/PDF export (Maatwebsite, Snappy)

---

## Модулі-кандидати (список)

### Tier-1 (базова реалізація, низькі залежності)

| Модуль | Залежить від | Статус |
|--------|-------------|--------|
| **shortlinks** | core | Fase-1 пілот (простий) |
| **surveys** | core, notifications | Fase-2 |
| **reports** | core, notifications | Fase-2 |
| **return-rules** | core | Fase-3 |

### Tier-2 (функціональні розширення)

| Модуль | Залежить від | Статус |
|--------|-------------|--------|
| **notifications-sms** | core | Fase-3 (TurboSMS, AlphaSms) |
| **notifications-telegram** | notifications-sms | Fase-3 |
| **echeck** | notifications-sms | Fase-4 (fiscal checks) |
| **finance-wallet** | core | Fase-3 |
| **driver-cabinet** | core | Fase-3 |

### Tier-3 (зовнішні інтеграції)

| Модуль | Залежить від | Статус | API |
|--------|-------------|--------|-----|
| **integration-bussystem** | core | Fase-5 | Bussystem API (ticket sync) |
| **integration-busfor** | core | Fase-5 | Busfor provider |
| **integration-global** | core | Fase-5 | Global ticket API |
| **integration-privatbank** | core | Fase-5 | PrivatBank (B2B settlement) |
| **integration-external** | core | Fase-5 | Custom OTA partners |
| **payments-portmone** | core | Fase-5 | Portmone gateway |
| **payments-liqpay** | core | Fase-5 | LiqPay gateway |
| **payments-privatbank** | core | Fase-5 | PrivatBank payments |
| **telephony-binotel** | core | Fase-5 | Binotel call center |

### Tier-4 (CMS / публічне фасада)

| Модуль | Залежить від | Статус |
|--------|-------------|--------|
| **cms-content** | core | Fase-6 (static pages) |
| **blog** | core, cms-content | Fase-6 |
| **public-storefront** | core, notifications-sms | Fase-6 |
| **client-cabinet** | core, notifications-sms, finance-wallet | Fase-6 |
| **insurance** | core | Fase-6 |

### Лишаються в CORE

- **transfers** — зчеплено з BookingService → розсипання ускладнює реалізацію

---

## Фази реалізації (0-6)

| Fase | Назва | Критерії готовності | Модулі |
|------|-------|-------------------|--------|
| **0** | Передумови | CORE видалити 800 рядків debug-closures у api.php; Queue::after → ModuleDisabledEvent | — |
| **1** | Каркас + пілот | ModuleRegistry + config/modules.php + shortlinks (пілот); php artisan modules:list | shortlinks |
| **2** | CRUD/меню/lang | CrudController::registerModuleFields(), sidebar реєстр, DB trans-loader з namespace-підтримкою, admin-сесія | surveys, reports |
| **3** | Notifications | notifications-sms (TurboSMS), notifications-telegram, Job::dispatch(guard); finance-wallet, driver-cabinet | notifications-*, finance-wallet, driver-cabinet |
| **4** | Echeck | EcheckService, fiscal check workflow, 17 тестів, heartbeat до API | echeck |
| **5** | Partner API's | 5 інтеграцій (Bussystem, Busfor, Global, PrivatBank, External), 3 payment-gateway'ю, Binotel | integration-*, payments-*, telephony-* |
| **6** | CMS / Storefronts | cms-content, blog, public-storefront, client-cabinet, insurance | cms-*, blog, public-*, client-*, insurance |

**Критерій: система продукційна** після кожної фази (без модуля — 404, не ломает CORE).

---

## 10 правил для модулів

1. **Не змінюй core-таблиці** — використовуй extension-таблиці 1:1 або пиши в config-JSON. Новий hook-field у ядрі, якщо потрібно.

2. **Декларуй залежності в module.php** — ModuleRegistry перевіряє dependsOn перед завантаженням. Ламання залежностей → exception.

3. **Локалізація з namespace** — trans('echeck::echeck.field') замість trans('fields.echeck_*'). Дозволяє вимкнення без конфлікту.

4. **Маршрути через registerRoutes(Router)** — не прямо в routes/api.php. Вимкнення модуля → 404.

5. **CRUD-контролери через ModuleRegistry** — registerCrudController(Model, ControllerClass). Видимість у адміні залежить від denyAccess() + модульного дозволу.

6. **Дозволи (Spatie) мають префікс** — 'echeck-read', 'echeck-create', не просто 'read'. Додаються вручну (не через міграцію).

7. **Спостерігачі моделей в boot()** — Model::observe(). Никогда не слушай события вне модуля (тільки якщо модуль в залежності).

8. **Джоби диспатчаються з гардом** — SendEcheckSmsJob::dispatch() → перевіка ModuleRegistry::isEnabled('echeck'). Job не виконується, якщо модуль вимкнено.

9. **Меню/sidebar через registerSidebarItem()** — об'єкт з icon, label, route, policy. Відповідь у /bootstrap API фільтрується за дозволами користувача.

10. **Тести — у модулі** — tests/Unit/, tests/Feature/, база даних як у CORE. Міграції у database/migrations/ завантажуються автоматично.

---

## Ризики та мітігація

| Ризик | Наслідок | Мітігація |
|-------|----------|-----------|
| DB-backed trans-loader глушить namespacedключи | Ключі вигідають як підпис замість перекладу | Запуск test:trans команди на Fase-2 |
| Зміна неймспейсів моделей (Entities → Modules/) | Job::unserialization збиває; activity_log.subject_type не знаходить модель | Залишити моделі на місці до Fase-4; використовувати class_alias для миграції |
| hasPermissionTo гейт мовчки не працює (typo у дозволу) | Користувач отримує 500 замість 403 | Логування: Log::warning() при регістрації дозволу; артизанська команда `check:permissions` |
| SPA-маршрут без permission-guard | Користувач жахлив доступ → 403 від API | Додати router.beforeEach() + перевірку дозволів на Fase-3 |
| Циклічні залежності (A dependsOn B, B dependsOn A) | Freezing при завантаженні | Граф-перевірка в validate_dependencies(); запис topology sort |

---

## Ліцензування (відкладено)

**Статус:** research-only, без реалізації

**Дизайн (майбутнє):**
- Ed25519 ECDSA токен підписаний license-серверм
- Гібрид: офлайн-скупення + періодичний heartbeat (1 раз на 24 год)
- Enforcement у ModuleRegistry::discover() → перевірка токена перед enable
- Контролює: список модулів, expiration, user seats
- Реальний захист: server-side relaying (echeck/SMS/partner API йде через proxy)

**Причина відкладення:** Спочатку модульна архітектура; ліцензування як оверлей.

---

## Посилання

- **Детальний план (код-як-план):** `/Users/serhiin/Data/Source/3g/Extraxct_Modules.md`
- **Session-нотатка:** [[2026-08-05-modularization-design]]
- **Project-overview:** [[project-overview]]

---

**Версія документу:** 0.1 (дизайн)
**Оновлено:** 2026-08-05
**Автор:** Claude Code / Serhii P.
