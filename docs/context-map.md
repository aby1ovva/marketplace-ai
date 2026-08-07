# Карта контекста: вопрос → правило → тесты → отчёты → код

| Вопрос продавца | Правило | Тесты | Отчёты | Код | ADR |
|---|---|---|---|---|---|
| Сколько закупить | Prophet-прогноз на 28 дней, бьёт baseline по MAPE | `test_prophet.py`, `test_baseline.py`, `test_pipeline_e2e.py` (slow) | `model_metrics.json`, `forecast_future.csv`, `daily_history.csv`, `07_prophet_forecast*.png` | `forecast_prophet.py`, `forecast_baseline.py` | 0001, 0002, 0003 |
| Какие категории растут | Рост за последние 28 дней к предыдущим 28 | `test_trends.py`, `test_pipeline_e2e.py` | `trends.csv`, `08_trends.png` | `trends.py` | 0002 |
| Что предложить в довесок | Пары с `lift > 1` (`LIFT_FLOOR`), ранжир по together/confidence | `test_recommend.py` (вкл. locking), `test_dashboard_contract.py` | `recs_categories.csv` | `recommend.py`, `dashboard.py`, `i18n.py` | 0004 |

## Заметки

- `recs_products.csv` генерируется `recommend.py`, но дашборд его НЕ читает
  (wired-but-unused; решение о товарном уровне — за владельцем).
- Не покрыто тестами: `check_data.py` (0%, одноразовый sanity-скрипт на raw-данных),
  I/O-обвязка `prepare_data.main` / `forecast_prophet.main` (логика покрыта отдельно).
- Все константы — в `src/config.py` (единый источник истины).
