# reports/ — generated artifacts

These files are **generated** by the pipeline scripts (see the run order in the root
`README.md` / `AGENTS.md`). Do not edit them by hand — regenerate by re-running the
owning script.

- `baseline_metrics.json`, `model_metrics.json` — forecast metrics.
- `daily_history.csv`, `forecast_future.csv` — history + Prophet forecast.
- `trends.csv` — category growth.
- `recs_products.csv`, `recs_categories.csv` — bought-together pairs.
- `figures/*.png` — charts (`07_prophet_forecast` and `08_trends` are embedded in the
  root README as demos).

## Licensing of derived data

These artifacts are **derived from the Olist Brazilian E-Commerce dataset**, distributed
on Kaggle under **CC BY-NC-SA 4.0** (attribution, non-commercial, share-alike). The project
**code** is MIT (see `LICENSE`), but these derived CSV/JSON/PNG files carry the dataset's
CC BY-NC-SA 4.0 terms. This is a maintainer's best-effort note, not legal advice — confirm
the exact terms before any commercial or redistributive use.
