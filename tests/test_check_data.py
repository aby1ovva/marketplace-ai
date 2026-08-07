"""Smoke-тест sanity-проверки сырых данных Olist (этап 0)."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import check_data


def _write_raw(data_dir):
    pd.DataFrame(
        {
            "order_id": ["o1", "o2"],
            "order_status": ["delivered", "canceled"],
            "order_purchase_timestamp": pd.to_datetime(["2018-01-05 10:00", "2018-02-10 12:00"]),
        }
    ).to_csv(data_dir / "olist_orders_dataset.csv", index=False)
    pd.DataFrame({"order_id": ["o1", "o1"], "product_id": ["p1", "p2"], "price": [10.0, 20.0]}).to_csv(
        data_dir / "olist_order_items_dataset.csv", index=False
    )
    pd.DataFrame({"product_id": ["p1", "p2"], "product_category_name": ["auto", "toys"]}).to_csv(
        data_dir / "olist_products_dataset.csv", index=False
    )


def test_check_data_runs_on_raw_fixtures(tmp_path, monkeypatch, capsys):
    _write_raw(tmp_path)
    monkeypatch.setattr(check_data, "DATA_DIR", tmp_path)
    check_data.main()  # не должно падать на валидных сырых данных
    out = capsys.readouterr().out
    assert "Заказы:" in out and "Позиции:" in out
