"""Тесты рекомендаций «покупают вместе» (этап 5)."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from recommend import build_pair_stats, top_recommendations


def make_baskets():
    """4 заказа: A+B вместе дважды, A+C один раз, D всегда один."""
    return pd.DataFrame(
        {
            "order_id": ["o1", "o1", "o2", "o2", "o3", "o3", "o4"],
            "item": ["A", "B", "A", "B", "A", "C", "D"],
        }
    )


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
    recs = top_recommendations(stats, "A", top_n=5)
    assert "A" not in recs["item_b"].values
    assert recs.iloc[0]["item_b"] == "B"  # B чаще покупают с A, чем C


def test_recommend_unknown_item_returns_empty():
    stats = build_pair_stats(make_baskets())
    assert top_recommendations(stats, "ZZZ", top_n=5).empty


def test_recommend_min_lift_filters():
    """Шов для этапа 4: min_lift отсекает пары со слабой связью."""
    stats = build_pair_stats(make_baskets())
    assert not top_recommendations(stats, "A").empty
    assert top_recommendations(stats, "A", min_lift=99).empty


def make_lift_baskets():
    """a↔c — настоящая связь (lift>1); a↔b — анти-корреляция (together есть, lift<1).

    a,c ∈ o1-5 (together=5); b ∈ o4-10 (с a пересекается в 2 заказах).
    lift(a→c)=(5/5)/(5/10)=2.0; lift(a→b)=(2/5)/(7/10)≈0.57.
    """
    rows = []
    for o in ["o1", "o2", "o3", "o4", "o5"]:
        rows += [{"order_id": o, "item": "a"}, {"order_id": o, "item": "c"}]
    for o in ["o4", "o5", "o6", "o7", "o8", "o9", "o10"]:
        rows.append({"order_id": o, "item": "b"})
    return pd.DataFrame(rows)


def test_recommend_excludes_lift_below_floor():
    """Этап 4: рекомендуем только пары с lift > LIFT_FLOOR (связь сильнее случайной)."""
    from config import LIFT_FLOOR

    stats = build_pair_stats(make_lift_baskets())
    recs = top_recommendations(stats, "a", min_lift=LIFT_FLOOR)
    assert "c" in recs["item_b"].values  # настоящая связь остаётся
    assert "b" not in recs["item_b"].values  # анти-коррелированная пара отсеяна
    assert (recs["lift"] > LIFT_FLOOR).all()
