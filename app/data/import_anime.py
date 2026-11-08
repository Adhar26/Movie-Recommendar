import numpy as np
import pandas as pd
from app.data.models import init_db

def run_import(max_users=10000):
    engine = init_db("sqlite:///recommender_anime.db")

    anime = pd.read_csv("data/anime/anime.csv")
    ratings = pd.read_csv("data/anime/rating.csv")

    anime = anime.rename(columns={"anime_id": "id", "name": "title", "genre": "genres"})
    anime["genres"] = anime["genres"].fillna("").str.replace(", ", "|", regex=False)
    anime = anime[["id", "title", "genres"]]

    ratings = ratings[ratings.rating > 0]
    ratings = ratings[ratings.anime_id.isin(anime.id)]
    keep = ratings.user_id.drop_duplicates().head(max_users)
    ratings = ratings[ratings.user_id.isin(keep)].rename(columns={"anime_id": "movie_id"})
    ratings["timestamp"] = np.random.default_rng(0).permutation(len(ratings))

    users = pd.DataFrame({"id": ratings["user_id"].unique()})
    anime.to_sql("movies", engine, if_exists="append", index=False)
    users.to_sql("users", engine, if_exists="append", index=False)
    ratings.to_sql("ratings", engine, if_exists="append", index=False, chunksize=10000)
    print("anime:", len(anime), "users:", len(users), "ratings:", len(ratings))

if __name__ == "__main__":
    run_import()
