from typing import Optional
from fastapi import FastAPI
from recommender import Recommender


rec = Recommender("data/anime_similarity_2020_cleaned.csv.gz")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/wake", status_code=200)
def wake_api():
    """
    endpoint for waking up the API when deployed on heroku

    a CRON job from https://cron-job.org/en/ pings the api every 15 minutes
    so it stays up 24/7

    probably a better way to do this though!

    """
    return {"api alive"}


@app.get("/recommend/{anime_name}")
def recommend(anime_name):
    """
    endpoint for returning recommendations

    anime is attached as part of path

    returns an object with an array of the top 5 recommended anime
    """
    recommended_anime = rec.recommend(anime_name)
    return{"anime": recommended_anime}
