"""Тесты подготовки данных для Prophet (этап 3). Само обучение в тестах не гоняем — долго."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from forecast_prophet import to_prophet_df


def test_to_prophet_df_format():
    dates = pd.date_range("2018-01-01", periods=5, freq="D")
    series = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0], index=dates)
    df = to_prophet_df(series)
    assert list(df.columns) == ["ds", "y"]
    assert len(df) == 5
    assert df["ds"].iloc[0] == pd.Timestamp("2018-01-01")
    assert df["y"].iloc[-1] == 5.0
