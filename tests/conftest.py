"""Общие фикстуры для тестов пайплайна."""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sales_mart():
    """Синтетическая витрина продаж в окне TRAIN_START..SERIES_END.

    - ежедневные одиночные заказы для baseline/trends/prophet;
    - 12 мультитоварных заказов (pA+pB, категории furniture_decor+bed_bath_table),
      чтобы recommend дал непустые пары товаров и категорий.
    Синтетика, НЕ реальный Olist (CC BY-NC-SA 4.0).
    """
    cats = ["health_beauty", "watches_gifts", "sports_leisure", "toys", "auto"]
    rows = []
    for i, day in enumerate(pd.date_range("2018-01-01", "2018-08-22", freq="D")):
        rows.append(
            {
                "date": day,
                "order_id": f"s{i}",
                "product_id": f"prod{i % 7}",
                "category": cats[i % len(cats)],
                "price": 50.0 + i % 20,
            }
        )
    for j, day in enumerate(pd.date_range("2018-08-01", periods=12, freq="D")):
        oid = f"pair{j}"
        rows.append({"date": day, "order_id": oid, "product_id": "pA", "category": "furniture_decor", "price": 100.0})
        rows.append({"date": day, "order_id": oid, "product_id": "pB", "category": "bed_bath_table", "price": 120.0})
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df


@pytest.fixture
def pipeline_dir(tmp_path, sales_mart):
    """tmp с data/processed/sales.csv и reports/figures/; возвращает корень tmp."""
    data = tmp_path / "data" / "processed"
    data.mkdir(parents=True)
    (tmp_path / "reports" / "figures").mkdir(parents=True)
    sales_mart.to_csv(data / "sales.csv", index=False)
    return tmp_path


@pytest.fixture
def valid_reports(tmp_path):
    """tmp-каталог с валидными мини-отчётами (те колонки, что читает дашборд)."""
    pd.DataFrame({"date": ["2018-01-01"], "items": [5]}).to_csv(tmp_path / "daily_history.csv", index=False)
    pd.DataFrame({"ds": ["2018-08-23"], "yhat": [5.0], "yhat_lower": [4.0], "yhat_upper": [6.0]}).to_csv(
        tmp_path / "forecast_future.csv", index=False
    )
    pd.DataFrame({"category": ["toys"], "prev": [10], "last": [20], "growth_pct": [100.0]}).to_csv(
        tmp_path / "trends.csv", index=False
    )
    pd.DataFrame({"item_a": ["a"], "item_b": ["b"], "together": [5], "confidence": [0.5], "lift": [1.5]}).to_csv(
        tmp_path / "recs_categories.csv", index=False
    )
    return tmp_path
