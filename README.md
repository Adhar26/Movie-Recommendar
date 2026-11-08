# Hybrid Movie Recommender (Desktop App)

A Netflix-style desktop app that recommends movies using a hybrid of popularity and item-based collaborative filtering, trained on the MovieLens dataset.

## Features
- Personalized recommendation row per user
- Cold-start fallback to popularity for new users
- Star ratings that feed back into the model (background retraining)
- Movie search and TMDB posters (cached locally)

## Results (time-based split, last 20% of each user's ratings held out)

| Model | Precision@10 | Recall@10 |
|---|---|---|
| Popularity (weighted rating) | 0.0591 | 0.0496 |
| Content-based (genres, TF-IDF) | 0.0056 | 0.0071 |
| Item-based CF | 0.0468 | 0.0412 |
| **Hybrid (w=0.5, rank fusion)** | **0.0718** | **0.0600** |

The hybrid improves on the popularity baseline by about 21%. Genre-only content filtering is weak because many movies share the same genres.

## Architecture
@'
# Hybrid Movie Recommender (Desktop App)

A Netflix-style desktop app that recommends movies using a hybrid of popularity and item-based collaborative filtering, trained on the MovieLens dataset.

## Features
- Personalized recommendation row per user
- Cold-start fallback to popularity for new users
- Star ratings that feed back into the model (background retraining)
- Movie search and TMDB posters (cached locally)

## Results (time-based split, last 20% of each user's ratings held out)

| Model | Precision@10 | Recall@10 |
|---|---|---|
| Popularity (weighted rating) | 0.0591 | 0.0496 |
| Content-based (genres, TF-IDF) | 0.0056 | 0.0071 |
| Item-based CF | 0.0468 | 0.0412 |
| **Hybrid (w=0.5, rank fusion)** | **0.0718** | **0.0600** |

The hybrid improves on the popularity baseline by about 21%. Genre-only content filtering is weak because many movies share the same genres.

## Architecture
- app/data: SQLite models, CSV importer, poster fetcher
- app/engine: popularity, content, itemcf, hybrid, evaluate
- app/core: RecommenderService (used by the UI)
- app/ui: PySide6 desktop window

## Setup
1. python -m venv venv, then activate it
2. pip install pandas numpy scikit-learn scipy sqlalchemy PySide6
3. Download MovieLens ml-latest-small. Put movies.csv and ratings.csv in data/, and keep links.csv in data/ml-latest-small/
4. python -m app.data.models, then python -m app.data.importer
5. Optional, for posters: create tmdb_key.txt containing your TMDB API key
6. Run: python -m app.ui.main_window

Evaluate the models: python -m app.engine.compare

## Tech
Python, pandas, scikit-learn, SciPy, SQLAlchemy, SQLite, PySide6
