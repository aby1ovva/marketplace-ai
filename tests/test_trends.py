"""Тесты аналитики трендов (этап 4)."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from trends import compute_category_growth


def make_sales():
    """Категория up: 10 -> 20 продаж, down: 20 -> 10, tiny: 1 -> 2 (мало данных)."""
    rows = []
    prev_day, last_day = "2018-07-01", "2018-08-01"  # попадают в разные 28-дневные окна
    rows += [{"date": prev_day, "category": "up"}] * 10 + [{"date": last_day, "category": "up"}] * 20
    rows += [{"date": prev_day, "category": "down"}] * 20 + [{"date": last_day, "category": "down"}] * 10
    rows += [{"date": prev_day, "category": "tiny"}] * 1 + [{"date": last_day, "category": "tiny"}] * 2
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df


def test_growth_computed_correctly():
    growth = compute_category_growth(make_sales(), end="2018-08-22", period_days=28, min_sales=5)
    up = growth.loc[growth["category"] == "up"].iloc[0]
    assert up["prev"] == 10 and up["last"] == 20
    assert up["growth_pct"] == 100.0


def test_decline_is_negative():
    growth = compute_category_growth(make_sales(), end="2018-08-22", period_days=28, min_sales=5)
    down = growth.loc[growth["category"] == "down"].iloc[0]
    assert down["growth_pct"] == -50.0


def test_low_volume_categories_filtered():
    growth = compute_category_growth(make_sales(), end="2018-08-22", period_days=28, min_sales=5)
    assert "tiny" not in growth["category"].values


def test_sorted_by_growth_desc():
    growth = compute_category_growth(make_sales(), end="2018-08-22", period_days=28, min_sales=5)
    assert growth["growth_pct"].is_monotonic_decreasing
