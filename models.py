import pandas as pd

class Schema():

    def __init__(self):
        self.matches = pd.read_csv("data/matches.csv")
        self.maps = pd.read_csv("data/maps.csv")

    def getMatch(self, matchID):
        # result = self.matches.loc[self.matches['Match ID'] == matchID]
        result = self.matches.iloc[0]
        return result