---
title: "Проект: 3g — Додано поле is_qr_sale на квитки (QR-продаж через Portmone)"
date: 2026-05-27
tags: [3g, work, session, feature, tickets, portmone, qrcode]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

# Поле `is_qr_sale` для квитків + проброс у Trip Management Resource

## Мета сесії

Додати boolean позначку на тікети, що ідентифікує квиток як проданий через QR-код (через WidgetsController flow). У Trip Management UI показувати `is_qrcode = 1` лише якщо квиток `is_qr_sale = true` І в статусі `sold`.

## Виконано

| Задача | Результат |
|--------|-----------|
| Міграція `add_is_qr_sale_to_tickets_table` | `database/migrations/2026_05_27_120000_*.php` — `boolean` default `false`, `after('full_refund')` |
| Оновити `Ticket` model | `$fillable` + `$casts` ('bool') |
| Виставляти `true` у `WidgetsController::getPortmoneUrl` | Спочатку для тікетів ордера, потім розширено на `parentTicket` + `childTicket` |
| Логіка `is_qrcode` у `TripManagementTicket` Resource | `is_qr_sale && status == STATUS_SOLD` |

## Важливі рішення (ADR)

| Рішення | Альтернатива | Чому обрано |
|---------|--------------|-------------|
| Назва колонки `is_qr_sale` | `sold_via_qrcode`, `via_qrcode` | Вибір користувача — короткий boolean-стиль |
| Не показувати в CRUD-адмінці | Додати column в TicketsCrudController | Поле службове, не для перегляду оператором |
| Виставлення в `WidgetsController::getPortmoneUrl` | У `BookingService` чи через event | Користувач явно вказав точку — це єдиний QR-флоу |
| `withoutGlobalScope(TicketScope::class)` на update | Без зняття скоупу | Профілактично — щойно фіксили баг де TicketScope ламав update related tickets ([[2026-05-27-portmone-parent-child-ticket-status-fix]]) |
| Variant A для parent/child: eager-load + batch UPDATE по id | Variant B: orWhereIn(parent_id, ...) | Простіше, не залежить від назви FK-колонки, явний guard `if ($ticket->parentTicket)` |
| Status check `==` а не `===` у Resource | Strict comparison | Match-стиль legacy-коду навколо (Ticket.php:593, сусідні рядки Resource) |
| Константа `Ticket::$STATUS_SOLD` | `$STATUS_PAYED` | `STATUS_PAYED` у моделі взагалі немає; `STATUS_SOLD` = `'sold'` — єдиний "проданий" статус |

## Проблеми й як вирішили

### Issue 1: Захист від TicketScope при update
**Контекст:** щойно перед цим фіксили баг де lazy-load parent/child повертав null через скоуп. Профілактично — всі звертання до `tickets()` / `parentTicket` / `childTicket` у новій логіці робилися з `withoutGlobalScope(TicketScope::class)`.

### Issue 2: Розширення на трансферні квитки
**Симптом:** перший варіант оновлював тільки прямі квитки ордера. Користувач уточнив що для трансферних треба також `parent` і `child`.
**Рішення:** eager-load relationships з `withoutGlobalScope` + збір унікальних id + один масовий UPDATE. Guard `if ($ticket->parentTicket)` / `if ($ticket->childTicket)` — для не-трансферних квитків нічого зайвого.
**SQL вартість:** 3 SELECT + 1 UPDATE незалежно від кількості тікетів (без N+1).

### IDE diagnostics (false positive)
`Method 'withoutGlobalScope' not found in Ticket` — Eloquent magic method, IDE не розпізнає. Не баг.

## Артефакти

### Файли змінено
- `database/migrations/2026_05_27_120000_add_is_qr_sale_to_tickets_table.php` (НОВИЙ)
- `app/Entities/Tenant/Ticket.php` — `$fillable` + `$casts`
- `app/Http/Controllers/Api/WidgetsController.php` — `getPortmoneUrl` рядки ~1168-1190
- `app/Http/Resources/System/Trip/Management/TripManagementTicket.php` — рядок 55 (тепер ~57 після Pint)

### Команди для запуску на сервері
```bash
php artisan migrate
```

### Pattern: `is_qr_sale` для ордера + трансферних

```php
$tickets = $order->tickets()
    ->withoutGlobalScope(TicketScope::class)
    ->with([
        'parentTicket' => fn ($q) => $q->withoutGlobalScope(TicketScope::class),
        'childTicket'  => fn ($q) => $q->withoutGlobalScope(TicketScope::class),
    ])
    ->get();

$ids = collect();
foreach ($tickets as $ticket) {
    $ids->push($ticket->id);
    if ($ticket->parentTicket) $ids->push($ticket->parentTicket->id);
    if ($ticket->childTicket)  $ids->push($ticket->childTicket->id);
}

Ticket::withoutGlobalScope(TicketScope::class)
    ->whereIn('id', $ids->unique())
    ->update(['is_qr_sale' => true]);
```

### Pattern: Resource conditional flag

```php
'is_qrcode' => $ticket->is_qr_sale && $ticket->status == Ticket::$STATUS_SOLD,
```

## Залишкові задачі

- Запустити `php artisan migrate` на сервері.
- **Можлива бізнес-розширення:** `OrderController` має окремий Portmone-checkout (стандартний веб) — якщо бізнес вважає що **будь-яка** Portmone-оплата = QR-sale, треба додати update і там. Зараз фіксується тільки QR-флоу через WidgetsController.
- Frontend (Trip Management UI) має використовувати нове поле `is_qrcode` з Resource.
- IDE warning `withoutGlobalScope not found in Ticket` — false positive, ігнорувати або додати PHPDoc/@mixin на Ticket щоб IDE розпізнавав статичні Eloquent методи.

## Пов'язані нотатки

- [[2026-05-27-portmone-parent-child-ticket-status-fix]] — попередній фікс цього ж дня, виявив проблему з TicketScope + lazy-load
- [[project_ticket_scope_relationships]] (auto-memory) — патерн обходу TicketScope для related tickets
- Trip Management context: операторський UI керування рейсами