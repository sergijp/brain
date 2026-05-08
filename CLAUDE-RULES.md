# 📚 Vault Frontmatter Standard

Уся документація у vault має дотримуватись єдиного frontmatter, щоб запити по категорії/тегу/статусу через Obsidian Search/Dataview працювали стабільно.

## Закрита taxonomy

### `category` (обов'язково, рівно одне значення)

| Значення | Призначення | Розташування |
|----------|-------------|--------------|
| `project` | Project overview | `10-Work/Projects/<p>/project-overview.md` |
| `docs` | Архітектурні документи | `10-Work/Projects/<p>/docs/<topic>.md` |
| `session` | Сесійні нотатки | `10-Work/Projects/<p>/sessions/YYYY-MM-DD-*.md` |
| `adr` | Architectural Decision Records | `10-Work/Projects/<p>/decisions/YYYY-MM-DD-*.md` |
| `trading-analysis` | TDA-аналіз ринку | `20-Trading/Analysis/YYYY-MM-DD/...` |
| `trading-journal` | Журнал угод | `20-Trading/Journal/...` |
| `trading-retro` | Ретро-сесії | `20-Trading/Retro/...` |
| `agent` | Інструкції/SKILL.md | `60-Agents/...`, `20-Trading/skills/...` |
| `reference` | Довідники, MCP-tools | `60-Agents/shared/...`, `50-Resources/...` |
| `inbox` | Тимчасові, ще не класифіковані | `00-Inbox/...` |

### `status` (обов'язково)

`active` | `done` | `archived` | `partial` | `research` | `planned` | `superseded`

### `tags` (масив, обов'язково ≥2)

Перший тег — **завжди** project slug (`buktrek`, `3g`, `air-trans`, `bustrek`) або domain (`trading`).
Решта — вільні: `architecture`, `multi-tenancy`, `notifications`, `sms`, `bus`, `tda`, `smc` тощо.

### Інші обов'язкові поля

- `title` — людський заголовок
- `date` — дата створення `YYYY-MM-DD`
- `project` — slug проекту (для work) або відсутнє (для trading/agent)
- `aliases` — масив, мінімум один alias виду `<project>-<topic>` для wiki-link стійкості при перейменуваннях
- `pinecone_indexed: false` — marker для майбутньої векторної індексації (див. `vault_writer.py`)

### Опційні

- `last_verified: YYYY-MM-DD` — для `category: docs` і `category: reference`. Дата останньої звірки змісту з реальним кодом/станом.
- `superseded_by: "[[...]]"` — для застарілих ADR.

## Шаблони

Шаблони з готовим frontmatter — у `~/MyVault/templates/`:
- `Project-Session.md`
- `Project-Architecture-Doc.md`
- `Project-Decision-ADR.md`
- `TDA-Template.md` (трейдинг)
- `Top-Down-Analysis-Template.md` (трейдинг)

При створенні нового файлу — спочатку копіюй шаблон, потім заповнюй.

## Поле `pinecone_indexed` — статус

> **⚠ Стан 2026-05-08:** поле `pinecone_indexed: false` присутнє у всіх шаблонах і `vault_writer.py`, але **векторна індексація НЕ реалізована**. Це задумане майбутнє: коли буде налаштовано Pinecone-pipeline, скрипт-індексатор буде вибирати файли з `pinecone_indexed: false`, відправляти у векторну БД і ставити `true`.
>
> Поки поле — marker зарезервованого формату, не функціональне. Залишається в шаблонах для forward-compatibility.

---

# 🔧 Git Commit Convention для Vault

Vault — це git-репо. Без message-конвенції `git log` стає read-only архівом. Усі коміти у vault мають формат:

```
<type>: YYYY-MM-DD <project|domain> <короткий-опис>
```

## Типи

| Тип | Коли | Приклад |
|-----|------|---------|
| `session` | сесійна нотатка | `session: 2026-05-08 buktrek SMS templates refactor` |
| `docs` | арх-документ або INDEX | `docs: 2026-05-08 buktrek + 3g docs/ skeleton` |
| `adr` | новий ADR | `adr: 2026-05-08 air-trans DTD identity refactor` |
| `analysis` | трейдинг-аналіз | `analysis: 2026-05-08 EURUSD H1 long setup` |
| `journal` | трейдинг-журнал | `journal: 2026-05-08 trading session GBPUSD/XAGUSD` |
| `retro` | трейдинг-ретро | `retro: 2026-04-23 weekly retro 3 rules` |
| `chore` | гігієна/інфра/CLAUDE-RULES | `chore: 2026-05-08 add Frontmatter Standard` |
| `fix` | виправлення в існуючих доках | `fix: 2026-05-08 buktrek mapping в feedback` |

## Правила

1. **Завжди вказуй дату YYYY-MM-DD** — навіть якщо це сьогодні.
2. **Project/domain** — `buktrek`, `3g`, `air-trans`, `bustrek` для work; `trading`, `dixie`, `kassandra` для трейдингу; `vault` для глобальних змін.
3. **Один коміт = одна логічна одиниця** (одна сесія, один doc, один ADR).
4. Опис до 60 символів. Деталі — у тілі коміту, якщо потрібні.
5. **Без `no message`** — це smell.

---

# 🏆 Golden Standard for Top-Down Analysis (TDA)

Цей документ визначає обов'язковий регламент проведення аналізу ринку.

## 1. Підготовка графіка
- Перед початком аналізу НОВОГО символу виконати повне очищення: `draw_clear`.
- Працювати в одній активній вкладці, послідовно змінюючи активи.

## 2. Послідовність та Візуалізація
Для кожного активу зробити 6 скріншотів у такому порядку:
1. **Weekly (W)** — Глобальна структура.
2. **Daily (D)** — Денний тренд та рівні.
3. **4-Hour (4H)** — Проміжний Order Flow.
4. **1-Hour (1H)** — Локальна структура.
5. **15-Minute (15m)** — Пошук POI (Point of Interest).
6. **5-Minute (5m)** — Торговий сетап з інструментом позиції (Long/Short).

**Правило візуалу перед скріншотом:**
- Натиснути `Alt+R` (скидання масштабу).
- Виконати `ui_scroll(direction: "right", amount: 600)` (центрування ціни).

## 3. Документування в Obsidian
- **Шлях:** `~/MyVault/20-Trading/Analysis/YYYY-MM-DD/[SYMBOL]-analysis.md`.
- **Зображення:** Зберігати в підпапку `img/` всередині папки дня.
- **Формат:**
    - Тільки українська мова.
    - Кожен таймфрейм — окремий розділ `##`.
    - Wiki-links для фото: `![[img/назва.png]]`.
    - Обов'язковий YAML frontmatter (title, tags, category, status).

## 4. Торговий План (Обов'язкові пункти)
У кінці кожного аналізу має бути блок:
- **Bias:** Напрямок (Bullish/Bearish/Neutral).
- **POI:** Точка входу.
- **Target:** Ціль (ліквідність).
- **Stop Loss:** Рівень ризику.

---
*Останнє оновлення: 24.04.2026*

# 🎯 Execution Standard: Position Setup

Цей регламент визначає правила встановлення торгових позицій після завершення TDA.

## 1. Співвідношення Ризик/Прибуток (RR)
- **Мінімальний стандарт:** RR 1:3. 
- Будь-яка угода з меншим RR має бути обґрунтована окремо (наприклад, скальпінг або сильний фундаментальний фактор).

## 2. Логіка ліквідності та Вхід
- **Entry (Вхід):** Має базуватися на знятті ліквідності (**Liquidity Sweep**) або ретесті зони інтересу (Breaker Block, Order Block, FVG).
- **BSL (Buy Side Liquidity):** Чекаємо зняття максимумів перед входом у Short.
- **SSL (Sell Side Liquidity):** Чекаємо зняття мінімумів перед входом у Long.

## 3. Таргетування та ADR
- **TP (Take Profit):** Встановлюється на наступний пул ліквідності, але обов'язково в межах **ADR (Average Daily Range)**.
- Ціна повинна мати реальну можливість дійти до тейку протягом поточної торгової сесії.

## 4. Захист позиції (Stop Loss)
- **SL (Stop Loss):** Встановлюється за точку анулювання сетапу (**Invalidation Level**). 
- Якщо ціна досягає стопу, торгова ідея вважається помилковою. Стоп має бути максимально вузьким, але технічно обґрунтованим.

## 5. Інструментарій
- Використовувати тільки стандартні інструменти TradingView: `Long Position` та `Short Position`.
- Точно налаштовувати рівні (`stopLevel`, `profitLevel`) у параметрах інструменту.

---
*Останнє оновлення: 24.04.2026*
