import pandas as pd
from app.data.models import init_db

def run_import():
    engine = init_db()

    movies = pd.read_csv("data/movies.csv")
    ratings = pd.read_csv("data/ratings.csv")

    movies = movies.rename(columns={"movieId": "id"})

    users = pd.DataFrame({"id": ratings["userId"].unique()})

    ratings = ratings.rename(columns={"userId": "user_id", "movieId": "movie_id"})

    movies.to_sql("movies", engine, if_exists="append", index=False)
    users.to_sql("users", engine, if_exists="append", index=False)
    ratings.to_sql("ratings", engine, if_exists="append", index=False, chunksize=10000)

    print("movies:", len(movies), "users:", len(users), "ratings:", len(ratings))

if __name__ == "__main__":
    run_import()