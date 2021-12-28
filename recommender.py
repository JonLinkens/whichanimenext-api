import pandas as pd


class Recommender:

    def __init__(self, filepath):
        self.filepath = filepath
        self.ratings = pd.read_csv(filepath)
        self.ratings = self.ratings.set_index('Name')

    def __str__(self):
        return f"Recommender based on the dataset found at {self.filepath}\n"

    def recommend(self, anime_name):
        try:
            # num = 1
            recs = []
            for anime in self.ratings.sort_values(by=anime_name, ascending=False).index[1:6]:
                recs.append({"name": anime, "match": round(
                    self.ratings[anime][anime_name]*100, 2)})
            return recs
        except KeyError:
            return -1
