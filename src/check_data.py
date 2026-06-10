"""Этап 0: проверка, что данные Olist загружаются и пригодны для работы."""
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent.parent / "data"


def main():
    orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv", parse_dates=["order_purchase_timestamp"])
    items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")
    products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")

    print(f"Заказы:  {len(orders):>7,} строк, период {orders.order_purchase_timestamp.min():%Y-%m-%d} — {orders.order_purchase_timestamp.max():%Y-%m-%d}")
    print(f"Позиции: {len(items):>7,} строк, {items.product_id.nunique():,} уникальных товаров")
    print(f"Товары:  {len(products):>7,} строк, {products.product_category_name.nunique()} категорий")
    print(f"Статусы заказов: {orders.order_status.value_counts().to_dict()}")


if __name__ == "__main__":
    main()
