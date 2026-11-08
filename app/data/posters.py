import os
import json
import urllib.request
import pandas as pd

CACHE = "cache/posters"
os.makedirs(CACHE, exist_ok=True)

_links = pd.read_csv("data/ml-latest-small/links.csv").dropna(subset=["tmdbId"])
_tmdb = dict(zip(_links.movieId, _links.tmdbId.astype(int)))


def _key():
    with open("tmdb_key.txt") as f:
        return f.read().strip()


def get_poster(movie_id):
    """Return a local poster path (downloads once, then cached), or None."""
    path = os.path.join(CACHE, f"{movie_id}.jpg")
    if os.path.exists(path):
        return path
    tmdb_id = _tmdb.get(movie_id)
    if tmdb_id is None:
        return None
    try:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={_key()}"
        with urllib.request.urlopen(url, timeout=10) as r:
            poster = json.load(r).get("poster_path")
        if not poster:
            return None
        with urllib.request.urlopen(f"https://image.tmdb.org/t/p/w185{poster}", timeout=10) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
        return path
    except Exception:
        return None
