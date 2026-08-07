"""Тесты логики сборки витрины продаж (этап 1)."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from prepare_data import build_sales_mart


def make_raw_frames():
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_status": ["delivered", "canceled", "delivered"],
            "order_purchase_timestamp": pd.to_datetime(["2018-01-05 10:00", "2018-01-06 11:00", "2018-02-10 12:00"]),
        }
    )
    items = pd.DataFrame(
        {
            "order_id": ["o1", "o1", "o2", "o3"],
            "product_id": ["p1", "p2", "p1", "p1"],
            "price": [100.0, 50.0, 100.0, 110.0],
        }
    )
    products = pd.DataFrame(
        {
            "product_id": ["p1", "p2"],
            "product_category_name": ["informatica_acessorios", None],
        }
    )
    translation = pd.DataFrame(
        {
            "product_category_name": ["informatica_acessorios"],
            "product_category_name_english": ["computers_accessories"],
        }
    )
    return orders, items, products, translation


def test_only_delivered_orders_kept():
    mart = build_sales_mart(*make_raw_frames())
    assert "o2" not in mart["order_id"].values
    assert len(mart) == 3  # 2 позиции из o1 + 1 из o3


def test_category_translated_to_english():
    mart = build_sales_mart(*make_raw_frames())
    p1 = mart[mart["product_id"] == "p1"]
    assert (p1["category"] == "computers_accessories").all()


def test_missing_category_becomes_unknown():
    mart = build_sales_mart(*make_raw_frames())
    p2 = mart[mart["product_id"] == "p2"]
    assert (p2["category"] == "unknown").all()


def test_date_column_is_normalized_day():
    mart = build_sales_mart(*make_raw_frames())
    assert set(mart["date"].dt.strftime("%Y-%m-%d")) == {"2018-01-05", "2018-02-10"}


def test_expected_columns():
    mart = build_sales_mart(*make_raw_frames())
    assert list(mart.columns) == ["date", "order_id", "product_id", "category", "price"]
