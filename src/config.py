"""Единый источник констант проекта.

Раньше эти значения дублировались по модулям src/ (пути к данным и отчётам,
dpi графиков, языки интерфейса, top-N, пороги рекомендаций, имена артефактов).
Теперь любое из них меняется в одном месте.
"""

from pathlib import Path

_ROOT = Path(__file__).parent.parent

# --- Пути ---
DATA_DIR = _ROOT / "data"  # сырые CSV Olist
DATA_PATH = DATA_DIR / "processed" / "sales.csv"  # витрина продаж (вход пайплайна)
REPORTS_DIR = _ROOT / "reports"
FIG_DIR = REPORTS_DIR / "figures"

# --- Графики ---
DPI = 120

# --- Интерфейс дашборда ---
LANGS = ("ru", "en")
DEFAULT_TOP_N = 5

# --- Пороги рекомендаций (этап 5) ---
MIN_TOGETHER_PRODUCTS = 3  # минимум совместных покупок для пар товаров
MIN_TOGETHER_CATEGORIES = 10  # минимум для пар категорий
STRONG_LIFT = 2  # lift > STRONG_LIFT => «сильная» связка (см. этап 4)
STRONG_MIN_TOGETHER = 15  # и одновременно together >= этого порога
TOP_STRONG_RULES = 8  # сколько сильных правил печатать

# --- Имена артефактов в reports/ ---
BASELINE_METRICS = "baseline_metrics.json"
MODEL_METRICS = "model_metrics.json"
FORECAST_FUTURE = "forecast_future.csv"
DAILY_HISTORY = "daily_history.csv"
TRENDS_CSV = "trends.csv"
RECS_CATEGORIES = "recs_categories.csv"
RECS_PRODUCTS = "recs_products.csv"

# Файлы, без которых дашборд не стартует
DASHBOARD_REQUIRED = (FORECAST_FUTURE, DAILY_HISTORY, TRENDS_CSV, RECS_CATEGORIES)
