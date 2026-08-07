"""Этап 1: исследовательский анализ (EDA) витрины продаж.

Строит графики в reports/figures/ и печатает ключевые выводы.
Графики 01-03 показываются в дашборде и генерируются на двух языках
(русский — без суффикса, английский — с суффиксом _en).
"""

import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from config import DATA_PATH, DPI, FIG_DIR, FIG_DOW, FIG_MONTHLY, FIG_TOP_CATS

sys.stdout.reconfigure(encoding="utf-8")

CHART_LABELS = {
    "ru": {
        "monthly_title": "Продажи по месяцам",
        "monthly_revenue": "Выручка, тыс. R$",
        "monthly_items": "Продано позиций",
        "top_cats_title": "Топ-10 категорий по выручке",
        "top_cats_x": "Выручка, тыс. R$",
        "dow_title": "Продажи по дням недели",
        "dow_y": "Продано позиций",
        "dow_names": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
    },
    "en": {
        "monthly_title": "Monthly sales",
        "monthly_revenue": "Revenue, thousand R$",
        "monthly_items": "Items sold",
        "top_cats_title": "Top 10 categories by revenue",
        "top_cats_x": "Revenue, thousand R$",
        "dow_title": "Sales by day of week",
        "dow_y": "Items sold",
        "dow_names": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
}


def fig_name(base, lang):
    return f"{base}.png" if lang == "ru" else f"{base}_{lang}.png"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG_DIR / name, dpi=DPI)
    plt.close(fig)
    print(f"  график: reports/figures/{name}")


def _bilingual_charts(monthly, top_cats, dow):
    """Графики 1-3 на двух языках (используются в дашборде)."""
    for lang, L in CHART_LABELS.items():
        # 1. Продажи по месяцам (выручка и число позиций)
        fig, ax1 = plt.subplots(figsize=(11, 5))
        ax1.bar(monthly.index.astype(str), monthly["revenue"] / 1000, color="steelblue")
        ax1.set_ylabel(L["monthly_revenue"])
        ax1.tick_params(axis="x", rotation=60)
        ax2 = ax1.twinx()
        ax2.plot(monthly.index.astype(str), monthly["items"], color="darkorange", marker="o")
        ax2.set_ylabel(L["monthly_items"])
        ax1.set_title(L["monthly_title"])
        save(fig, fig_name(FIG_MONTHLY, lang))

        # 2. Топ-10 категорий по выручке
        fig, ax = plt.subplots(figsize=(9, 5))
        top_cats.iloc[::-1].plot.barh(ax=ax, color="seagreen")
        ax.set_xlabel(L["top_cats_x"])
        ax.set_title(L["top_cats_title"])
        save(fig, fig_name(FIG_TOP_CATS, lang))

        # 3. Сезонность по дням недели
        dow_named = dow.copy()
        dow_named.index = L["dow_names"]
        fig, ax = plt.subplots(figsize=(8, 4))
        dow_named.plot.bar(ax=ax, color="slateblue", rot=0)
        ax.set_ylabel(L["dow_y"])
        ax.set_title(L["dow_title"])
        save(fig, fig_name(FIG_DOW, lang))


def _extra_charts(sales):
    """Графики 4-5 (одна языковая версия): дневной ряд и динамика топ-5 категорий."""
    # 4. Дневной ряд продаж (основа будущего прогноза)
    daily = sales.groupby("date")["price"].count()
    fig, ax = plt.subplots(figsize=(11, 4))
    daily.plot(ax=ax, color="steelblue", linewidth=0.8, label="Факт")
    daily.rolling(7).mean().plot(ax=ax, color="crimson", linewidth=1.8, label="Среднее за 7 дней")
    ax.set_ylabel("Позиций в день")
    ax.set_title("Продажи по дням")
    ax.legend()
    save(fig, "04_daily_sales.png")

    # 5. Динамика топ-5 категорий по месяцам
    top5 = sales.groupby("category")["price"].sum().nlargest(5).index
    pivot = sales[sales["category"].isin(top5)].pivot_table(
        index="month", columns="category", values="price", aggfunc="count"
    )
    fig, ax = plt.subplots(figsize=(11, 5))
    pivot.plot(ax=ax, marker=".")
    ax.set_ylabel("Продано позиций")
    ax.set_title("Динамика топ-5 категорий")
    ax.tick_params(axis="x", rotation=60)
    save(fig, "05_top5_dynamics.png")


def _print_findings(monthly, top_cats, dow):
    """Ключевые цифры EDA в консоль."""
    print("\nКлючевые выводы:")
    dow_ru = dow.copy()
    dow_ru.index = CHART_LABELS["ru"]["dow_names"]
    full_months = monthly[(monthly.index >= "2017-01") & (monthly.index <= "2018-08")]
    growth = full_months["revenue"].iloc[-1] / full_months["revenue"].iloc[0]
    print(f"- Рост выручки янв-2017 → авг-2018: x{growth:.1f}")
    peak = f"{monthly['revenue'].idxmax()} (R$ {monthly['revenue'].max():,.0f})"
    print(f"- Пиковый месяц: {peak} — Black Friday в ноябре")
    print(f"- Топ-категория: {top_cats.index[0]} (R$ {top_cats.iloc[0]:,.0f} тыс.)")
    print(f"- Самый активный день: {dow_ru.idxmax()}, самый тихий: {dow_ru.idxmin()}")
    sparse = monthly[monthly["items"] < 100]
    sparse_months = list(sparse.index.astype(str))
    print(f"- Месяцев с <100 продаж (нерепрезентативные, убрать из обучения): {len(sparse)}: {sparse_months}")


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    sales = pd.read_csv(DATA_PATH, parse_dates=["date"])
    sales["month"] = sales["date"].dt.to_period("M")

    monthly = sales.groupby("month").agg(revenue=("price", "sum"), items=("order_id", "count"))
    top_cats = sales.groupby("category")["price"].sum().nlargest(10) / 1000
    dow = sales.groupby(sales["date"].dt.dayofweek)["price"].count()

    _bilingual_charts(monthly, top_cats, dow)
    _extra_charts(sales)
    _print_findings(monthly, top_cats, dow)


if __name__ == "__main__":
    main()
