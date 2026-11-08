# Copilot Instructions

## Project

This is a Python movie recommender with a PySide6 desktop UI, a FastAPI API module, SQLAlchemy/SQLite persistence, and pandas/scikit-learn/SciPy recommendation engines. Keep changes focused and preserve the existing module boundaries.

## Structure

- `app/data/`: SQLAlchemy models and MovieLens CSV import.
- `app/engine/`: popularity, content-based, item-based collaborative filtering, hybrid ranking, and evaluation.
- `app/core/service.py`: shared service used by the UI and API.
- `app/ui/main_window.py`: PySide6 desktop interface.
- `app/api.py`: FastAPI endpoints.
- `launcher.py`: desktop launcher, including the frozen-app working-directory adjustment.

## Data and runtime

- The importer reads `data/movies.csv` and `data/ratings.csv` relative to the project working directory. Keep the MovieLens column names expected by `app/data/importer.py` in mind (`movieId`, `userId`, `rating`, and `timestamp`).
- SQLite defaults to `recommender.db` in the current working directory. Do not commit generated databases, datasets, caches, or credentials.
- `tmdb_key.txt` is ignored and must remain local; never log or expose its contents.
- Treat the README as potentially stale: `requirements.txt` does not currently list PySide6, and `app/api.py` imports `app.data.posters`, which is not present in the repository. Verify these before relying on desktop or poster/API setup instructions.

## Commands

- Create database schema: `python -m app.data.models`
- Import the CSV dataset: `python -m app.data.importer`
- Evaluate popularity: `python -m app.engine.evaluate`
- Compare recommenders: `python -m app.engine.compare`
- Start the desktop app: `python -m app.ui.main_window` (requires PySide6 and initialized data/database)
- Start the API only after resolving/verifying its poster-module import: `uvicorn app.api:app --reload`

There is no test suite or test configuration in the repository currently. For behavior changes, add focused tests when practical and at minimum run a relevant module or compile check. Avoid commands that assume MovieLens data or a populated database is available.

## Implementation conventions

- Keep recommendation logic in `app/engine/`; use `RecommenderService` for data access and orchestration shared by interfaces.
- Use SQLAlchemy parameterized statements for writes and preserve the existing SQLite schema unless a change requires a migration or compatible initialization path.
- Keep paths and defaults compatible with the project's current working-directory-based execution unless explicitly updating all entry points.
- Preserve the existing straightforward Python style; avoid unrelated refactors and new dependencies unless necessary.
