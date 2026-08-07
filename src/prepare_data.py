"""Этап 1: сборка витрины продаж из сырых CSV Olist.

Витрина: одна строка = одна проданная позиция.
Колонки: date | order_id | product_id | category | price
Только доставленные заказы (delivered), категории переведены на английский.
"""
import sys

import pandas as pd

from config import DATA_DIR, DATA_PATH

sys.stdout.reconfigure(encoding="utf-8")


def build_sales_mart(orders, items, products, translation):
    delivered = orders[orders["order_status"] == "delivered"]

    mart = (
        items.merge(delivered[["order_id", "order_purchase_timestamp"]], on="order_id", how="inner")
        .merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
        .merge(translation, on="product_category_name", how="left")
    )
    mart["category"] = mart["product_category_name_english"].fillna("unknown")
    mart["date"] = mart["order_purchase_timestamp"].dt.normalize()

    return mart[["date", "order_id", "product_id", "category", "price"]].sort_values("date").reset_index(drop=True)


def main():
    orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv", parse_dates=["order_purchase_timestamp"])
    items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")
    products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")
    translation = pd.read_csv(DATA_DIR / "product_category_name_translation.csv")

    mart = build_sales_mart(orders, items, products, translation)

    DATA_PATH.parent.mkdir(exist_ok=True)
    mart.to_csv(DATA_PATH, index=False)

    print(f"Витрина сохранена: {DATA_PATH}")
    print(f"Строк: {len(mart):,} (позиций доставленных заказов)")
    print(f"Период: {mart.date.min():%Y-%m-%d} — {mart.date.max():%Y-%m-%d}")
    print(f"Товаров: {mart.product_id.nunique():,}, категорий: {mart.category.nunique()}")
    print(f"Выручка всего: R$ {mart.price.sum():,.0f}")


if __name__ == "__main__":
    main()
