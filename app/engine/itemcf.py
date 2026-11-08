import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

def make_itemcf(train, min_ratings=5):
    counts = train.groupby("movie_id").size()
    df = train[train.movie_id.isin(counts[counts >= min_ratings].index)].copy()

    # center each rating by the user's mean so "above average" = positive signal
    df["centered"] = df["rating"] - df.groupby("user_id")["rating"].transform("mean")

    users = df["user_id"].unique()
    items = df["movie_id"].unique()
    uidx = {u: i for i, u in enumerate(users)}
    iidx = {m: i for i, m in enumerate(items)}

    M = csr_matrix(
        (df["centered"], (df["user_id"].map(uidx), df["movie_id"].map(iidx))),
        shape=(len(users), len(items)),
    )
    S = cosine_similarity(M.T.tocsr()).astype(np.float32)   # item x item similarity
    np.fill_diagonal(S, 0)

    def recommend(user_id, seen):
        if user_id not in uidx:
            return []
        scores = np.asarray(M[uidx[user_id]] @ S).ravel()
        order = scores.argsort()[::-1]
        return [items[i] for i in order if items[i] not in seen]

    return recommend
