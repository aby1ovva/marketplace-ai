"""Локализация дашборда: строки интерфейса (RU/EN) и названия категорий.

t(key, lang, **kwargs) — строка интерфейса с подстановками.
category_name(cat, lang) — человекочитаемое имя категории Olist.
"""

CATEGORY_RU = {
    "health_beauty": "Красота и здоровье",
    "watches_gifts": "Часы и подарки",
    "bed_bath_table": "Спальня и ванная",
    "sports_leisure": "Спорт и отдых",
    "computers_accessories": "Компьютерные аксессуары",
    "furniture_decor": "Мебель и декор",
    "housewares": "Товары для дома",
    "telephony": "Мобильные телефоны и аксессуары",
    "auto": "Автотовары",
    "toys": "Игрушки",
    "cool_stuff": "Необычные товары",
    "garden_tools": "Сад и инструменты",
    "perfumery": "Парфюмерия",
    "baby": "Детские товары",
    "electronics": "Электроника",
    "stationery": "Канцтовары",
    "fashion_bags_accessories": "Сумки и аксессуары",
    "pet_shop": "Зоотовары",
    "office_furniture": "Офисная мебель",
    "consoles_games": "Консоли и игры",
    "luggage_accessories": "Чемоданы и багаж",
    "construction_tools_construction": "Строительные инструменты",
    "construction_tools_lights": "Освещение для ремонта",
    "musical_instruments": "Музыкальные инструменты",
    "food": "Продукты питания",
    "home_confort": "Домашний уют (пледы, подушки)",
    "home_construction": "Стройка и ремонт",
    "small_appliances": "Мелкая бытовая техника",
    "furniture_living_room": "Мебель для гостиной",
    "air_conditioning": "Климатическая техника",
    "home_appliances": "Бытовая техника",
    "fixed_telephony": "Стационарные телефоны",
    "drinks": "Напитки",
    "audio": "Аудиотехника",
    "books_general_interest": "Книги",
    "fashion_shoes": "Обувь",
    "unknown": "Без категории",
}


def category_name(category, lang):
    if lang == "ru":
        return CATEGORY_RU.get(category, category)
    return category.replace("_", " ").title()


def t(key, lang, **kwargs):
    text = STRINGS[lang][key]
    return text.format(**kwargs) if kwargs else text


STRINGS = {
    "ru": {
        "app_title": "🛍️ Marketplace AI — умная аналитика продаж",
        "app_intro": (
            "Система смотрит на историю продаж маркетплейса и помогает продавцу принимать решения: "
            "**сколько товара будут покупать** (прогноз), **что сейчас набирает популярность** (тренды) "
            "и **что предлагать в дополнение к покупке** (рекомендации)."
        ),
        "error_missing": "Нет артефактов: {files}. Запусти скрипты: prepare_data, forecast_prophet, trends, recommend.",
        "tab_about": "ℹ️ О проекте",
        "tab_forecast": "📈 Прогноз",
        "tab_trends": "🔥 Тренды",
        "tab_recs": "🛒 Покупают вместе",
        "about_orders": "Заказов в данных",
        "about_products": "Товаров",
        "about_categories": "Категорий",
        "about_period": "Период",
        "about_md": """
### Что это?

Перед тобой аналитическая система для продавца на маркетплейсе. Она построена на **реальных данных
бразильского маркетплейса [Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)** —
это ~100 тысяч настоящих заказов за два года: кто, когда и что покупал.

### Какие вопросы решает?

| Вкладка | Вопрос продавца | Как решаем |
|---------|-----------------|------------|
| 📈 **Прогноз** | «Сколько будут покупать в следующий месяц? Сколько товара закупить?» | Модель Prophet выучила тренд и сезонность продаж и предсказывает на 28 дней вперёд |
| 🔥 **Тренды** | «Какие категории сейчас взлетают? Куда заходить?» | Сравниваем продажи за последний месяц с предыдущим |
| 🛒 **Покупают вместе** | «Что предложить покупателю в довесок?» | Ищем пары товаров, которые подозрительно часто встречаются в одном заказе |

### Откуда мы знаем, что прогнозу можно верить?

Мы спрятали от модели последний месяц данных, попросили её «предсказать» его, а потом сравнили
с тем, что было на самом деле. Модель ошибалась в среднем на **20,9%** — а примитивный способ
«завтра будет как в среднем за последний месяц» ошибается на 24%. Улучшение доказано на честной проверке.
""",
        "about_charts_header": "### Как выглядят данные",
        "caption_monthly": (
            "Маркетплейс быстро рос: выручка увеличилась в 7,5 раза за полтора года. "
            "Пик в ноябре 2017 — Чёрная пятница."
        ),
        "caption_dow": (
            "Недельный ритм: больше всего заказов в понедельник, меньше всего в субботу. "
            "Модель прогноза учитывает этот ритм."
        ),
        "caption_top_cats": (
            "Крупнейшие категории по выручке: красота и здоровье, часы и подарки, товары для спальни и ванной."
        ),
        "caption_prophet": (
            "Проверка модели: красная линия — прогноз, синяя — что было на самом деле. "
            "Модель поймала и тренд, и недельные колебания."
        ),
        "forecast_header": "Сколько будут покупать в ближайшие 28 дней",
        "forecast_info": (
            "📌 **Как читать:** синяя линия — реальные продажи в прошлом (штук в день), "
            "красная — предсказание модели на месяц вперёд. Линия «пилит» вверх-вниз — это нормально: "
            "в начале недели покупают больше, в выходные меньше. Модель этот ритм знает и повторяет."
        ),
        "metric_forecast_label": "Прогноз: продаж в день (в среднем)",
        "metric_forecast_value": "{n} шт.",
        "metric_forecast_delta": "{pct}% к прошлому месяцу",
        "metric_error_label": "Средняя ошибка модели",
        "metric_error_value": "20,9%",
        "metric_error_delta": "лучше простого угадывания (24%)",
        "metric_history_label": "На чём училась модель",
        "metric_history_value": "{n} дней продаж",
        "slider_label": "Сколько истории показать, дней",
        "legend_fact": "Факт (было)",
        "legend_forecast": "Прогноз (будет)",
        "expander_table": "Прогноз по дням — таблица",
        "expander_caption": "«мин» и «макс» — коридор неопределённости: реальное значение с высокой вероятностью попадёт в него.",
        "col_forecast": "прогноз, шт.",
        "col_min": "мин",
        "col_max": "макс",
        "trends_header": "Что взлетает, а что проседает",
        "trends_info": (
            "📌 **Как читать:** сравниваем продажи каждой категории за последние 28 дней с предыдущими 28 днями. "
            "+100% — продажи удвоились. Весь рынок растёт, поэтому «отстающие» — это не всегда падение, "
            "а рост медленнее остальных. Практический смысл: зелёное — куда заходить продавцу, "
            "красное — где не стоит наращивать закупки."
        ),
        "col_category": "Категория",
        "col_prev": "Прошлый месяц, шт.",
        "col_last": "Последний месяц, шт.",
        "col_growth": "Рост, %",
        "trends_rising": "**🚀 Лидеры роста**",
        "trends_lagging": "**🐢 Отстающие**",
        "trends_chart_x": "категория",
        "trends_chart_y": "рост продаж, %",
        "recs_header": "Что покупают вместе",
        "recs_info": (
            "📌 **Как читать:** выбери категорию — система покажет, что покупатели чаще всего берут с ней "
            "в одном заказе. Это тот самый блок «С этим товаром часто покупают» на маркетплейсах. "
            "**Уверенность** — вероятность совместной покупки: 74% значит «3 из 4 покупателей возьмут и это». "
            "**Сила связи (lift)** больше 1 — связь не случайна."
        ),
        "recs_select": "Покупатель положил в корзину:",
        "col_recommend": "Рекомендуем предложить",
        "col_together": "Куплены вместе, раз",
        "col_confidence": "Уверенность",
        "col_lift": "Сила связи (lift)",
        "recs_empty": "Для этой категории слишком мало совместных покупок — рекомендаций нет.",
        "recs_conclusion": (
            "💡 Вывод: к категории «{cat}» стоит предлагать «{rec}» — "
            "вместе их купили {n} раз ({conf} покупателей берут обе)."
        ),
        "recs_lift_caption": "lift > 1 — связь сильнее случайной (среди заказов с 2+ товарами)",
    },
    "en": {
        "app_title": "🛍️ Marketplace AI — smart sales analytics",
        "app_intro": (
            "The system analyzes marketplace sales history and helps sellers make decisions: "
            "**how much will be sold** (forecast), **what is gaining popularity** (trends) "
            "and **what to offer alongside a purchase** (recommendations)."
        ),
        "error_missing": "Missing artifacts: {files}. Run the scripts: prepare_data, forecast_prophet, trends, recommend.",
        "tab_about": "ℹ️ About",
        "tab_forecast": "📈 Forecast",
        "tab_trends": "🔥 Trends",
        "tab_recs": "🛒 Bought together",
        "about_orders": "Orders in dataset",
        "about_products": "Products",
        "about_categories": "Categories",
        "about_period": "Period",
        "about_md": """
### What is this?

An analytics system for a marketplace seller, built on **real data from the Brazilian
marketplace [Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)** —
about 100,000 genuine orders over two years: who bought what, and when.

### What questions does it answer?

| Tab | Seller's question | How we solve it |
|-----|-------------------|-----------------|
| 📈 **Forecast** | "How much will sell next month? How much stock should I buy?" | A Prophet model learned the trend and seasonality and predicts 28 days ahead |
| 🔥 **Trends** | "Which categories are taking off? Where should I enter?" | We compare last month's sales with the previous month |
| 🛒 **Bought together** | "What should I offer as an add-on?" | We find product pairs that appear in the same order suspiciously often |

### Why can the forecast be trusted?

We hid the last month of data from the model, asked it to "predict" it, and compared
with what actually happened. The model was off by **20.9%** on average — while the naive approach
"tomorrow equals last month's average" is off by 24%. The improvement is proven by honest validation.
""",
        "about_charts_header": "### What the data looks like",
        "caption_monthly": (
            "The marketplace grew fast: revenue increased 7.5x in a year and a half. "
            "The November 2017 peak is Black Friday."
        ),
        "caption_dow": (
            "Weekly rhythm: most orders on Monday, fewest on Saturday. The forecast model accounts for this rhythm."
        ),
        "caption_top_cats": ("Top categories by revenue: health & beauty, watches & gifts, bed, bath & table goods."),
        "caption_prophet": (
            "Model validation: the red line is the forecast, the blue one is what actually happened. "
            "The model captured both the trend and the weekly swings."
        ),
        "forecast_header": "How much will be sold in the next 28 days",
        "forecast_info": (
            "📌 **How to read:** the blue line is actual past sales (items per day), "
            "the red one is the model's prediction for the next month. The zigzag is normal: "
            "people buy more early in the week and less on weekends. The model knows this rhythm and repeats it."
        ),
        "metric_forecast_label": "Forecast: sales per day (average)",
        "metric_forecast_value": "{n} items",
        "metric_forecast_delta": "{pct}% vs last month",
        "metric_error_label": "Average model error",
        "metric_error_value": "20.9%",
        "metric_error_delta": "better than naive guessing (24%)",
        "metric_history_label": "Training data",
        "metric_history_value": "{n} days of sales",
        "slider_label": "History to show, days",
        "legend_fact": "Actual (past)",
        "legend_forecast": "Forecast (future)",
        "expander_table": "Day-by-day forecast — table",
        "expander_caption": '"min" and "max" form the uncertainty band: the real value will most likely fall inside it.',
        "col_forecast": "forecast, items",
        "col_min": "min",
        "col_max": "max",
        "trends_header": "What is taking off and what is slowing down",
        "trends_info": (
            "📌 **How to read:** we compare each category's sales over the last 28 days with the previous 28 days. "
            '+100% means sales doubled. The whole market is growing, so "lagging" doesn\'t always mean decline — '
            "just slower growth. Practical meaning: green — where a seller should enter, "
            "red — where not to increase stock."
        ),
        "col_category": "Category",
        "col_prev": "Previous month, items",
        "col_last": "Last month, items",
        "col_growth": "Growth, %",
        "trends_rising": "**🚀 Growth leaders**",
        "trends_lagging": "**🐢 Lagging**",
        "trends_chart_x": "category",
        "trends_chart_y": "sales growth, %",
        "recs_header": "What is bought together",
        "recs_info": (
            "📌 **How to read:** pick a category — the system shows what buyers most often add to the same order. "
            'This is the "Frequently bought together" block you see on marketplaces. '
            '**Confidence** is the probability of a joint purchase: 74% means "3 out of 4 buyers take this too". '
            "**Lift** above 1 means the link is not random."
        ),
        "recs_select": "The buyer put in the cart:",
        "col_recommend": "Recommend offering",
        "col_together": "Bought together, times",
        "col_confidence": "Confidence",
        "col_lift": "Lift",
        "recs_empty": "Too few joint purchases for this category — no recommendations.",
        "recs_conclusion": (
            '💡 Takeaway: alongside "{cat}" it pays to offer "{rec}" — '
            "they were bought together {n} times ({conf} of buyers take both)."
        ),
        "recs_lift_caption": "lift > 1 — the link is stronger than chance (among orders with 2+ items)",
    },
}
