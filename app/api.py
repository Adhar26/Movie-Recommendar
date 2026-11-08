import threading
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.core.service import RecommenderService
from app.data.posters import get_poster

app = FastAPI(title="Recommender API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DBS = {"movies": "sqlite:///recommender.db", "anime": "sqlite:///recommender_anime.db"}
_svcs = {}
_locks = {k: threading.Lock() for k in DBS}


def get_svc(dataset):
    if dataset not in DBS:
        raise HTTPException(status_code=400, detail="unknown dataset")
    with _locks[dataset]:
        if dataset not in _svcs:
            _svcs[dataset] = RecommenderService(DBS[dataset])   # anime trains on first use
        return _svcs[dataset]


get_svc("movies")


class RateIn(BaseModel):
    user_id: int
    movie_id: int
    rating: float
    dataset: str = "movies"


@app.get("/recommendations/{user_id}")
def recommendations(user_id: int, n: int = 20, dataset: str = "movies"):
    return get_svc(dataset).get_recommendations(user_id, n)


@app.get("/search")
def search(q: str, dataset: str = "movies"):
    return get_svc(dataset).search_movies(q, 20)


@app.post("/rate")
def rate(r: RateIn):
    get_svc(r.dataset).rate_movie(r.user_id, r.movie_id, r.rating)
    return {"ok": True}


@app.post("/retrain")
def retrain(bg: BackgroundTasks, dataset: str = "movies"):
    bg.add_task(get_svc(dataset).refresh)
    return {"status": "retraining"}


@app.get("/poster/{item_id}")
def poster(item_id: int, dataset: str = "movies"):
    path = get_poster(item_id, dataset)
    if not path:
        raise HTTPException(status_code=404)
    return FileResponse(path)