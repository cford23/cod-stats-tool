import pandas as pd
import numpy as np

class Schema:

    def __init__(self):
        self.matches = pd.read_csv("data/matches.csv")
        self.maps = pd.read_csv("data/maps.csv")

    def getTeamMatches(self, team):
        return self.matches[(self.matches['Team 1'] == team) | (self.matches['Team 2'] == team)]