---
title: "Проект: 3g — Route Access Control для користувачів"
date: 2026-05-14
tags: [3g, work, session, route-access, scope, laravel]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Реалізувати обмеження доступу до рейсів для певних користувачів — тільки рейси вибраних маршрутів. Адміни бачать все. Backward compatibility: якщо маршрути не призначені — повний доступ.

---

## Виконано

| Задача | Результат |
|--------|-----------|
| Планування + архітектурний review (ddd-architect, dba, devil) | Plan у `plan-route-access.md` |
| Migration `member_route` pivot | Composite PK, cascade, index route_id |
| Migration `route_access_restricted` на `members` | Boolean flag, default false |
| `Member::allowedRoutes()` + `isRouteRestricted()` | BelongsToMany to Route |
| `RouteAccessService` | `hasFullAccess`, `getAllowedRouteIds` (мемоізація), `canAccessRoute` |
| `RouteAccessScope` (global scope на Trip) | Фільтрує скрізь автоматично |
| `Trip::booted()` → global scope | Замінили local scope |
| `TripPolicy::view()` | Захист одиничних endpoints |
| `GetUserRouteField` PreProcessor | Активні маршрути + вибрані user |
| `StoreUserRouteField` PreProcessor | sync pivot |
| `UsersCrudController` — таб "Маршрути" | checkbox + user_route field |
| `ReportsController::routes()` | Фільтрує маршрути по доступу |
| Singleton + мемоізація `RouteAccessService` | Один SQL запит per request |
| `CreateTicketJob` → `withoutGlobalScope` | Infobus sync не ламається |
| Postman колекція Busfor API | `busfor-api.postman_collection.json` |

---

## Важливі рішення (ADR)

Детальні ADR: [[decisions/2026-05-14-route-access-global-scope]]

| Рішення | Вибір | Причина |
|---------|-------|---------|
| Global vs Local scope | **Global scope** | Local потребував ручного `->accessibleBy()` скрізь — легко пропустити |
| Opt-in семантика | **`route_access_restricted` flag** | Порожній pivot двозначний; flag = явна семантика |
| `canAccessRoute()` в BookingService | **Прибрали** | Global scope покриває автоматично |
| `withoutGlobalScope` в Jobs | Тільки `CreateTicketJob` | Єдиний job що встановлює user через `request()->setUserResolver()` |
| Мемоізація | `private array $cache` в singleton | Один DB запит на request |

---

## Проблеми й як вирішили

| Проблема | Рішення |
|----------|---------|
| `addClause()` не існує в кастомному CRUD | Замінили на `modifyQuery()` |
| "Select All" не зберігалось | `StoreUserRouteField` при `all_routs=true` очищав pivot — виправили на `sync($data['routs'])` |
| `request()->user()` в global scope ламає Jobs | null-check на початку scope — Jobs безпечні |
| Busfor API `tripInfo` не фільтрував по маршруту | Global scope покриває автоматично |
| `.env.testing` відсутній | Тести не написані — потрібно спочатку налаштувати |

---

## Артефакти

- `plan-route-access.md` — повний план у корені проекту
- `busfor-api.postman_collection.json` — Postman колекція
- `database/migrations/2026_05_14_000001_create_member_route_table.php`
- `database/migrations/2026_05_14_000002_add_route_access_restricted_to_members.php`
- `app/Scopes/RouteAccessScope.php`
- `app/Services/RouteAccessService.php`
- `app/Policies/TripPolicy.php`
- `app/Crud/PreProcessors/Get/GetUserRouteField.php`
- `app/Crud/PreProcessors/Store/StoreUserRouteField.php`

## Залишилось

- Налаштувати `.env.testing` → написати feature tests (6 сценаріїв)
- `php artisan migrate` на проді
- Злити worktrees в основну гілку

---

## Пов'язані нотатки

- [[docs/architecture]]
- [[decisions/2026-05-14-route-access-global-scope]]