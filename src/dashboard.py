"""Этап 6: Streamlit-дашборд — прогноз, тренды, рекомендации в одном окне.

Запуск:  .venv\\Scripts\\streamlit run src\\dashboard.py
Дашборд читает готовые артефакты из reports/ (модели на лету не обучает).
Перед запуском прогнать: prepare_data.py, forecast_prophet.py, trends.py, recommend.py.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

REPORTS_DIR = Path(__file__).parent.parent / "reports"
FIG_DIR = REPORTS_DIR / "figures"

# Перевод категорий Olist для читаемости (остальные показываются как есть)
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


def ru(category):
    return CATEGORY_RU.get(category, category)


st.set_page_config(page_title="Marketplace AI", page_icon="🛍️", layout="wide")
st.title("🛍️ Marketplace AI — умная аналитика продаж")
st.markdown(
    "Система смотрит на историю продаж маркетплейса и помогает продавцу принимать решения: "
    "**сколько товара будут покупать** (прогноз), **что сейчас набирает популярность** (тренды) "
    "и **что предлагать в дополнение к покупке** (рекомендации)."
)


@st.cache_data
def load_csv(name, **kwargs):
    return pd.read_csv(REPORTS_DIR / name, **kwargs)


missing = [f for f in ["forecast_future.csv", "daily_history.csv", "trends.csv", "recs_categories.csv"]
           if not (REPORTS_DIR / f).exists()]
if missing:
    st.error(f"Нет артефактов: {missing}. Запусти скрипты: prepare_data, forecast_prophet, trends, recommend.")
    st.stop()

tab_about, tab_forecast, tab_trends, tab_recs = st.tabs(
    ["ℹ️ О проекте", "📈 Прогноз", "🔥 Тренды", "🛒 Покупают вместе"]
)

# ---------- О проекте ----------
with tab_about:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Заказов в данных", "99 441")
    col2.metric("Товаров", "32 951")
    col3.metric("Категорий", "73")
    col4.metric("Период", "2016–2018")

    st.markdown("""
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
""")

    st.divider()
    st.markdown("### Как выглядят данные")
    c1, c2 = st.columns(2)
    with c1:
        st.image(str(FIG_DIR / "01_monthly_sales.png"),
                 caption="Маркетплейс быстро рос: выручка увеличилась в 7,5 раза за полтора года. "
                         "Пик в ноябре 2017 — Чёрная пятница.")
        st.image(str(FIG_DIR / "03_day_of_week.png"),
                 caption="Недельный ритм: больше всего заказов в понедельник, меньше всего в субботу. "
                         "Модель прогноза учитывает этот ритм.")
    with c2:
        st.image(str(FIG_DIR / "02_top_categories.png"),
                 caption="Крупнейшие категории по выручке: красота и здоровье, часы и подарки, "
                         "товары для спальни и ванной.")
        st.image(str(FIG_DIR / "07_prophet_forecast.png"),
                 caption="Проверка модели: красная линия — прогноз, синяя — что было на самом деле. "
                         "Модель поймала и тренд, и недельные колебания.")

# ---------- Прогноз ----------
with tab_forecast:
    history = load_csv("daily_history.csv", parse_dates=["date"], index_col="date")["items"]
    forecast = load_csv("forecast_future.csv", parse_dates=["ds"], index_col="ds")

    st.subheader("Сколько будут покупать в ближайшие 28 дней")
    st.info(
        "📌 **Как читать:** синяя линия — реальные продажи в прошлом (штук в день), "
        "красная — предсказание модели на месяц вперёд. Линия «пилит» вверх-вниз — это нормально: "
        "в начале недели покупают больше, в выходные меньше. Модель этот ритм знает и повторяет."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Прогноз: продаж в день (в среднем)", f"{forecast['yhat'].mean():.0f} шт.",
                f"{(forecast['yhat'].mean() / history.iloc[-28:].mean() - 1) * 100:+.0f}% к прошлому месяцу")
    col2.metric("Средняя ошибка модели", "20,9%", "лучше простого угадывания (24%)")
    col3.metric("На чём училась модель", f"{len(history)} дней продаж")

    days_back = st.slider("Сколько истории показать, дней", 30, len(history), 120)
    chart_df = pd.DataFrame({"Факт (было)": history.iloc[-days_back:], "Прогноз (будет)": forecast["yhat"]})
    st.line_chart(chart_df, height=380)
    with st.expander("Прогноз по дням — таблица"):
        st.caption("«мин» и «макс» — коридор неопределённости: реальное значение с высокой вероятностью попадёт в него.")
        st.dataframe(forecast.rename(columns={"yhat": "прогноз, шт.", "yhat_lower": "мин", "yhat_upper": "макс"}))

# ---------- Тренды ----------
with tab_trends:
    trends = load_csv("trends.csv")
    trends["Категория"] = trends["category"].map(ru)
    show = trends.rename(columns={"prev": "Прошлый месяц, шт.", "last": "Последний месяц, шт.",
                                  "growth_pct": "Рост, %"})

    st.subheader("Что взлетает, а что проседает")
    st.info(
        "📌 **Как читать:** сравниваем продажи каждой категории за последние 28 дней с предыдущими 28 днями. "
        "+100% — продажи удвоились. Весь рынок растёт, поэтому «отстающие» — это не всегда падение, "
        "а рост медленнее остальных. Практический смысл: зелёное — куда заходить продавцу, красное — где не стоит наращивать закупки."
    )

    col1, col2 = st.columns(2)
    cols = ["Категория", "Прошлый месяц, шт.", "Последний месяц, шт.", "Рост, %"]
    col1.markdown("**🚀 Лидеры роста**")
    col1.dataframe(show.head(10)[cols].set_index("Категория"), width="stretch")
    col2.markdown("**🐢 Отстающие**")
    col2.dataframe(show.tail(10).iloc[::-1][cols].set_index("Категория"), width="stretch")

    st.bar_chart(show.set_index("Категория")["Рост, %"], height=380,
                 x_label="категория", y_label="рост продаж, %")

# ---------- Рекомендации ----------
with tab_recs:
    recs = load_csv("recs_categories.csv")

    st.subheader("Что покупают вместе")
    st.info(
        "📌 **Как читать:** выбери категорию — система покажет, что покупатели чаще всего берут с ней "
        "в одном заказе. Это тот самый блок «С этим товаром часто покупают» на маркетплейсах. "
        "**Уверенность** — вероятность совместной покупки: 74% значит «3 из 4 покупателей возьмут и это». "
        "**Сила связи (lift)** больше 1 — связь не случайна."
    )

    category = st.selectbox("Покупатель положил в корзину:", sorted(recs["item_a"].unique()), format_func=ru)
    top = (recs[recs["item_a"] == category]
           .sort_values(["together", "confidence"], ascending=False).head(5)
           .assign(**{
               "Рекомендуем предложить": lambda df: df["item_b"].map(ru),
               "Куплены вместе, раз": lambda df: df["together"].astype(int),
               "Уверенность": lambda df: (df["confidence"] * 100).round(1).astype(str) + " %",
               "Сила связи (lift)": lambda df: df["lift"].round(2),
           }))
    if top.empty:
        st.warning("Для этой категории слишком мало совместных покупок — рекомендаций нет.")
    else:
        st.dataframe(top[["Рекомендуем предложить", "Куплены вместе, раз", "Уверенность", "Сила связи (lift)"]]
                     .reset_index(drop=True), width="stretch")
        best = top.iloc[0]
        st.success(f"💡 Вывод: к категории «{ru(category)}» стоит предлагать «{best['Рекомендуем предложить']}» — "
                   f"вместе их купили {best['Куплены вместе, раз']} раз ({best['Уверенность']} покупателей берут обе).")
