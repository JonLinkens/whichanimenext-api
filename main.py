from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from recommender import Recommender
import pandas as pd

# putting titles into array for use later
anime_names = pd.read_csv(
    "data/anime_similarity_2020_cleaned.csv.gz").columns.values.tolist()

# initiatlising Recommender class
rec = Recommender("data/anime_similarity_2020_cleaned.csv.gz",
                  "data/anime_info.csv.gz")

# initialise API object
app = FastAPI()


# bypassing CORS stuff - this probably needs adjusting for safety
# but for now all origins are allowed
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
    returns object with 5 recommendations based on query param

    anime is attached as part of path

    returns an object with an array of the top 5 recommended anime

    raises a 404 error if the anime isn't found
    """
    recommended_anime = rec.recommend(anime_name)
    # if recommended_anime == -1:
    #     raise HTTPException(status_code=404, detail="Anime not found")
    return{"anime": recommended_anime}
    return{"test": anime_name}


@app.get("/get/anime")
def list_all_anime():
    """
    returns an array of anime name objects structured as:
    {   
        "value": <anime_name>,
        "label": <anime_name>
    }

    to allow for react-select entries
    """
    anime_labels = []
    for name in anime_names:
        anime_labels.append({"value": name, "label": name})
    return{"names": anime_labels}
