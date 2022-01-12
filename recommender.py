import pandas as pd


class Recommender:

    def __init__(self, recpath, infopath):
        """
        Class constructor: reading in datasets and assigning to variables

        Args:
            recpath (string): relative path for recommendation dataset
            namepath (string): relative path for name dataset
        """
        self.recpath = recpath
        self.ratings = pd.read_csv(recpath)
        self.ratings = self.ratings.set_index('Name')
        self.animeinfo = pd.read_csv(infopath)

    def __str__(self):
        """
        Temporary string representation - nothing more needed as of now

        Returns:
            string: the path of the dataset it is using
        """
        return f"Recommender based on the dataset found at {self.recpath}\n"

    def recommend(self, anime_name):
        """
        Main recommendation function

        Args:
            anime_name (string): name of anime to build recommendations 

        Returns:
            [type]: array of 5 anime with highest match percentange value
            [integer]: -1 if KeyError (anime isn't found in dataset)
        """
        try:
            recs = []
            for anime in self.ratings.sort_values(by=anime_name, ascending=False).index[1:6]:
                # get the relevant details from the anime_info dataset
                mal_id = int(self.animeinfo.loc[self.animeinfo['Name']
                                                == anime].iloc[0]['MAL_ID'])
                url = self.animeinfo.loc[self.animeinfo['Name']
                                         == anime].iloc[0]['URL']
                image_url = self.animeinfo.loc[self.animeinfo['Name']
                                               == anime].iloc[0]['Image URL']
                aired_from = self.animeinfo.loc[self.animeinfo['Name']
                                                == anime].iloc[0]['Aired From']
                aired_to = self.animeinfo.loc[self.animeinfo['Name']
                                              == anime].iloc[0]['Aired To']
                synopsis = self.animeinfo.loc[self.animeinfo['Name']
                                              == anime].iloc[0]['Synopsis']

                recs.append({
                    "id": mal_id,
                    "url": url,
                    "name": anime,
                    "image_url": image_url,
                    "aired_from": aired_from,
                    "aired_to": aired_to,
                    "synopsis": synopsis,
                    "match": round(self.ratings[anime][anime_name]*100, 2)})

            return recs
        except KeyError:
            return -1
