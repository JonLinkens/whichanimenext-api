from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from recommender import Recommender
import pandas as pd

anime_names = pd.read_csv(
    "data/anime_similarity_2020_cleaned.csv.gz").columns.values.tolist()
rec = Recommender("data/anime_similarity_2020_cleaned.csv.gz",
                  "data/anime_names.csv.gz")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    raises a 404 error if the anime isn't found
    """
    recommended_anime = rec.recommend(anime_name)
    if recommended_anime == -1:
        raise HTTPException(status_code=404, detail="Anime not found")
    return{"anime": recommended_anime}


@app.get("/get/anime")
def list_all_anime():
    anime_labels = []
    for name in anime_names:
        anime_labels.append({"value": name, "label": name})
    return{"names": anime_labels}
