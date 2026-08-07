# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-08-07

First tagged release. Bundles the original demo with a full reproducibility,
testing, and documentation pass.

### Added
- Data prep from raw Olist CSVs (delivered orders only), EDA figures.
- Baseline forecast (naive_mean 24.01% / seasonal_naive 26.7% MAPE) and Prophet
  forecast (20.94% MAPE); category trends; bought-together recommender.
- Bilingual (RU/EN) Streamlit dashboard.
- Reproducible setup: pinned `requirements.txt` + `requirements-dev.txt`, `Makefile`,
  `ruff` config, `src/config.py` as the single source of truth for constants.
- Tests: unit + end-to-end pipeline + dashboard render/contract + edge cases
  (coverage 31% → 84%).
- CI (GitHub Actions): pytest with an 80% coverage gate + `ruff` lint/format checks.
- AI/contributor context: `AGENTS.md`, `docs/product-context.md`, `docs/context-map.md`,
  `docs/decisions/0001-0004` (ADRs).
- Community health: `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue/PR templates.

### Changed
- Recommendations are gated by `lift > 1` (`LIFT_FLOOR`), so the dashboard no longer
  surfaces weaker-than-chance pairs (e.g. `bed_bath_table → furniture_decor`, lift 0.64).

### Fixed
- Removed dead code and duplicated constants; the README no longer references a
  non-existent `notebooks/` directory.

[Unreleased]: https://github.com/aby1ovva/marketplace-ai-clean/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/aby1ovva/marketplace-ai-clean/releases/tag/v0.1.0
