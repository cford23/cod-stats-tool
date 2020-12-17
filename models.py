import pandas as pd
import numpy as np

class CoDStats:

    def __init__(self):
        self.matches = pd.read_csv("data/matches.csv")
        self.maps = pd.read_csv("data/maps.csv")

    def getTeamMatches(self, team):
        return self.matches[(self.matches['Team 1'] == team) | (self.matches['Team 2'] == team)]

    def getTeamOppMatches(self, team, opponent):
        return self.matches[((self.matches['Team 1'] == team) & (self.matches['Team 2'] == opponent)) |
                            ((self.matches['Team 2'] == team) & (self.matches['Team 1'] == opponent))]

    def getAllMatches(self):
        return self.matches

    def getTeamWins(self, team):
        return self.matches[self.matches['Winner'] == team]