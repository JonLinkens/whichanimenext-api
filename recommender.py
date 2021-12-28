import pandas as pd


class Recommender:

    def __init__(self, recpath, namepath):
        self.recpath = recpath
        self.ratings = pd.read_csv(recpath)
        self.ratings = self.ratings.set_index('Name')
        self.names = pd.read_csv(namepath, index_col=[0])

    def __str__(self):
        return f"Recommender based on the dataset found at {self.recpath}\n"

    def recommend(self, anime_name):
        try:
            recs = []
            for anime in self.ratings.sort_values(by=anime_name, ascending=False).index[1:6]:
                id = int(self.names.loc[self.names['Name']
                                        == anime].iloc[0]['MAL_ID'])
                recs.append({"id": id, "name": anime, "match": round(
                    self.ratings[anime][anime_name]*100, 2)})
            return recs
        except KeyError:
            return -1
