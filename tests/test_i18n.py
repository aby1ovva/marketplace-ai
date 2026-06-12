"""Тесты локализации (RU/EN)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from i18n import STRINGS, category_name, t


def test_locales_have_identical_keys():
    assert set(STRINGS["ru"].keys()) == set(STRINGS["en"].keys())


def test_all_strings_non_empty():
    for lang, strings in STRINGS.items():
        for key, value in strings.items():
            assert isinstance(value, str) and value.strip(), f"{lang}.{key} пустая"


def test_category_name_ru_translated():
    assert category_name("bed_bath_table", "ru") == "Спальня и ванная"


def test_category_name_en_prettified():
    assert category_name("bed_bath_table", "en") == "Bed Bath Table"


def test_category_name_unknown_falls_back():
    assert category_name("brand_new_category", "ru") == "brand_new_category"
    assert category_name("brand_new_category", "en") == "Brand New Category"


def test_t_returns_string_for_both_langs():
    assert t("app_title", "ru") != t("app_title", "en")


def test_t_formats_placeholders():
    result = t("metric_forecast_delta", "ru", pct="+12")
    assert "+12" in result
