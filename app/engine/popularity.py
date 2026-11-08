import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///recommender.db")

def score_movies(ratings, m=50):
    C = ratings["rating"].mean()
    stats = ratings.groupby("movie_id")["rating"].agg(["count", "mean"]).reset_index()
    stats = stats[stats["count"] >= m].copy()
    v, R = stats["count"], stats["mean"]
    stats["score"] = (v / (v + m)) * R + (m / (v + m)) * C
    return stats.sort_values("score", ascending=False)

def popular_movies(n=10, m=50):
    ratings = pd.read_sql("SELECT movie_id, rating FROM ratings", engine)
    movies = pd.read_sql("SELECT id, title FROM movies", engine)
    top = score_movies(ratings, m).head(n)
    return top.merge(movies, left_on="movie_id", right_on="id")[["title", "count", "mean", "score"]]

if __name__ == "__main__":
    print(popular_movies())
