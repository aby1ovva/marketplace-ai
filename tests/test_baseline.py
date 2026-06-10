"""Тесты baseline-прогноза (этап 2)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from forecast_baseline import mape, naive_mean_forecast, seasonal_naive_forecast


def test_mape_basic():
    actual = pd.Series([100.0, 200.0])
    forecast = pd.Series([110.0, 180.0])
    # (10/100 + 20/200) / 2 = 10%
    assert mape(actual, forecast) == 10.0


def test_mape_ignores_zero_actuals():
    actual = pd.Series([100.0, 0.0])
    forecast = pd.Series([110.0, 50.0])
    assert mape(actual, forecast) == 10.0


def test_naive_mean_forecast_is_window_mean():
    dates = pd.date_range("2018-01-01", periods=30, freq="D")
    series = pd.Series(np.arange(30, dtype=float), index=dates)
    fc = naive_mean_forecast(series, horizon=5, window=10)
    # среднее последних 10 значений: mean(20..29) = 24.5
    assert len(fc) == 5
    assert (fc == 24.5).all()
    assert fc.index[0] == pd.Timestamp("2018-01-31")


def test_seasonal_naive_uses_same_weekday():
    dates = pd.date_range("2018-01-01", periods=28, freq="D")  # 4 полных недели, Пн-Вс
    # понедельники = 100, остальные дни = 10
    values = [100.0 if d.dayofweek == 0 else 10.0 for d in dates]
    series = pd.Series(values, index=dates)
    fc = seasonal_naive_forecast(series, horizon=7)
    # прогноз на следующий понедельник должен быть 100, на остальные дни 10
    for date, val in fc.items():
        assert val == (100.0 if date.dayofweek == 0 else 10.0)
