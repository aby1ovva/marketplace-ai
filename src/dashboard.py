"""Этап 6: Streamlit-дашборд — прогноз, тренды, рекомендации в одном окне.

Запуск:  .venv\\Scripts\\streamlit run src\\dashboard.py
Дашборд читает готовые артефакты из reports/ (модели на лету не обучает).
Перед запуском прогнать: prepare_data.py, forecast_prophet.py, trends.py, recommend.py.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

REPORTS_DIR = Path(__file__).parent.parent / "reports"

st.set_page_config(page_title="Marketplace AI", layout="wide")
st.title("Marketplace AI — аналитика продаж")


@st.cache_data
def load_csv(name, **kwargs):
    return pd.read_csv(REPORTS_DIR / name, **kwargs)


missing = [f for f in ["forecast_future.csv", "daily_history.csv", "trends.csv", "recs_categories.csv"]
           if not (REPORTS_DIR / f).exists()]
if missing:
    st.error(f"Нет артефактов: {missing}. Запусти скрипты: prepare_data, forecast_prophet, trends, recommend.")
    st.stop()

tab_forecast, tab_trends, tab_recs = st.tabs(["📈 Прогноз", "🔥 Тренды", "🛒 Покупают вместе"])

with tab_forecast:
    history = load_csv("daily_history.csv", parse_dates=["date"], index_col="date")["items"]
    forecast = load_csv("forecast_future.csv", parse_dates=["ds"], index_col="ds")

    st.subheader("Прогноз продаж на 28 дней (Prophet)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Прогноз, позиций/день (среднее)", f"{forecast['yhat'].mean():.0f}",
                f"{(forecast['yhat'].mean() / history.iloc[-28:].mean() - 1) * 100:+.0f}% к последним 28 дням")
    col2.metric("Точность модели (MAPE)", "20.9%", "лучше baseline на 3.1 п.п.")
    col3.metric("История данных", f"{len(history)} дней")

    days_back = st.slider("Показать историю, дней", 30, len(history), 120)
    chart_df = pd.DataFrame({"Факт": history.iloc[-days_back:], "Прогноз": forecast["yhat"]})
    st.line_chart(chart_df, height=380)
    with st.expander("Таблица прогноза"):
        st.dataframe(forecast.rename(columns={"yhat": "прогноз", "yhat_lower": "мин", "yhat_upper": "макс"}))

with tab_trends:
    trends = load_csv("trends.csv")
    st.subheader("Рост категорий: последние 28 дней vs предыдущие 28")

    col1, col2 = st.columns(2)
    col1.markdown("**🚀 Лидеры роста**")
    col1.dataframe(trends.head(10).set_index("category"), width="stretch")
    col2.markdown("**📉 Отстающие**")
    col2.dataframe(trends.tail(10).iloc[::-1].set_index("category"), width="stretch")

    st.bar_chart(trends.set_index("category")["growth_pct"], height=380,
                 x_label="категория", y_label="рост, %")

with tab_recs:
    recs = load_csv("recs_categories.csv")
    st.subheader("Что покупают вместе (по категориям)")

    category = st.selectbox("Категория", sorted(recs["item_a"].unique()))
    top = (recs[recs["item_a"] == category]
           .sort_values(["together", "confidence"], ascending=False).head(5)
           .assign(confidence=lambda df: (df["confidence"] * 100).round(1),
                   lift=lambda df: df["lift"].round(2))
           .rename(columns={"item_b": "рекомендуем", "together": "вместе, раз",
                            "confidence": "confidence, %", "lift": "lift"}))
    if top.empty:
        st.info("Для этой категории недостаточно совместных покупок.")
    else:
        st.dataframe(top[["рекомендуем", "вместе, раз", "confidence, %", "lift"]].reset_index(drop=True),
                     width="stretch")
        st.caption("lift > 1 — связь сильнее случайной (среди заказов с 2+ товарами)")
