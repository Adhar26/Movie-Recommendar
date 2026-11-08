from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.core.service import RecommenderService
from app.data.posters import get_poster

app = FastAPI(title="Recommender API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
svc = RecommenderService()


class RateIn(BaseModel):
    user_id: int
    movie_id: int
    rating: float


@app.get("/recommendations/{user_id}")
def recommendations(user_id: int, n: int = 20):
    return svc.get_recommendations(user_id, n)


@app.get("/search")
def search(q: str):
    return svc.search_movies(q, 20)


@app.post("/rate")
def rate(r: RateIn):
    svc.rate_movie(r.user_id, r.movie_id, r.rating)
    return {"ok": True}


@app.post("/retrain")
def retrain(bg: BackgroundTasks):
    bg.add_task(svc.refresh)
    return {"status": "retraining"}


@app.get("/poster/{movie_id}")
def poster(movie_id: int):
    path = get_poster(movie_id)
    if not path:
        raise HTTPException(status_code=404)
    return FileResponse(path)
