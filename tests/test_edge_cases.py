"""Граничные случаи и failure-режимы чистых функций пайплайна."""

import math

import pandas as pd

import forecast_baseline as fb
import prepare_data
import recommend
import trends


def test_build_pair_stats_empty_returns_columns():
    stats = recommend.build_pair_stats(pd.DataFrame({"order_id": [], "item": []}))
    assert list(stats.columns) == ["item_a", "item_b", "together", "confidence", "lift"]
    assert stats.empty


def test_top_recommendations_unknown_item_empty():
    stats = recommend.build_pair_stats(pd.DataFrame({"order_id": ["o1", "o1"], "item": ["A", "B"]}))
    assert recommend.top_recommendations(stats, "ZZZ").empty


def test_mape_all_zero_actuals_is_nan():
    result = fb.mape(pd.Series([0.0, 0.0]), pd.Series([1.0, 2.0]))
    assert math.isnan(result)


def test_naive_mean_window_larger_than_series():
    dates = pd.date_range("2018-01-01", periods=3, freq="D")
    series = pd.Series([1.0, 2.0, 3.0], index=dates)
    fc = fb.naive_mean_forecast(series, horizon=2, window=28)  # окно больше длины ряда
    assert len(fc) == 2
    assert (fc == 2.0).all()  # среднее всего ряда [1,2,3]


def test_compute_category_growth_zero_prev_filtered():
    # категория есть только в последнем окне -> prev=0 -> отсекается по min_sales
    df = pd.DataFrame({"date": pd.to_datetime(["2018-08-10"] * 40), "category": ["newcat"] * 40})
    growth = trends.compute_category_growth(df, end="2018-08-22", min_sales=5)
    assert "newcat" not in growth["category"].values


def test_build_sales_mart_no_delivered_orders():
    orders = pd.DataFrame(
        {
            "order_id": ["o1"],
            "order_status": ["canceled"],
            "order_purchase_timestamp": pd.to_datetime(["2018-01-01"]),
        }
    )
    items = pd.DataFrame({"order_id": ["o1"], "product_id": ["p1"], "price": [10.0]})
    products = pd.DataFrame({"product_id": ["p1"], "product_category_name": ["x"]})
    translation = pd.DataFrame({"product_category_name": ["x"], "product_category_name_english": ["y"]})
    mart = prepare_data.build_sales_mart(orders, items, products, translation)
    assert mart.empty
    assert list(mart.columns) == ["date", "order_id", "product_id", "category", "price"]
