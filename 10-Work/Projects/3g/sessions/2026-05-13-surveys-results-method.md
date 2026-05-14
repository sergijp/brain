---
title: "Проект: 3g — Survey results endpoint рефакторинг"
date: 2026-05-13
tags: [3g, work, session, surveys, api]
category: session
project: 3g
status: completed
aliases: []
pinecone_indexed: false
---

## Мета сесії

Оновити метод `results` у `SurveysCrudController` — повертати структуровані дані по кожному опитуванню: ім'я користувача, id квитка, дата опитування, середня оцінка, відповіді з текстом запитання.

## Виконано

| Задача | Результат |
|--------|-----------|
| Визначити структуру відповіді методу `results` | JSON зі списком `responses`, кожен з `ticket_id`, `user_name`, `surveyed_at`, `average_rating`, `answers[]` |
| Дослідити структуру моделей | `SurveyResponse` → `ticket` + `answers`; `SurveyResponseAnswer` → `question_id`, `type`, `answer` |
| Виявити проблему `question: null` | `questions` у Survey — масив рядків-типів, без тексту; `question_id` = `Survey.id` |
| Реалізувати отримання тексту запитання | `Survey::whereIn('id', $questionIds)->get()->keyBy('id')` → `$survey->title` |
| Рефакторинг методу `results` | Повертає `responses[]` замість плоского `answers[]` |

## Важливі рішення (ADR)

Див. [[2026-05-13-survey-question-from-survey-title]]

| Рішення | Обґрунтування |
|---------|---------------|
| `question_id` в `SurveyResponseAnswer` = `Survey.id` | Кожен Survey — окреме запитання з `title` як текстом |
| Текст запитання береться з `Survey.title` | `questions` JSON в Survey зберігає лише типи, не текст |
| `eager load` surveys через `whereIn` | Уникаємо N+1 при обробці відповідей |

## Проблеми й як вирішили

**`question: null` у відповідях:**
- Причина: код шукав текст у `Survey.questions` JSON через `keyBy('id')`, але `questions = ["rating"]` — просто масив типів без тексту
- Рішення: завантажити Survey-моделі за `question_id` і повернути `Survey.title` як текст запитання

## Артефакти

- `app/Http/Controllers/Api/Crud/SurveysCrudController.php` — оновлено метод `results()`

### Фінальна структура відповіді

```json
{
  "trip_id": 42,
  "responses_count": 2,
  "responses": [
    {
      "ticket_id": 101,
      "user_name": "Іваненко Петро",
      "surveyed_at": "2026-05-13 14:23:00",
      "average_rating": 4.5,
      "answers": [
        { "type": "rating", "question": "Оцініть комфорт поїздки", "answer": "5" },
        { "type": "text",   "question": "Ваші побажання",          "answer": "Все чудово!" }
      ]
    }
  ]
}
```

### Ключовий фрагмент коду

```php
$questionIds = $responses->pluck('answers')->flatten()->pluck('question_id')->unique();
$surveysMap = Survey::whereIn('id', $questionIds)->get()->keyBy('id');

// в map():
'question' => $surveysMap->get($a->question_id)?->title,
```

## Пов'язані нотатки

- [[2026-05-13-surveys-custom-routes]]
- [[2026-05-11-survey-module]]