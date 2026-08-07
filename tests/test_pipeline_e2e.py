"""E2E-контракт пайплайна: стадии пишут CSV с колонками, которые читает дашборд.

Пути модулей подменяются на tmp через monkeypatch (main() читает их из модульных
констант в момент вызова) — config.py не трогаем, реальные reports/ не портим.
"""

import json

import pandas as pd
import pytest

import forecast_baseline
import recommend
import trends


def _run_deterministic(pipeline_dir, monkeypatch):
    reports = pipeline_dir / "reports"
    data_csv = pipeline_dir / "data" / "processed" / "sales.csv"
    for mod in (forecast_baseline, trends, recommend):
        monkeypatch.setattr(mod, "DATA_PATH", data_csv)
        monkeypatch.setattr(mod, "REPORTS_DIR", reports)
    for mod in (forecast_baseline, trends):
        monkeypatch.setattr(mod, "FIG_DIR", reports / "figures")
    forecast_baseline.main()
    trends.main()
    recommend.main()
    return reports


def test_deterministic_pipeline_writes_expected_schemas(pipeline_dir, monkeypatch):
    reports = _run_deterministic(pipeline_dir, monkeypatch)

    assert set(pd.read_csv(reports / "trends.csv").columns) >= {"category", "prev", "last", "growth_pct"}

    recs = pd.read_csv(reports / "recs_categories.csv")
    assert set(recs.columns) == {"item_a", "item_b", "together", "confidence", "lift"}

    prods = pd.read_csv(reports / "recs_products.csv")
    assert set(prods.columns) == {"item_a", "item_b", "together", "confidence", "lift"}

    metrics = json.loads((reports / "baseline_metrics.json").read_text(encoding="utf-8"))
    assert {"naive_mean", "seasonal_naive"} <= set(metrics)
    assert "mape" in metrics["naive_mean"]


def test_recs_categories_nonempty_for_crafted_pairs(pipeline_dir, monkeypatch):
    reports = _run_deterministic(pipeline_dir, monkeypatch)
    # crafted furniture_decor<->bed_bath_table (12 заказов) должен пройти порог min_together
    assert not pd.read_csv(reports / "recs_categories.csv").empty


def test_eda_smoke_writes_figures(pipeline_dir, monkeypatch):
    import eda

    reports = pipeline_dir / "reports"
    monkeypatch.setattr(eda, "DATA_PATH", pipeline_dir / "data" / "processed" / "sales.csv")
    monkeypatch.setattr(eda, "FIG_DIR", reports / "figures")
    eda.main()
    # 01-03 на двух языках (6) + 04_daily_sales + 05_top5_dynamics
    assert len(list((reports / "figures").glob("*.png"))) >= 8


@pytest.mark.slow
def test_prophet_pipeline_writes_forecast_schema(pipeline_dir, monkeypatch):
    pytest.importorskip("prophet")
    import forecast_prophet

    reports = pipeline_dir / "reports"
    data_csv = pipeline_dir / "data" / "processed" / "sales.csv"
    monkeypatch.setattr(forecast_baseline, "DATA_PATH", data_csv)
    monkeypatch.setattr(forecast_baseline, "REPORTS_DIR", reports)
    monkeypatch.setattr(forecast_baseline, "FIG_DIR", reports / "figures")
    monkeypatch.setattr(forecast_prophet, "REPORTS_DIR", reports)
    monkeypatch.setattr(forecast_prophet, "FIG_DIR", reports / "figures")

    forecast_baseline.main()  # пишет baseline_metrics.json, который читает prophet
    forecast_prophet.main()

    daily = pd.read_csv(reports / "daily_history.csv")
    assert set(daily.columns) >= {"date", "items"}
    fc = pd.read_csv(reports / "forecast_future.csv")
    assert set(fc.columns) >= {"ds", "yhat", "yhat_lower", "yhat_upper"}
