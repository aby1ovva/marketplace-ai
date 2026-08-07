"""Контракт отчётов producer->dashboard: обязательные файлы и их колонки.

Cognitive-debt #3: смена формата отчёта должна ловиться тестом, а не падать
KeyError в дашборде при зелёных unit-тестах.
"""

import pandas as pd
import pytest

import config
import dashboard


def test_required_columns_keys_match_config():
    assert set(dashboard.REQUIRED_COLUMNS) == set(config.DASHBOARD_REQUIRED)


def test_missing_column_is_detected(valid_reports):
    df = pd.read_csv(valid_reports / "trends.csv").drop(columns=["growth_pct"])
    df.to_csv(valid_reports / "trends.csv", index=False)
    with pytest.raises(ValueError, match="growth_pct"):
        dashboard.load_reports(valid_reports)
