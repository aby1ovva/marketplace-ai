"""Тесты рекомендаций «покупают вместе» (этап 5)."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from recommend import build_pair_stats, recommend


def make_baskets():
    """4 заказа: A+B вместе дважды, A+C один раз, D всегда один."""
    return pd.DataFrame({
        "order_id": ["o1", "o1", "o2", "o2", "o3", "o3", "o4"],
        "item":     ["A",  "B",  "A",  "B",  "A",  "C",  "D"],
    })


def test_pair_counts():
    stats = build_pair_stats(make_baskets())
    ab = stats[(stats["item_a"] == "A") & (stats["item_b"] == "B")].iloc[0]
    assert ab["together"] == 2


def test_confidence():
    stats = build_pair_stats(make_baskets())
    # A встречается в 3 заказах, A+B вместе в 2 => confidence(A->B) = 2/3
    ab = stats[(stats["item_a"] == "A") & (stats["item_b"] == "B")].iloc[0]
    assert abs(ab["confidence"] - 2 / 3) < 1e-9


def test_lift():
    stats = build_pair_stats(make_baskets())
    # lift(A->B) = confidence / P(B) = (2/3) / (2/4) = 4/3
    ab = stats[(stats["item_a"] == "A") & (stats["item_b"] == "B")].iloc[0]
    assert abs(ab["lift"] - 4 / 3) < 1e-9


def test_both_directions_present():
    stats = build_pair_stats(make_baskets())
    assert ((stats["item_a"] == "B") & (stats["item_b"] == "A")).any()


def test_recommend_sorted_and_excludes_self():
    stats = build_pair_stats(make_baskets())
    recs = recommend(stats, "A", top_n=5)
    assert "A" not in recs["item_b"].values
    assert recs.iloc[0]["item_b"] == "B"  # B чаще покупают с A, чем C


def test_recommend_unknown_item_returns_empty():
    stats = build_pair_stats(make_baskets())
    assert recommend(stats, "ZZZ", top_n=5).empty
