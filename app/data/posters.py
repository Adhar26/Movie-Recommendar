import os
import json
import time
import threading
import urllib.request
import pandas as pd

CACHE = "cache/posters"
os.makedirs(CACHE, exist_ok=True)
_lock = threading.Lock()

_links = pd.read_csv("data/ml-latest-small/links.csv").dropna(subset=["tmdbId"])
_tmdb = dict(zip(_links.movieId, _links.tmdbId.astype(int)))


def _key():
    with open("tmdb_key.txt") as f:
        return f.read().strip()


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "hybrid-recommender"})
    return urllib.request.urlopen(req, timeout=10).read()


def _movie_url(movie_id):
    tmdb_id = _tmdb.get(movie_id)
    if tmdb_id is None:
        return None
    meta = json.loads(_get(f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={_key()}"))
    p = meta.get("poster_path")
    return f"https://image.tmdb.org/t/p/w185{p}" if p else None


def _anime_url(anime_id):
    time.sleep(0.4)  # Jikan allows about 3 requests per second
    meta = json.loads(_get(f"https://api.jikan.moe/v4/anime/{anime_id}"))
    return meta["data"]["images"]["jpg"]["image_url"]


def get_poster(item_id, dataset="movies"):
    """Return a local poster path (downloaded once, then cached), or None."""
    path = os.path.join(CACHE, f"{dataset}_{item_id}.jpg")
    if os.path.exists(path):
        return path
    try:
        with _lock:
            url = _anime_url(item_id) if dataset == "anime" else _movie_url(item_id)
            if not url:
                return None
            with open(path, "wb") as f:
                f.write(_get(url))
        return path
    except Exception:
        return None