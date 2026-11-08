import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine

engine = create_engine("sqlite:///recommender.db")

def make_content(train):
    movies = pd.read_sql("SELECT id, title, genres FROM movies", engine)
    movies["genres"] = movies["genres"].fillna("").str.replace("(no genres listed)", "", regex=False)

    tfidf = TfidfVectorizer(tokenizer=lambda s: s.split("|"), token_pattern=None, lowercase=False)
    X = tfidf.fit_transform(movies["genres"])          # movie x genre matrix
    ids = movies["id"].tolist()
    idx = {mid: i for i, mid in enumerate(ids)}
    liked_by_user = train[train.rating >= 4.0].groupby("user_id")["movie_id"].apply(list)

    def recommend(user_id, seen):
        liked = [idx[m] for m in liked_by_user.get(user_id, []) if m in idx]
        if not liked:
            return []
        profile = np.asarray(X[liked].mean(axis=0))    # user taste = average of liked movies
        sims = cosine_similarity(profile, X).ravel()
        order = sims.argsort()[::-1]
        return [ids[i] for i in order if ids[i] not in seen]

    return recommend
