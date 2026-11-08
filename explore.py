import pandas as pd

movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/ratings.csv")

print(movies.head())
print(ratings.head())
print("movies:", len(movies))
print("users:", ratings.userId.nunique())
print("ratings:", len(ratings))

n_users = ratings.userId.nunique()
n_movies = ratings.movieId.nunique()
sparsity = 1 - len(ratings) / (n_users * n_movies)
print("sparsity:", round(sparsity * 100, 2), "%")

top = (ratings.groupby("movieId").size()
       .sort_values(ascending=False).head(10)
       .reset_index(name="num_ratings")
       .merge(movies, on="movieId"))
print(top[["title", "num_ratings"]])

print(ratings.rating.value_counts().sort_index())
