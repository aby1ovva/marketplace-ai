# AGENTS.md — guide for AI agents and contributors

Marketplace AI is a small solo **Python 3.14 + Streamlit** data project: sales
forecasting, category trends and "bought-together" recommendations for marketplace
sellers, built on the public **Olist** Brazilian e-commerce dataset. Claude Code is
the primary developer here. Read this before editing.

## What you may edit

- `src/` (pipeline + dashboard), `tests/`, `docs/`, `README.md`.
- **Never** edit `data/` (git-ignored, downloaded from Kaggle) or hand-edit files in
  `reports/` — those are generated (see policy below).
- Constants live in `src/config.py` — the single source of truth for paths, DPI,
  languages, recommendation thresholds and artifact names. Change a value there, not
  inline in a script.

## Pipeline / run order

Scripts run in this order (each reads `data/processed/sales.csv` and/or `reports/`):

1. `prepare_data.py` → builds `data/processed/sales.csv` (delivered orders only).
2. `forecast_baseline.py` → `reports/baseline_metrics.json`, `figures/06_baseline_forecast.png`.
3. `forecast_prophet.py` → `reports/model_metrics.json`, `forecast_future.csv`,
   `daily_history.csv`, `figures/07_prophet_forecast*.png`.
4. `trends.py` → `reports/trends.csv`, `figures/08_trends.png`.
5. `recommend.py` → `reports/recs_categories.csv`.
6. `dashboard.py` (Streamlit) → reads pre-computed `reports/`, trains nothing.

`make run-pipeline` runs steps 1–5 headless; `make run-dashboard` launches the UI.

## Safe-edit boundaries (domain invariants — do not break)

- **Delivered orders only.** The sales mart keeps `order_status == "delivered"`.
- **28-day windows.** `TEST_DAYS = 28` is the forecast holdout (last 4 weeks hidden,
  compared to actuals). Trends compare the last 28 days vs the previous 28.
- **Meaning of lift.** `lift > 1` = a pair co-occurs more than chance; `lift < 1` =
  weaker than chance. A recommendation must never surface a `lift <= 1` pair, even with
  high `together`. Canonical trap: for `bed_bath_table` the pair `furniture_decor` has
  together=70 but **lift=0.64** — it must NOT be recommended (gated by `LIFT_FLOOR`; see
  `docs/decisions/0004-recommend-by-lift-gate.md`). The correct top pair is
  `home_confort` (lift 2.99).
- **Training window.** `TRAIN_START=2017-01-01`, `SERIES_END=2018-08-22` (2016 is empty,
  the tail is incomplete). Metrics are valid only inside this window
  (`docs/decisions/0001-training-window.md`).

## Verify your change

Linux/macOS:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -m "not slow"            # fast suite
ruff check src tests && ruff format --check src tests
```

Windows (PowerShell):

```powershell
python -m venv .venv; .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
.venv\Scripts\python -m pytest -m "not slow"
```

`-m "not slow"` skips the Prophet end-to-end test (heavy). Coverage floor is 80%
(enforced in CI).

## reports/ regeneration policy

`reports/` artifacts are committed (the dashboard and README render them offline).
Treat them as a generated cache: regenerate ONLY by re-running the owning script
(mapping above). Never hand-edit a CSV/JSON/PNG. Figures `07_prophet_forecast` and
`08_trends` are also embedded in the README as demos.

## Handoff

- GitHub **Issues are enabled** — open one for scope or acceptance questions.
- Project convention: quiz/question text in **English**, explanations in **Russian**.
- More context: `docs/product-context.md`, `docs/context-map.md`, `docs/decisions/`.
