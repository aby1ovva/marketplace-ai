# Command surface for POSIX shells / CI / Git-Bash / WSL.
# Windows users without `make`: run the raw commands shown in the README.
.DEFAULT_GOAL := help
PY ?= python

.PHONY: help install install-dev test lint format run-dashboard run-pipeline verify clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install runtime dependencies
	$(PY) -m pip install -r requirements.txt

install-dev: ## Install runtime + dev/test/lint dependencies
	$(PY) -m pip install -r requirements-dev.txt

test: ## Run the test suite with coverage
	$(PY) -m pytest tests --cov=src --cov-report=term-missing

lint: ## Lint with ruff
	$(PY) -m ruff check src tests

format: ## Auto-format with ruff
	$(PY) -m ruff format src tests

run-dashboard: ## Launch the Streamlit dashboard
	$(PY) -m streamlit run src/dashboard.py

run-pipeline: ## Recompute all report artifacts in order (needs data/)
	$(PY) src/prepare_data.py
	$(PY) src/forecast_baseline.py
	$(PY) src/forecast_prophet.py
	$(PY) src/trends.py
	$(PY) src/recommend.py

verify: run-pipeline test ## Headless check: recompute artifacts, then run tests

clean: ## Remove caches and build artifacts
	rm -rf __pycache__ src/__pycache__ tests/__pycache__ \
		.pytest_cache .ruff_cache .coverage htmlcov build dist *.egg-info
