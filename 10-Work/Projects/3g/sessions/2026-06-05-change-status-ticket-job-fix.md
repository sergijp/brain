---
title: "Проект: 3g — Фікс ChangeStatusTicketJob (Infobus DomCrawler)"
date: 2026-06-05
tags: [3g, work, session, infobus, jobs, bugfix]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Виправити помилку `InvalidArgumentException: The current node list is empty` у `App\Jobs\Trips\ChangeStatusTicketJob` при спробі розпарсити HTML-відповідь від Infobus.

## Виконано

| Задача | Результат |
|--------|-----------|
| Діагностика помилки DomCrawler | Встановлено: `.text()` кидає exception на порожньому NodeList |
| Додано debug-роут в `api.php` | Перевірено логін + відповідь від `dispatcher.bussystem.eu` |
| Виявлено root cause | Деякі `ticket_api` не існують в Infobus → сервер повертає 404-сторінку з HTTP 200 |
| Фікс `ChangeStatusTicketJob` | Перевірка `->count() > 0` перед `->text()`, `Log::warning` + `return` при відсутності тікета |
| Верифікація | Debug-роут підтвердив: валідний тікет повертає `status: "Оплачений"` |
| Видалення debug-роуту | `api.php` очищено |

## Важливі рішення

| Рішення | Обґрунтування |
|---------|---------------|
| `return` замість `throw` при 404 від Infobus | Тікет може бути куплений через інший канал і не існувати в Infobus — це не помилка, а нормальний кейс |
| `Log::warning` з `ticket_id` і `ticket_api` | Дозволяє відстежити які тікети не синхронізуються без падіння черги |

## Проблеми й як вирішили

**Проблема:** `->text()` кидає `InvalidArgumentException` коли CSS-селектор не знайдений.  
**Рішення:** Додати `->count() > 0` перед кожним `->text()`.

**Проблема:** Debug-роут — `Call to a member function getName() on array`.  
**Причина:** `$cookieJar->toArray()` повертає масиви, не об'єкти.  
**Рішення:** `array_column($cookieJar->toArray(), 'Name')`.

**Проблема:** Infobus повертає HTTP 200 але з HTML сторінкою "Ошибка 404" (soft 404).  
**Наслідок:** DomCrawler не знаходив `.ticket-id-wrapper` і падав.

## Артефакти

- `app/Jobs/Trips/ChangeStatusTicketJob.php` — фікс рядки 66-77
- `routes/api.php` — debug-роут додано і видалено в межах сесії

## Пов'язані нотатки

- [[project_infobus_sync]] — попередні баги з Infobus синхронізацією
