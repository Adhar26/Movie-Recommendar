import pandas as pd
from sqlalchemy import create_engine
from app.engine.popularity import score_movies

engine = create_engine("sqlite:///recommender.db")

def load_ratings():
    return pd.read_sql("SELECT user_id, movie_id, rating, timestamp FROM ratings", engine)

def split(ratings, test_frac=0.2):
    ratings = ratings.sort_values(["user_id", "timestamp"])
    rank = ratings.groupby("user_id").cumcount(ascending=False)
    size = ratings.groupby("user_id")["movie_id"].transform("size")
    is_test = rank < (size * test_frac).round()
    return ratings[~is_test], ratings[is_test]

def make_popularity(train):
    ranked = score_movies(train)["movie_id"].tolist()
    return lambda user_id, seen: [m for m in ranked if m not in seen]

def precision_recall_at_k(recommend_fn, train, test, k=10, threshold=4.0):
    precisions, recalls = [], []
    for user_id, user_test in test.groupby("user_id"):
        relevant = set(user_test[user_test.rating >= threshold].movie_id)
        if not relevant:
            continue
        seen = set(train[train.user_id == user_id].movie_id)
        recs = recommend_fn(user_id, seen)[:k]

        hits = len(set(recs) & relevant)
        precisions.append(hits / k)
        recalls.append(hits / len(relevant))

    return sum(precisions) / len(precisions), sum(recalls) / len(recalls)

if __name__ == "__main__":
    train, test = split(load_ratings())
    print("train:", len(train), "test:", len(test))
    p, r = precision_recall_at_k(make_popularity(train), train, test)
    print(f"Popularity  P@10={p:.4f}  R@10={r:.4f}")
