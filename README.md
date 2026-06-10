# Marketplace AI

AI-система аналитики для маркетплейса: прогноз продаж, анализ трендов, рекомендации товаров.

Данные: [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — реальный бразильский маркетплейс, ~100k заказов за 2016–2018.

## Структура

- `data/` — CSV-файлы датасета (не в git, скачиваются скриптом)
- `notebooks/` — Jupyter-ноутбуки для анализа (EDA, эксперименты с моделями)
- `src/` — Python-скрипты (подготовка данных, модели, дашборд)

## Установка

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python -c "import kagglehub, shutil, pathlib; p = kagglehub.dataset_download('olistbr/brazilian-ecommerce'); [shutil.copy(f, 'data') for f in pathlib.Path(p).glob('*.csv')]"
```

## Проверка данных

```powershell
.venv\Scripts\python src\check_data.py
```

## Этапы проекта

- [x] Этап 0 — окружение и данные
- [x] Этап 1 — очистка данных + EDA
- [x] Этап 2 — baseline-прогноз (naive_mean: MAPE 24.0%, seasonal_naive: 26.7%)
- [x] Этап 3 — модель прогноза (Prophet: MAPE 20.9% — лучше baseline на 3.1 п.п.)
- [ ] Этап 4 — аналитика трендов
- [ ] Этап 5 — рекомендации «покупают вместе»
- [ ] Этап 6 — Streamlit-дашборд
