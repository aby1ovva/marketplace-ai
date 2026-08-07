"""Тесты подготовки данных для Prophet (этап 3). Само обучение в тестах не гоняем — долго."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from forecast_prophet import fit_and_forecast, to_prophet_df


def test_fit_and_forecast_shape():
    """Прогноз: ровно horizon строк сразу после конца обучения, с интервалом."""
    dates = pd.date_range("2018-01-01", periods=120, freq="D")
    series = pd.Series([100 + 10 * (d.dayofweek == 0) for d in dates], index=dates, dtype=float)
    fc = fit_and_forecast(series, horizon=14)
    assert len(fc) == 14
    assert list(fc.columns) == ["yhat", "yhat_lower", "yhat_upper"]
    assert fc.index[0] == pd.Timestamp("2018-05-01")
    assert (fc["yhat_lower"] <= fc["yhat_upper"]).all()


def test_to_prophet_df_format():
    dates = pd.date_range("2018-01-01", periods=5, freq="D")
    series = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0], index=dates)
    df = to_prophet_df(series)
    assert list(df.columns) == ["ds", "y"]
    assert len(df) == 5
    assert df["ds"].iloc[0] == pd.Timestamp("2018-01-01")
    assert df["y"].iloc[-1] == 5.0
