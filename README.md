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

## Запуск

Пересчёт всех артефактов (по порядку), затем дашборд:

```powershell
.venv\Scripts\python src\prepare_data.py      # витрина продаж
.venv\Scripts\python src\forecast_baseline.py # baseline-метрики
.venv\Scripts\python src\forecast_prophet.py  # модель + прогноз на 28 дней
.venv\Scripts\python src\trends.py            # тренды категорий
.venv\Scripts\python src\recommend.py         # «покупают вместе»
.venv\Scripts\streamlit run src\dashboard.py  # дашборд: http://localhost:8501
```

Тесты:

```powershell
.venv\Scripts\python -m pytest tests
```

## Этапы проекта

- [x] Этап 0 — окружение и данные
- [x] Этап 1 — очистка данных + EDA
- [x] Этап 2 — baseline-прогноз (naive_mean: MAPE 24.0%, seasonal_naive: 26.7%)
- [x] Этап 3 — модель прогноза (Prophet: MAPE 20.9% — лучше baseline на 3.1 п.п.)
- [x] Этап 4 — аналитика трендов (рост категорий: 28 дней к предыдущим 28)
- [x] Этап 5 — рекомендации «покупают вместе» (частые пары: confidence + lift)
- [x] Этап 6 — Streamlit-дашборд (прогноз / тренды / рекомендации)
