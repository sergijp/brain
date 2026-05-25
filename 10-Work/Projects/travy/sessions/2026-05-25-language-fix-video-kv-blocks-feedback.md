---
title: "Проект: travy — Фікс мовного перемикача, нові поля (video, kv_blocks, info_blocks), feedback-форма"
date: 2026-05-25
tags: [travy, work, session, crud, laravel, vue]
category: session
project: travy
status: completed
aliases: []
pinecone_indexed: false
---

# Проект: travy — Фікс мовного перемикача, нові поля (video, kv_blocks, info_blocks), feedback-форма

## Мета сесії

- Виправити баг із додаванням `/public/uk` у URL при переключенні мови на сервері.
- Додати у CRUD-фреймворк нові типи полів: завантаження відео, конструктор key-value блоків, конструктор інформаційних блоків (title + список).
- Зробити поле `slug` у events необов'язковим.
- Додати accessor для отримання `kv_blocks` / `info_blocks` на поточній мові.
- Створити endpoint для обробки зворотного зв'язку з фронту з валідацією та відправкою на email із `config('settings.email_contact_form')`.

## Виконано

### 1. Фікс мовного перемикача (`/public/uk` у URL)

- `resources/js/front-end/components/header/language/LangDropdown.vue` — у методі `changeLanguage` додано прибирання сегмента `public` з `pathSegments` перед маніпуляціями.
- Видано рекомендований root `.htaccess` із 301 redirect для всіх запитів, що містять `/public/` (фактичне виправлення на рівні сервера).

### 2. Поле "Відео" у `WidgetsPageCrudController`

- Міграція `2026_05_25_120000_add_video_to_widgets_page_table.php` — колонка `video` (string, nullable).
- Модель `WidgetPage` — `video` у `$fillable`, cleanup у `deleting`, accessor `video_link`, у `logOnly`.
- Контролер `app/Http/Controllers/Api/System/VideosController.php` — endpoint для аплоаду/видалення відео (`multipart/form-data`, mimetypes mp4/webm/ogg/quicktime, max 200 MB).
- Маршрути `POST /api/system/videoSave`, `POST /api/system/videoDelete`.
- Vue-компонент `resources/js/crud/base/fields/VideoField.vue` — прев'ю через `<video>`, multipart-аплоад (НЕ base64), кнопка delete.
- Зареєстровано тип `'video'` у `resources/js/crud/config/fields.js`.
- Поле додано у `setupUpdateOperation` контролера на вкладці "Картинки".

### 3. Поле `kv_blocks` (конструктор блоків ключ-значення) — Widgets і Rooms

- Міграції додають json-колонку `kv_blocks` у `widgets_page` і `rooms`.
- Моделі `WidgetPage` і `Room` — `kv_blocks` у `$fillable` і `'kv_blocks' => 'array'` у `$casts`. Preprocessors не потрібні — Laravel сам серіалізує.
- Vue-компонент `KvBlocksField.vue` — collapsible-блоки, перемикач мов через `current_language` зі store, додавання/видалення блоків і items.
- Зареєстровано `'kv_blocks'` у `fields.js`.
- Поля додано у `WidgetsPageCrudController` (вкладка "Властивості") і `RoomsCrudController` (теж "Властивості").

### 4. Поле `info_blocks` (title + перекладений список) — Rooms

- Міграція `2026_05_25_120400_add_info_blocks_to_rooms_table.php`.
- Модель `Room` — `info_blocks` у `$fillable` і `$casts` як `'array'`.
- Vue-компонент `InfoBlocksField.vue` — без key, item = translatable string.
- Зареєстровано `'info_blocks'` у `fields.js`.
- Поле у `RoomsCrudController` на вкладці "Додаткова інформація".

### 5. Slug в Events — необов'язковий

- `app/Http/Requests/CRUD/Content/EventRequest.php` — `'required'` → `'nullable'` для `slug`.
- Міграція `2026_05_25_120300_make_slug_nullable_on_events_table.php` — `slug nullable` (unique-індекс залишається, MySQL дозволяє кілька NULL).

### 6. Трейт `LocalizesBlocks` — accessors на поточній мові

- `app/Helpers/LocalizesBlocks.php` — два accessor-атрибути:
  - `$model->kv_blocks_localized` — `[{ title: string, items: [{key, value}] }]`
  - `$model->info_blocks_localized` — `[{ title: string, items: string[] }]` (порожні відсіюються)
- Трейт підключено у `Room` і `WidgetPage`.

### 7. Feedback endpoint

- `POST /feedback` (route name: `feedback.send`).
- `app/Http/Requests/FeedbackRequest.php` — валідація: `name`/`message` required, `email` або `phone` обов'язкове (через `required_without`).
- `app/Notifications/FeedbackNotification.php` — `implements ShouldQueue`, конструктор з named args, додає `replyTo` якщо email присутній.
- `app/Http/Controllers/Frontend/FeedbackController.php` — перевірка, що `config('settings.email_contact_form')` не порожнє, відправка через `Notification::route('mail', ...)`, логування помилок.
- Маршрут у `routes/web.php`.

## Важливі рішення (ADR)

| Рішення | Альтернатива | Чому |
| ------- | ------------ | ---- |
| Відео через `multipart/form-data`, не base64 | Base64 (як `image`) | Відео великі — base64 роздуває payload +33%, впирається в `post_max_size`/PHP memory |
| `video` зберігається ОДРАЗУ під час аплоаду в окремому endpoint, не разом із submit форми | Зберегти шлях у фронт-state і відправити в загальному save | Сумісність з паттерном `files`/`images`, які теж аплоадять окремо |
| `kv_blocks` / `info_blocks` — JSON-колонка | Окремі таблиці + `texts` як для FAQ | Дуже сильно простіше, нема нових моделей/preprocessors, дані атомарні |
| Преаксесори у трейті `LocalizesBlocks` | Дублювати код в обох моделях | DRY — однакова логіка для двох моделей |
| Окремий `FeedbackController` + `FeedbackNotification` | Розширити існуючий `HomeController@sendMessageContactUs` | Існуючий код погано обробляє помилки (`$e->getCode()` як HTTP status), не валідує "email або phone"; чистіше зробити поряд |
| `nullable` у валідації slug + nullable-колонка | Авто-генерація slug при порожньому | Бекенд не повинен здогадуватись — це задача адміна, або згодом окремий beforeCreate-hook |

## Проблеми й як вирішили

- **`/public/uk` у URL**: причина — root `.htaccess` робив rewrite `^(.*)$ /public/$1` без `[L]`, Apache інколи перетворює його на зовнішній redirect, URL у браузері містить `/public/`. Рішення — додати правило 301 на прибирання `/public/` із browser-URL + `[L]` на всіх правилах + workaround у Vue.
- **`StoreImageHelper` приймає лише `data:image`** — для відео не підходить, бо великі. Зробили окремий контролер `VideosController` з multipart-аплоадом.
- **Default `setValue` у `FieldMixin`** для translatable-полів повертає об'єкт `{lang: ''}` — це не підходить для вкладеної структури. Тому у `KvBlocksField` / `InfoBlocksField` перевизначено `setValue` із нормалізацією під структуру блоків.
- **Unique slug у `events` + nullable**: MySQL дозволяє кілька NULL у unique-стовпці, тож конфлікту нема.

## Артефакти

### Створені файли

- `database/migrations/2026_05_25_120000_add_video_to_widgets_page_table.php`
- `database/migrations/2026_05_25_120100_add_kv_blocks_to_widgets_page_table.php`
- `database/migrations/2026_05_25_120200_add_kv_blocks_to_rooms_table.php`
- `database/migrations/2026_05_25_120300_make_slug_nullable_on_events_table.php`
- `database/migrations/2026_05_25_120400_add_info_blocks_to_rooms_table.php`
- `app/Http/Controllers/Api/System/VideosController.php`
- `app/Http/Controllers/Frontend/FeedbackController.php`
- `app/Http/Requests/FeedbackRequest.php`
- `app/Notifications/FeedbackNotification.php`
- `app/Helpers/LocalizesBlocks.php`
- `resources/js/crud/base/fields/VideoField.vue`
- `resources/js/crud/base/fields/KvBlocksField.vue`
- `resources/js/crud/base/fields/InfoBlocksField.vue`

### Змінені файли

- `resources/js/front-end/components/header/language/LangDropdown.vue` — workaround `/public/` segment
- `resources/js/crud/config/fields.js` — зареєстровано `'video'`, `'kv_blocks'`, `'info_blocks'`
- `app/Entities/System/Content/WidgetPage.php` — fillable + casts + cleanup + accessor + трейт `LocalizesBlocks`
- `app/Entities/System/Content/Room.php` — fillable + casts + трейт `LocalizesBlocks`
- `app/Http/Controllers/Api/Crud/Content/WidgetsPageCrudController.php` — поля video, kv_blocks
- `app/Http/Controllers/Api/Crud/Content/RoomsCrudController.php` — поля kv_blocks, info_blocks
- `app/Http/Requests/CRUD/Content/EventRequest.php` — slug required → nullable
- `routes/api.php` — `/system/videoSave`, `/system/videoDelete`
- `routes/web.php` — `POST /feedback`

### Команди розгортання

```bash
php artisan migrate
npm run build
```

Перевірити на проді:
- `php.ini`: `upload_max_filesize`, `post_max_size`, `max_execution_time` — узгодити з лімітом відео (200 MB)
- Налаштувати ключ `email_contact_form` у Settings CRUD адмінки
- Запустити `php artisan horizon` (якщо ще не запущено) — `FeedbackNotification implements ShouldQueue`

### Зразок використання у Blade

```blade
{{-- kv_blocks --}}
@foreach ($model->kv_blocks_localized as $block)
    <h3>{{ $block['title'] }}</h3>
    <dl>
        @foreach ($block['items'] as $item)
            <dt>{{ $item['key'] }}</dt>
            <dd>{{ $item['value'] }}</dd>
        @endforeach
    </dl>
@endforeach

{{-- info_blocks --}}
@foreach ($room->info_blocks_localized as $block)
    <h3>{{ $block['title'] }}</h3>
    <ul>
        @foreach ($block['items'] as $item)
            <li>{{ $item }}</li>
        @endforeach
    </ul>
@endforeach
```

### Структура JSON у БД

**kv_blocks:**
```json
[
  {
    "title": {"uk": "Контакти", "en": "Contacts"},
    "items": [
      {"key": "phone", "value": {"uk": "+380...", "en": "+380..."}}
    ]
  }
]
```

**info_blocks:**
```json
[
  {
    "title": {"uk": "Перевірте при виїзді", "en": "Check before leaving"},
    "items": [
      {"uk": "ліжко", "en": "bed"}
    ]
  }
]
```

## Пов'язані нотатки

- [[travy-crud-architecture]] (TODO — задокументувати CRUD-фреймворк, типи полів, реєстрацію через `fields.js`)
- [[travy-localization-pattern]] (TODO — як працюють translatable-поля через `texts` vs JSON-cast)
