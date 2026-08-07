"""Этап 6: Streamlit-дашборд — прогноз, тренды, рекомендации в одном окне.

Запуск:  .venv\\Scripts\\streamlit run src\\dashboard.py
Дашборд читает готовые артефакты из reports/ (модели на лету не обучает).
Перед запуском прогнать: prepare_data.py, forecast_prophet.py, trends.py, recommend.py.
Все тексты интерфейса — в i18n.py (переключатель RU/EN вверху страницы).
"""

import pandas as pd
import streamlit as st

from config import DASHBOARD_REQUIRED, DEFAULT_TOP_N, FIG_DIR, LANGS, LIFT_FLOOR, REPORTS_DIR
from i18n import category_name, t
from recommend import top_recommendations

# Контракт producer -> dashboard: какие колонки дашборд читает из каждого отчёта.
# Ключи совпадают с config.DASHBOARD_REQUIRED (проверяется тестом-контрактом).
REQUIRED_COLUMNS = {
    "daily_history.csv": {"date", "items"},
    "forecast_future.csv": {"ds", "yhat", "yhat_lower", "yhat_upper"},
    "trends.csv": {"category", "prev", "last", "growth_pct"},
    "recs_categories.csv": {"item_a", "item_b", "together", "confidence", "lift"},
}


def fig_path(base, lang):
    return str(FIG_DIR / (f"{base}.png" if lang == "ru" else f"{base}_{lang}.png"))


def load_reports(reports_dir=REPORTS_DIR):
    """Читает обязательные отчёты и проверяет их колонки.

    Бросает FileNotFoundError (нет файла) или ValueError (нет колонки), чтобы
    рассинхрон формата отчётов ловился на старте, а не KeyError в середине рендера.
    """
    frames = {}
    for name, required in REQUIRED_COLUMNS.items():
        path = reports_dir / name
        if not path.exists():
            raise FileNotFoundError(f"Нет отчёта: {name} (в {reports_dir}). Запусти пайплайн — см. README.")
        df = pd.read_csv(path)
        absent = required - set(df.columns)
        if absent:
            raise ValueError(f"В отчёте {name} нет колонок: {sorted(absent)}")
        frames[name] = df
    return frames


@st.cache_data
def load_csv(name, **kwargs):
    return pd.read_csv(REPORTS_DIR / name, **kwargs)


def main():
    st.set_page_config(page_title="Marketplace AI", page_icon="🛍️", layout="wide")

    title_col, lang_col = st.columns([5, 1])
    lang = lang_col.radio(
        "Language",
        list(LANGS),
        horizontal=True,
        label_visibility="collapsed",
        format_func=lambda code: {"ru": "🇷🇺 Рус", "en": "🇬🇧 Eng"}[code],
    )
    title_col.title(t("app_title", lang))
    st.markdown(t("app_intro", lang))

    missing = [f for f in DASHBOARD_REQUIRED if not (REPORTS_DIR / f).exists()]
    if missing:
        st.error(t("error_missing", lang, files=missing))
        st.stop()
    try:
        load_reports()  # дополнительно проверяем колонки отчётов
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    tab_about, tab_forecast, tab_trends, tab_recs = st.tabs(
        [t("tab_about", lang), t("tab_forecast", lang), t("tab_trends", lang), t("tab_recs", lang)]
    )

    # ---------- О проекте ----------
    with tab_about:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(t("about_orders", lang), "99 441")
        col2.metric(t("about_products", lang), "32 951")
        col3.metric(t("about_categories", lang), "73")
        col4.metric(t("about_period", lang), "2016–2018")

        st.markdown(t("about_md", lang))

        st.divider()
        st.markdown(t("about_charts_header", lang))
        c1, c2 = st.columns(2)
        with c1:
            st.image(fig_path("01_monthly_sales", lang), caption=t("caption_monthly", lang))
            st.image(fig_path("03_day_of_week", lang), caption=t("caption_dow", lang))
        with c2:
            st.image(fig_path("02_top_categories", lang), caption=t("caption_top_cats", lang))
            st.image(fig_path("07_prophet_forecast", lang), caption=t("caption_prophet", lang))

    # ---------- Прогноз ----------
    with tab_forecast:
        history = load_csv("daily_history.csv", parse_dates=["date"], index_col="date")["items"]
        forecast = load_csv("forecast_future.csv", parse_dates=["ds"], index_col="ds")

        st.subheader(t("forecast_header", lang))
        st.info(t("forecast_info", lang))

        col1, col2, col3 = st.columns(3)
        delta_pct = (forecast["yhat"].mean() / history.iloc[-28:].mean() - 1) * 100
        col1.metric(
            t("metric_forecast_label", lang),
            t("metric_forecast_value", lang, n=f"{forecast['yhat'].mean():.0f}"),
            t("metric_forecast_delta", lang, pct=f"{delta_pct:+.0f}"),
        )
        col2.metric(t("metric_error_label", lang), t("metric_error_value", lang), t("metric_error_delta", lang))
        col3.metric(t("metric_history_label", lang), t("metric_history_value", lang, n=len(history)))

        days_back = st.slider(t("slider_label", lang), 30, len(history), 120)
        chart_df = pd.DataFrame(
            {t("legend_fact", lang): history.iloc[-days_back:], t("legend_forecast", lang): forecast["yhat"]}
        )
        st.line_chart(chart_df, height=380)
        with st.expander(t("expander_table", lang)):
            st.caption(t("expander_caption", lang))
            st.dataframe(
                forecast.rename(
                    columns={
                        "yhat": t("col_forecast", lang),
                        "yhat_lower": t("col_min", lang),
                        "yhat_upper": t("col_max", lang),
                    }
                )
            )

    # ---------- Тренды ----------
    with tab_trends:
        trends = load_csv("trends.csv")
        trends[t("col_category", lang)] = trends["category"].map(lambda c: category_name(c, lang))
        show = trends.rename(
            columns={"prev": t("col_prev", lang), "last": t("col_last", lang), "growth_pct": t("col_growth", lang)}
        )

        st.subheader(t("trends_header", lang))
        st.info(t("trends_info", lang))

        col1, col2 = st.columns(2)
        cols = [t("col_category", lang), t("col_prev", lang), t("col_last", lang), t("col_growth", lang)]
        col1.markdown(t("trends_rising", lang))
        col1.dataframe(show.head(10)[cols].set_index(t("col_category", lang)), width="stretch")
        col2.markdown(t("trends_lagging", lang))
        col2.dataframe(show.tail(10).iloc[::-1][cols].set_index(t("col_category", lang)), width="stretch")

        st.bar_chart(
            show.set_index(t("col_category", lang))[t("col_growth", lang)],
            height=380,
            x_label=t("trends_chart_x", lang),
            y_label=t("trends_chart_y", lang),
        )

    # ---------- Рекомендации ----------
    with tab_recs:
        recs = load_csv("recs_categories.csv")

        st.subheader(t("recs_header", lang))
        st.info(t("recs_info", lang))

        category = st.selectbox(
            t("recs_select", lang), sorted(recs["item_a"].unique()), format_func=lambda c: category_name(c, lang)
        )
        top = top_recommendations(recs, category, top_n=DEFAULT_TOP_N, min_lift=LIFT_FLOOR).assign(
            **{
                t("col_recommend", lang): lambda df: df["item_b"].map(lambda c: category_name(c, lang)),
                t("col_together", lang): lambda df: df["together"].astype(int),
                t("col_confidence", lang): lambda df: (df["confidence"] * 100).round(1).astype(str) + " %",
                t("col_lift", lang): lambda df: df["lift"].round(2),
            }
        )
        if top.empty:
            st.warning(t("recs_empty", lang))
        else:
            out_cols = [
                t("col_recommend", lang),
                t("col_together", lang),
                t("col_confidence", lang),
                t("col_lift", lang),
            ]
            st.dataframe(top[out_cols].reset_index(drop=True), width="stretch")
            best = top.iloc[0]
            st.success(
                t(
                    "recs_conclusion",
                    lang,
                    cat=category_name(category, lang),
                    rec=best[t("col_recommend", lang)],
                    n=best[t("col_together", lang)],
                    conf=best[t("col_confidence", lang)],
                )
            )
            st.caption(t("recs_lift_caption", lang))


if __name__ == "__main__":
    main()
