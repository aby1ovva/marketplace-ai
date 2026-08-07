# Contributing

Thanks for your interest! This is a small solo data project — issues and PRs are welcome.

## Setup

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

**Linux / macOS:** `python3 -m venv .venv && source .venv/bin/activate && make install-dev`

Requires Python 3.14 (see `.python-version`). The Olist dataset is downloaded separately
(see the install snippet in the README) and is not stored in the repo.

## Before you push

```bash
pytest -m "not slow"          # fast suite (skips the heavy Prophet e2e)
ruff check src tests
ruff format --check src tests
```

On Linux/macOS `make test` / `make lint` / `make verify` wrap these. CI runs the same
checks and enforces ≥ 80% coverage.

## What to contribute

- Bug fixes and data-quality checks.
- Forecast / trends / recommender improvements — keep the domain invariants in `AGENTS.md`
  (delivered-orders-only, 28-day windows, `lift > 1` recommendation gate).
- i18n strings (`src/i18n.py`) — keep the `ru` and `en` key sets identical.
- Docs.

## Conventions

- Constants live in `src/config.py` (single source of truth), not inline.
- Lines ≤ 120 chars; `ruff format` is the formatter.
- One logical change per PR; run the checks above; link the issue.
- New code in `src/` should ship with tests (see `tests/`).

More context: `AGENTS.md`, `docs/product-context.md`, `docs/context-map.md`, `docs/decisions/`.
