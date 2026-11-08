import time
import pandas as pd
from sqlalchemy import create_engine, text
from app.engine.popularity import score_movies
from app.engine.itemcf import make_itemcf
from app.engine.hybrid import make_hybrid


class RecommenderService:
    def __init__(self, db_url="sqlite:///recommender.db"):
        self.engine = create_engine(db_url)
        self.movies = pd.read_sql("SELECT id, title, genres FROM movies", self.engine).set_index("id")
        self.refresh()

    def refresh(self):
        """Reload ratings and retrain the hybrid model."""
        self.ratings = pd.read_sql(
            "SELECT user_id, movie_id, rating, timestamp FROM ratings", self.engine
        )
        ranked = score_movies(self.ratings)["movie_id"].tolist()
        pop = lambda user_id, seen: [m for m in ranked if m not in seen]
        self._recommend = make_hybrid(make_itemcf(self.ratings), pop, w=0.5)

    def get_recommendations(self, user_id, n=10):
        seen = set(self.ratings[self.ratings.user_id == user_id].movie_id)
        ids = self._recommend(user_id, seen)[:n]
        return self.movies.loc[ids].reset_index().to_dict("records")

    def rate_movie(self, user_id, movie_id, rating):
        """Save a rating. Call refresh() to retrain with it."""
        with self.engine.begin() as conn:
            conn.execute(
                text("INSERT INTO ratings (user_id, movie_id, rating, timestamp) "
                     "VALUES (:u, :m, :r, :t)"),
                {"u": int(user_id), "m": int(movie_id), "r": float(rating), "t": int(time.time())},
            )

    def create_user(self, name):
        with self.engine.begin() as conn:
            result = conn.execute(text("INSERT INTO users (name) VALUES (:n)"), {"n": name})
            return result.lastrowid

    def search_movies(self, query, limit=20):
        hits = self.movies[self.movies.title.str.contains(query, case=False, regex=False)]
        return hits.head(limit).reset_index().to_dict("records")


if __name__ == "__main__":
    svc = RecommenderService()
    print("Recommendations for user 1:")
    for m in svc.get_recommendations(1, 5):
        print("  ", m["title"])
    print("Unknown user (falls back to popularity):")
    for m in svc.get_recommendations(99999, 5):
        print("  ", m["title"])
    print("Search 'matrix':", [m["title"] for m in svc.search_movies("matrix", 3)])
