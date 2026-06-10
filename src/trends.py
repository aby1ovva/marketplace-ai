"""Этап 4: аналитика трендов — какие категории растут, какие падают.

Сравнивает продажи за последние 28 дней с предыдущими 28 днями.
Результаты: reports/trends.csv + график топов роста/падения.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from forecast_baseline import DATA_PATH, SERIES_END

REPORTS_DIR = Path(__file__).parent.parent / "reports"

sys.stdout.reconfigure(encoding="utf-8")


def compute_category_growth(sales, end, period_days=28, min_sales=30):
    """Рост продаж по категориям: последние `period_days` дней vs предыдущие.

    min_sales — минимум продаж в предыдущем периоде, чтобы отсечь шум малых объёмов.
    """
    end = pd.Timestamp(end)
    last_start = end - pd.Timedelta(days=period_days - 1)
    prev_start = last_start - pd.Timedelta(days=period_days)

    last = sales[(sales["date"] >= last_start) & (sales["date"] <= end)]
    prev = sales[(sales["date"] >= prev_start) & (sales["date"] < last_start)]

    growth = (
        pd.DataFrame({"prev": prev.groupby("category").size(), "last": last.groupby("category").size()})
        .fillna(0)
        .query("prev >= @min_sales")
        .assign(growth_pct=lambda df: ((df["last"] - df["prev"]) / df["prev"] * 100).round(1))
        .sort_values("growth_pct", ascending=False)
        .reset_index()
        .rename(columns={"index": "category"})
    )
    return growth


def main():
    sales = pd.read_csv(DATA_PATH, parse_dates=["date"])
    growth = compute_category_growth(sales, end=SERIES_END)

    growth.to_csv(REPORTS_DIR / "trends.csv", index=False)

    rising, falling = growth.head(10), growth.tail(10)
    print(f"Период: последние 28 дней до {SERIES_END} vs предыдущие 28 дней")
    print(f"Категорий в анализе: {len(growth)} (с продажами >= 30 за период)\n")
    print("Топ-10 растущих категорий:")
    for _, r in rising.iterrows():
        print(f"  {r['category']:<30} {int(r['prev']):>4} -> {int(r['last']):>4}  ({r['growth_pct']:+.0f}%)")
    print("\nТоп-10 отстающих категорий:")
    for _, r in falling.iterrows():
        print(f"  {r['category']:<30} {int(r['prev']):>4} -> {int(r['last']):>4}  ({r['growth_pct']:+.0f}%)")

    both = pd.concat([rising, falling])
    colors = ["seagreen" if g > 0 else "indianred" for g in both["growth_pct"]]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(both["category"][::-1], both["growth_pct"][::-1], color=colors[::-1])
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Рост продаж, % (28 дней к предыдущим 28)")
    ax.set_title("Лидеры и отстающие по росту продаж")
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "figures" / "08_trends.png", dpi=120)
    print("\nГрафик: reports/figures/08_trends.png")
    print("Таблица: reports/trends.csv")


if __name__ == "__main__":
    main()
