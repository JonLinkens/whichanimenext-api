from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# endpoint for waking up the API when deployed on heroku
# a CRON job from https://cron-job.org/en/ pings the api every 15 minutes
# so it stays up 24/7
# probably a better way to do this though!
@app.get("/wake", status_code=200)
def wake_api():
    return {"api alive"}
