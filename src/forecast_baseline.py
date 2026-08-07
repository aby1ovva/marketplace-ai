"""Этап 2: наивный baseline-прогноз дневных продаж.

Два метода:
- naive_mean: среднее за последние N дней (игнорирует сезонность)
- seasonal_naive: среднее по тому же дню недели за последние 4 недели

Метрики сохраняются в reports/baseline_metrics.json — планка для этапа 3.
"""

import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from config import BASELINE_METRICS, DATA_PATH, DPI, FIG_DIR, REPORTS_DIR

TRAIN_START = "2017-01-01"  # 2016 почти пустой — исключаем (вывод EDA)
SERIES_END = "2018-08-22"  # последние дни датасета неполные — обрезаем
TEST_DAYS = 28  # горизонт проверки — 4 недели

sys.stdout.reconfigure(encoding="utf-8")


def mape(actual, forecast):
    """Средняя абсолютная процентная ошибка, %. Нулевые факты пропускаются."""
    actual = pd.Series(actual.values, dtype=float)
    forecast = pd.Series(forecast.values, dtype=float)
    mask = actual != 0
    return float((abs(actual[mask] - forecast[mask]) / actual[mask]).mean() * 100)


def future_index(series, horizon):
    return pd.date_range(series.index[-1] + pd.Timedelta(days=1), periods=horizon, freq="D")


def naive_mean_forecast(series, horizon, window=28):
    """Прогноз = среднее последних `window` дней, одинаковое на весь горизонт."""
    value = series.iloc[-window:].mean()
    return pd.Series(value, index=future_index(series, horizon))


def seasonal_naive_forecast(series, horizon, weeks=4):
    """Прогноз = среднее по тому же дню недели за последние `weeks` недель."""
    tail = series.iloc[-weeks * 7 :]
    by_weekday = tail.groupby(tail.index.dayofweek).mean()
    idx = future_index(series, horizon)
    return pd.Series([by_weekday[d.dayofweek] for d in idx], index=idx)


def load_daily_series():
    sales = pd.read_csv(DATA_PATH, parse_dates=["date"])
    daily = sales.groupby("date")["price"].count().asfreq("D", fill_value=0)
    return daily.loc[TRAIN_START:SERIES_END].rename("items")


def main():
    daily = load_daily_series()
    train, test = daily.iloc[:-TEST_DAYS], daily.iloc[-TEST_DAYS:]
    print(f"Обучение: {train.index[0]:%Y-%m-%d} — {train.index[-1]:%Y-%m-%d} ({len(train)} дней)")
    print(f"Проверка: {test.index[0]:%Y-%m-%d} — {test.index[-1]:%Y-%m-%d} ({len(test)} дней)\n")

    forecasts = {
        "naive_mean": naive_mean_forecast(train, TEST_DAYS),
        "seasonal_naive": seasonal_naive_forecast(train, TEST_DAYS),
    }

    metrics = {}
    for name, fc in forecasts.items():
        metrics[name] = {"mape": round(mape(test, fc), 2), "mae": round(float(abs(test - fc).mean()), 1)}
        print(f"{name:>15}: MAPE = {metrics[name]['mape']:.1f}%, MAE = {metrics[name]['mae']:.0f} позиций/день")

    REPORTS_DIR.mkdir(exist_ok=True)
    (REPORTS_DIR / BASELINE_METRICS).write_text(json.dumps(metrics, indent=2))
    print("\nМетрики сохранены: reports/baseline_metrics.json")

    fig, ax = plt.subplots(figsize=(11, 5))
    daily.iloc[-90:].plot(ax=ax, color="steelblue", label="Факт")
    forecasts["naive_mean"].plot(ax=ax, color="gray", linestyle="--", label="Наивный (среднее 28 дн.)")
    forecasts["seasonal_naive"].plot(ax=ax, color="crimson", label="Сезонно-наивный (дни недели)")
    ax.set_ylabel("Позиций в день")
    ax.set_title(f"Baseline-прогноз на {TEST_DAYS} дней")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / "06_baseline_forecast.png", dpi=DPI)
    print("График: reports/figures/06_baseline_forecast.png")


if __name__ == "__main__":
    main()
