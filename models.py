import pandas as pd
import numpy as np

class CoDStats:

    def __init__(self):
        self.matches = pd.read_csv("data/matches.csv")
        self.maps = pd.read_csv("data/maps.csv")
        self.players = pd.read_csv("data/players.csv")
        self.modes = self.maps['Game Mode'].unique()
        self.modeMaps = [0, 0, 0]
        self.modeMaps[0] = self.maps[self.maps['Game Mode'] == self.modes[0]]['Map'].unique()
        self.modeMaps[0].sort()
        self.modeMaps[1] = self.maps[self.maps['Game Mode'] == self.modes[1]]['Map'].unique()
        self.modeMaps[1].sort()
        self.modeMaps[2] = self.maps[self.maps['Game Mode'] == self.modes[2]]['Map'].unique()
        self.modeMaps[2].sort()
        self.playerList = self.players['Player'].unique()
        self.playerList.sort()
        self.teams = pd.unique(self.matches[['Team 1', 'Team 2']].values.ravel())
        self.teams.sort()
        self.events = self.matches['Event'].unique()

    ############### MATCH FUNCTIONS ###############
    def getTeamMatches(self, team):
        return self.matches[(self.matches['Team 1'] == team) | (self.matches['Team 2'] == team)]

    def getTeamOppMatches(self, team, opponent):
        return self.matches[((self.matches['Team 1'] == team) & (self.matches['Team 2'] == opponent)) |
                            ((self.matches['Team 2'] == team) & (self.matches['Team 1'] == opponent))]

    def getOverallRecord(self, team):
        wins = self.matches['Winner'].value_counts()[team]
        losses = self.matches['Team 1'].value_counts()[team] + self.matches['Team 2'].value_counts()[team] - wins
        return wins, losses

    def getMapRecord(self, team):
        wins = self.maps['Map Winner'].value_counts()[team]
        losses = self.maps['Team 1'].value_counts()[team] + self.maps['Team 2'].value_counts()[team] - wins
        return wins, losses

    def getModeRecord(self, team, mode):
        wins = self.maps[self.maps['Game Mode'] == mode]['Map Winner'].value_counts()[team]
        losses = self.maps[self.maps['Game Mode'] == mode]['Team 1'].value_counts()[team] + self.maps[self.maps['Game Mode'] == mode]['Team 2'].value_counts()[team] - wins
        return wins, losses

    def getAllMatches(self):
        return self.matches

    def getTeamWins(self, team):
        return self.matches[self.matches['Winner'] == team]

    ############### MAP FUNCTIONS ###############
    def getAllMaps(self):
        return self.maps

    def getTeamMaps(self, team):
        return self.maps[(self.maps['Team 1'] == team) | (self.maps['Team 2'] == team)]

    def getTeamModeMaps(self, team, mode):
        return self.maps[((self.maps['Team 1'] == team) & (self.maps['Game Mode'] == mode)) |
                         ((self.maps['Team 2'] == team) & (self.maps['Game Mode'] == mode))]

    def getModeMapRecord(self, team, mode, map):
        # Returns win-loss record for given team, mode, and map

    ############### PLAYER FUNCTIONS ###############
    def getPlayerKD(self, player):
        stats = self.players[self.players['Player'] == player]
        kills = stats['Kills'].sum()
        deaths = stats['Deaths'].sum()
        kd = round(kills / deaths, 2)
        return kills, deaths, kd

    def getAllPlayers(self):
        results = self.players['Player'].unique()
        results.sort()
        return results

    ############### MATCHUP PREVIEW ###############
    def getMatchupPreview(self, team1, team2):
        # TODO
        return

    ############### MAP PREVIEW ###############
    def getMapPreview(self, team1, team2, maps):
        # TODO
        return


class Team:

    def __init__(self, name="Team"):
        stats = CoDStats()
        self.name = name
        self.modeWins = [0, 0, 0]
        self.modeLosses = [0, 0, 0]
        if self.name != "Team":
            self.wins, self.losses = stats.getOverallRecord(name)
            self.mapWins, self.mapLosses = stats.getMapRecord(name)
            for k in range(3):
                self.modeWins[k], self.modeLosses[k] = stats.getModeRecord(name, stats.modes[k])
        else:
            self.wins = 0
            self.losses = 0
            self.mapWins = 0
            self.mapLosses = 0

# Same kind of class except for Player?