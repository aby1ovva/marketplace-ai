"""Тесты дашборда: импорт-безопасность, загрузка отчётов, реальный рендер."""

from pathlib import Path

import pytest

import config
import dashboard

DASH = Path(__file__).parent.parent / "src" / "dashboard.py"


def test_import_is_side_effect_free():
    # модуль импортируется, функции доступны, Streamlit при импорте не рендерит
    assert callable(dashboard.main)
    assert callable(dashboard.load_reports)


def test_load_reports_ok(valid_reports):
    frames = dashboard.load_reports(valid_reports)
    assert set(frames) == set(config.DASHBOARD_REQUIRED)
    assert list(frames["trends.csv"].columns) == ["category", "prev", "last", "growth_pct"]


def test_load_reports_missing_file_raises(valid_reports):
    (valid_reports / "trends.csv").unlink()
    with pytest.raises(FileNotFoundError, match="trends.csv"):
        dashboard.load_reports(valid_reports)


def test_dashboard_renders_happy_path():
    """Дашборд рендерится на реальных reports/ репозитория: 4 вкладки, без исключений."""
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(DASH), default_timeout=90)
    at.run()
    assert not at.exception
    assert len(at.tabs) == 4
