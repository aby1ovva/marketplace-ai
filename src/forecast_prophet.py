"""Этап 3: прогноз дневных продаж моделью Prophet.

Тренд + недельная и годовая сезонность + бразильские праздники.
Сравнение с baseline из reports/baseline_metrics.json (этап 2).
"""
import json
import logging
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from prophet import Prophet

from config import BASELINE_METRICS, DAILY_HISTORY, DPI, FIG_DIR, FORECAST_FUTURE, MODEL_METRICS, REPORTS_DIR
from forecast_baseline import TEST_DAYS, load_daily_series, mape

sys.stdout.reconfigure(encoding="utf-8")
logging.getLogger("cmdstanpy").setLevel(logging.WARNING)


def to_prophet_df(series):
    """pd.Series с DatetimeIndex -> DataFrame формата Prophet (ds, y)."""
    return series.rename_axis("ds").rename("y").reset_index()


def fit_and_forecast(train, horizon):
    model = Prophet(weekly_seasonality=True, yearly_seasonality=True, daily_seasonality=False)
    model.add_country_holidays(country_name="BR")  # Black Friday и праздники — вывод EDA
    model.fit(to_prophet_df(train))

    future = model.make_future_dataframe(periods=horizon)
    forecast = model.predict(future).tail(horizon)
    return forecast.set_index("ds")[["yhat", "yhat_lower", "yhat_upper"]]


def main():
    daily = load_daily_series()
    train, test = daily.iloc[:-TEST_DAYS], daily.iloc[-TEST_DAYS:]
    print(f"Обучение: {train.index[0]:%Y-%m-%d} — {train.index[-1]:%Y-%m-%d}, проверка: {TEST_DAYS} дней")

    forecast = fit_and_forecast(train, TEST_DAYS)

    metrics = {"mape": round(mape(test, forecast["yhat"]), 2),
               "mae": round(float(abs(test - forecast["yhat"]).mean()), 1)}
    baseline = json.loads((REPORTS_DIR / BASELINE_METRICS).read_text())
    best_baseline = min(m["mape"] for m in baseline.values())

    print(f"\nProphet:        MAPE = {metrics['mape']:.1f}%, MAE = {metrics['mae']:.0f} позиций/день")
    print(f"Лучший baseline: MAPE = {best_baseline:.1f}%")
    verdict = "ЛУЧШЕ baseline" if metrics["mape"] < best_baseline else "НЕ лучше baseline"
    print(f"Вывод: Prophet {verdict} (разница {best_baseline - metrics['mape']:+.1f} п.п.)")

    (REPORTS_DIR / MODEL_METRICS).write_text(json.dumps({"prophet": metrics}, indent=2))

    # График валидации — на двух языках (показывается в дашборде)
    mape_note = f"(MAPE {metrics['mape']:.1f}% vs baseline {best_baseline:.1f}%)"
    chart_labels = {
        "ru": {"fact": "Факт", "interval": "Доверительный интервал", "y": "Позиций в день",
               "title": f"Prophet: прогноз на {TEST_DAYS} дней {mape_note}",
               "file": "07_prophet_forecast.png"},
        "en": {"fact": "Actual", "interval": "Confidence interval", "y": "Items per day",
               "title": f"Prophet: {TEST_DAYS}-day forecast {mape_note}",
               "file": "07_prophet_forecast_en.png"},
    }
    for L in chart_labels.values():
        fig, ax = plt.subplots(figsize=(11, 5))
        daily.iloc[-90:].plot(ax=ax, color="steelblue", label=L["fact"])
        forecast["yhat"].plot(ax=ax, color="crimson", linewidth=1.8, label="Prophet")
        ax.fill_between(forecast.index, forecast["yhat_lower"], forecast["yhat_upper"],
                        color="crimson", alpha=0.15, label=L["interval"])
        ax.set_ylabel(L["y"])
        ax.set_title(L["title"])
        ax.legend()
        fig.tight_layout()
        fig.savefig(FIG_DIR / L["file"], dpi=DPI)
        print(f"График: reports/figures/{L['file']}")

    # Прогноз в будущее (за пределы данных) — обучение на всём ряде, читает дашборд
    future_fc = fit_and_forecast(daily, TEST_DAYS)
    future_fc.round(1).to_csv(REPORTS_DIR / FORECAST_FUTURE)
    daily.to_csv(REPORTS_DIR / DAILY_HISTORY)
    print("Прогноз для дашборда: reports/forecast_future.csv")


if __name__ == "__main__":
    main()
