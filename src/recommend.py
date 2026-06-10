"""Этап 5: рекомендации «покупают вместе» по корзинам заказов.

Считаем частые пары товаров/категорий в одном заказе (эквивалент Apriori для пар):
- together   — в скольких заказах пара встретилась вместе
- confidence — P(B в заказе | A в заказе)
- lift       — насколько связь сильнее случайности (>1 = неслучайно)

Результаты: reports/recs_products.csv и reports/recs_categories.csv.
"""
import sys
from itertools import combinations
from pathlib import Path

import pandas as pd

from forecast_baseline import DATA_PATH

REPORTS_DIR = Path(__file__).parent.parent / "reports"

sys.stdout.reconfigure(encoding="utf-8")


def build_pair_stats(baskets, min_together=1):
    """baskets: DataFrame[order_id, item] -> статистика пар в обе стороны."""
    order_items = baskets.groupby("order_id")["item"].apply(lambda s: sorted(set(s)))
    n_orders = len(order_items)
    item_orders = baskets.groupby("item")["order_id"].nunique()

    pair_counts = {}
    for items in order_items:
        for a, b in combinations(items, 2):
            pair_counts[(a, b)] = pair_counts.get((a, b), 0) + 1

    rows = []
    for (a, b), together in pair_counts.items():
        if together < min_together:
            continue
        for x, y in [(a, b), (b, a)]:
            confidence = together / item_orders[x]
            lift = confidence / (item_orders[y] / n_orders)
            rows.append({"item_a": x, "item_b": y, "together": together,
                         "confidence": confidence, "lift": lift})

    return pd.DataFrame(rows, columns=["item_a", "item_b", "together", "confidence", "lift"])


def recommend(pair_stats, item, top_n=5):
    """Топ сопутствующих к `item`: чаще вместе -> выше confidence."""
    recs = pair_stats[pair_stats["item_a"] == item]
    return recs.sort_values(["together", "confidence"], ascending=False).head(top_n)


def main():
    sales = pd.read_csv(DATA_PATH, parse_dates=["date"])

    multi = sales.groupby("order_id")["product_id"].nunique()
    multi_orders = multi[multi >= 2]
    print(f"Заказов всего: {multi.size:,}, из них с 2+ разными товарами: {len(multi_orders):,} "
          f"({len(multi_orders) / multi.size:.1%})")

    # Уровень товаров: только заказы с 2+ товарами, пары от 3 совместных покупок
    basket_sales = sales[sales["order_id"].isin(multi_orders.index)]
    prod_stats = build_pair_stats(
        basket_sales.rename(columns={"product_id": "item"})[["order_id", "item"]], min_together=3
    )
    prod_stats.sort_values("together", ascending=False).to_csv(REPORTS_DIR / "recs_products.csv", index=False)
    print(f"Пар товаров (3+ совместные покупки): {len(prod_stats) // 2}")

    # Уровень категорий: читаемые правила для дашборда.
    # Вселенная для lift — только заказы с 2+ товарами: среди одиночных заказов
    # совместная покупка невозможна, и lift по всем заказам всегда был бы < 1.
    cat_stats = build_pair_stats(
        basket_sales.rename(columns={"category": "item"})[["order_id", "item"]], min_together=10
    )
    cat_stats.sort_values("together", ascending=False).to_csv(REPORTS_DIR / "recs_categories.csv", index=False)

    strong = cat_stats[(cat_stats["lift"] > 2) & (cat_stats["together"] >= 15)]
    top_rules = strong.sort_values("together", ascending=False).drop_duplicates("item_a").head(8)
    print("\nСильные связки категорий (lift > 2, неслучайные):")
    for _, r in top_rules.iterrows():
        print(f"  {r['item_a']:<28} -> {r['item_b']:<28} вместе {int(r['together']):>3} раз, "
              f"confidence {r['confidence']:.0%}, lift {r['lift']:.0f}")

    top_prod = prod_stats.sort_values("together", ascending=False).iloc[0]
    print(f"\nСамая частая пара товаров: {top_prod['item_a'][:8]}... + {top_prod['item_b'][:8]}... "
          f"({int(top_prod['together'])} совместных заказов)")


if __name__ == "__main__":
    main()
