import pandas as pd
import numpy as np

class CoDStats:

    def __init__(self):
        # self.matches = pd.read_csv("data/matches.csv").set_index('Match ID')
        self.matches = pd.read_csv("data/matches.csv")
        # self.maps = pd.read_csv("data/maps.csv").set_index(['Match ID', 'Map ID'])
        self.maps = pd.read_csv("data/maps.csv")
        # self.players = pd.read_csv("data/players.csv").set_index(['Match ID', 'Map ID'])
        self.players = pd.read_csv("data/players.csv")
        self.players['K/D'] = self.players['K/D'].round(2)
        self.modes = self.maps['Mode'].unique()
        self.modeMaps = [0, 0, 0]
        self.modeMaps[0] = self.maps[self.maps['Mode'] == self.modes[0]]['Map'].unique()
        self.modeMaps[0].sort()
        self.modeMaps[1] = self.maps[self.maps['Mode'] == self.modes[1]]['Map'].unique()
        self.modeMaps[1].sort()
        self.modeMaps[2] = self.maps[self.maps['Mode'] == self.modes[2]]['Map'].unique()
        self.modeMaps[2].sort()
        self.allMaps = self.maps['Map'].unique()
        self.allMaps.sort()
        self.playerList = list(self.players['Player'].unique())
        self.playerList.sort(key=lambda x: x.lower())
        self.teams = pd.unique(self.matches[['Team 1', 'Team 2']].values.ravel())
        self.teams.sort()
        self.events = self.matches['Event'].unique()
        self.teamAbbrs = {
            'Atlanta FaZe': 'ATL',
            'Dallas Empire': 'DAL',
            'Florida Mutineers': 'FLA',
            'London Royal Ravens': 'LDN',
            'Los Angeles Guerrillas': 'LAG',
            'Los Angeles Thieves': 'LAT',
            'Minnesota ROKKR': 'MIN',
            'New York Subliners': 'NY',
            'OpTic Chicago': 'CHI',
            'Paris Legion': 'PAR',
            'Seattle Surge': 'SEA',
            'Toronto Ultra': 'TOR',
        }

    def getMatchData(self, matchID=None, team=None, opponent=None, event=None):
        if matchID is not None:
            data = self.matches[self.matches['Match ID'] == matchID]
        else:
            data = self.matches
        return pd.DataFrame(data)

    def getMapData(self, matchID=None, mapID=None, team=None, opponent=None, event=None, mode=None, map=None):
        if matchID is not None:
            data = self.maps[self.maps['Match ID'] == matchID]
        else:
            data = self.maps
        return pd.DataFrame(data)

    def getPlayerData(self, matchID=None, mapID=None):
        if matchID is not None:
            data = self.players[self.players['Match ID'] == matchID]
        else:
            data = self.players
        return pd.DataFrame(data)

    def getMatchRecord(self, team, opponent, event):
        wins = 0
        losses = 0
        if opponent != 'All' and event != 'All':
            # specific opponent and specific event
            data = self.matches[((self.matches['Team 1'] == team) & (self.matches['Team 2'] == opponent) & (self.matches['Event'] == event)) |
                                ((self.matches['Team 2'] == team) & (self.matches['Team 1'] == opponent) & (self.matches['Event'] == event))]
        if opponent != 'All' and event == 'All':
            # specific opponent and all events
            data = self.matches[((self.matches['Team 1'] == team) & (self.matches['Team 2'] == opponent)) |
                                ((self.matches['Team 2'] == team) & (self.matches['Team 1'] == opponent))]
        if opponent == 'All' and event != 'All':
            # all opponents and specific event
            data = self.matches[((self.matches['Team 1'] == team) & (self.matches['Event'] == event)) |
                                ((self.matches['Team 2'] == team) & (self.matches['Event'] == event))]
        if opponent == 'All' and event == 'All':
            # all opponents and all events
            data = self.matches[(self.matches['Team 1'] == team) | (self.matches['Team 2'] == team)]

        if data.shape[0] > 0:
            wins = data[data['Winner'] == team].shape[0]
            matchData = data[(data['Team 1'] == team) | (data['Team 2'] == team)]
            losses = matchData.shape[0] - wins
            return wins, losses
        else:
            return wins, losses  # both are 0

    def getMapRecord(self, team, opponent, event, mode, map):
        wins = 0
        losses = 0
        # team, opponent, event, mode, map
        if opponent != "All" and event != "All" and mode != "All" and map != "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
        # team, opponent, event, mode
        if opponent != "All" and event != "All" and mode != "All" and map == "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode))]
        # team, opponent, event, map
        if opponent != "All" and event != "All" and mode == "All" and map != "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Event'] == event) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Event'] == event) & (self.maps['Map'] == map))]
        # team, opponent, mode, map
        if opponent != "All" and event == "All" and mode != "All" and map != "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
        # team, event, mode, map
        if opponent == "All" and event != "All" and mode != "All" and map != "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
        # team, opponent, event
        if opponent != "All" and event != "All" and mode == "All" and map == "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Event'] == event)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Event'] == event))]
        # team, opponent, mode
        if opponent != "All" and event == "All" and mode != "All" and map == "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Mode'] == mode)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Mode'] == mode))]
        # team, opponent, map
        if opponent != "All" and event == "All" and mode == "All" and map != "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Map'] == map))]
        # team, mode, map
        if opponent == "All" and event == "All" and mode != "All" and map != "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
        # team, opponent
        if opponent != "All" and event == "All" and mode == "All" and map == "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent))]
        # team, event
        if opponent == "All" and event != "All" and mode == "All" and map == "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Event'] == event)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Event'] == event))]
        # team, mode
        if opponent == "All" and event == "All" and mode != "All" and map == "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Mode'] == mode)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Mode'] == mode))]
        # team, map
        if opponent == "All" and event == "All" and mode == "All" and map != "All":
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Map'] == map))]
        # team
        if opponent == "All" and event == "All" and mode == "All" and map == "All":
            data = self.maps[(self.maps['Team 1'] == team) | (self.maps['Team 2'] == team)]

        if data.shape[0] > 0:
            wins = data[data['Map Winner'] == team].shape[0]
            losses = data.shape[0] - wins
            return wins, losses
        else:
            return wins, losses  # both are 0

    def getPlayerRecord(self, name, event):
        player = Player(name)
        matches = player.getPlayerMatchIDs()
        wins = 0
        losses = 0
        if len(matches) > 0:
            for key, value in matches.items():
                match = self.findMatch(key)
                if event == 'All' or match['Event'] == event:
                    if match['Winner'] == value:
                        wins += 1
                    else:
                        losses += 1
        return wins, losses

    def getPlayerMapRecord(self, name, event):
        player = Player(name)
        maps = player.getPlayerMapIDs()
        wins = 0
        losses = 0
        if len(maps) > 0:
            for key, value in maps.items():
                map = self.findMap(key[0], key[1])
                if event == 'All' or map['Event'] == event:
                    if map['Map Winner'] == value:
                        wins += 1
                    else:
                        losses += 1
        return wins, losses

    def getTeamModeRecord(self, team, event, mode):
        if event == 'All':
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Mode'] == mode)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Mode'] == mode))]
        else:
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode))]
        wins = data[data['Map Winner'] == team].shape[0]
        losses = data.shape[0] - wins
        return wins, losses

    def getAllPlayers(self):
        results = self.players['Player'].unique()
        results.sort()
        return results

    ############### GET MATCHES ###############
    def getMatches(self, team, opponent, event):
        # team, opponent, and event
        if team != "All" and opponent != "All" and event != "All":
            return self.matches[((self.matches['Team 1'] == team) & (self.matches['Team 2'] == opponent) & (self.matches['Event'] == event)) |
                                ((self.matches['Team 2'] == team) & (self.matches['Team 1'] == opponent) & (self.matches['Event'] == event))]
        # team and opponent
        if team != "All" and opponent != "All" and event == "All":
            return self.matches[((self.matches['Team 1'] == team) & (self.matches['Team 2'] == opponent)) |
                                ((self.matches['Team 2'] == team) & (self.matches['Team 1'] == opponent))]
        # team and event
        if team != "All" and opponent == "All" and event != "All":
            return self.matches[((self.matches['Team 1'] == team) & (self.matches['Event'] == event) |
                                (self.matches['Team 2'] == team) & (self.matches['Event'] == event))]
        # team
        if team != "All" and opponent == "All" and event == "All":
            return self.matches[(self.matches['Team 1'] == team) | (self.matches['Team 2'] == team)]
        # event
        if team == "All" and opponent == "All" and event != "All":
            return self.matches[self.matches['Event'] == event]
        # opponent (error)
        if team == "All" and opponent != "All":
            return self.matches
        # none
        if team == "All" and opponent == "All" and event == "All":
            return self.matches

    def getViewMatchRecord(self, team, data):
        wins = data[data['Winner'] == team].shape[0]
        losses = data.shape[0] - wins
        return wins, losses

    ############### GET MAPS ###############
    def getMaps(self, team, opponent, event, mode, map):
        # team, opponent, event, mode, map
        if team != "All" and opponent != "All" and event != "All" and mode != "All" and map != "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
        # team, opponent, event, mode
        if team != "All" and opponent != "All" and event != "All" and mode != "All" and map == "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode))]
        # team, opponent, event, map
        if team != "All" and opponent != "All" and event != "All" and mode == "All" and map != "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Event'] == event) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Event'] == event) & (self.maps['Map'] == map))]
        # team, opponent, mode, map
        if team != "All" and opponent != "All" and event == "All" and mode != "All" and map != "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
        # team, event, mode, map
        if team != "All" and opponent == "All" and event != "All" and mode != "All" and map != "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
        # team, opponent, event
        if team != "All" and opponent != "All" and event != "All" and mode == "All" and map == "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Event'] == event)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Event'] == event))]
        # team, opponent, mode
        if team != "All" and opponent != "All" and event == "All" and mode != "All" and map == "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Mode'] == mode)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Mode'] == mode))]
        # team, opponent, map
        if team != "All" and opponent != "All" and event == "All" and mode == "All" and map != "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent) & (self.maps['Map'] == map))]
        # team, event, mode
        if team != 'All' and opponent == 'All' and event != 'All' and mode != 'All' and map == 'All':
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode))]
        # team, event, map
        if team != 'All' and opponent == 'All' and event != 'All' and mode == 'All' and map != 'All':
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Event'] == event) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Event'] == event) & (self.maps['Map'] == map))]
        # team, mode, map
        if team != "All" and opponent == "All" and event == "All" and mode != "All" and map != "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
        # event, mode, map
        if team == "All" and opponent == "All" and event != "All" and mode != "All" and map != "All":
            return self.maps[(self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)]
        # team, opponent
        if team != "All" and opponent != "All" and event == "All" and mode == "All" and map == "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Team 2'] == opponent)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Team 1'] == opponent))]
        # team, event
        if team != "All" and opponent == "All" and event != "All" and mode == "All" and map == "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Event'] == event)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Event'] == event))]
        # team, mode
        if team != "All" and opponent == "All" and event == "All" and mode != "All" and map == "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Mode'] == mode)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Mode'] == mode))]
        # team, map
        if team != "All" and opponent == "All" and event == "All" and mode == "All" and map != "All":
            return self.maps[((self.maps['Team 1'] == team) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Map'] == map))]
        # event, mode
        if team == "All" and opponent == "All" and event != "All" and mode != "All" and map == "All":
            return self.maps[(self.maps['Event'] == event) & (self.maps['Mode'] == mode)]
        # event, map
        if team == "All" and opponent == "All" and event != "All" and mode == "All" and map != "All":
            return self.maps[(self.maps['Event'] == event) & (self.maps['Map'] == map)]
        # mode, map
        if team == "All" and opponent == "All" and event == "All" and mode != "All" and map != "All":
            return self.maps[(self.maps['Mode'] == mode) & (self.maps['Map'] == map)]
        # team
        if team != "All" and opponent == "All" and event == "All" and mode == "All" and map == "All":
            return self.maps[(self.maps['Team 1'] == team) | (self.maps['Team 2'] == team)]
        # event
        if team == "All" and opponent == "All" and event != "All" and mode == "All" and map == "All":
            return self.maps[self.maps['Event'] == event]
        # mode
        if team == "All" and opponent == "All" and event == "All" and mode != "All" and map == "All":
            return self.maps[self.maps['Mode'] == mode]
        # map
        if team == "All" and opponent == "All" and event == "All" and mode == "All" and map != "All":
            return self.maps[self.maps['Map'] == map]
        # opponent (error)
        if team == "All" and opponent != "All":
            return self.maps
        # none
        if team == "All" and opponent == "All" and event == "All" and mode == "All" and map == "All":
            return self.maps

    def getViewMapRecord(self, team, data):
        wins = data[data['Map Winner'] == team].shape[0]
        losses = data.shape[0] - wins
        return wins, losses

    ############### GET PLAYERS ###############
    def getPlayers(self, player, team, opponent, event, mode, map):
        # team, opponent, event, mode, map
        if team != 'All' and opponent != 'All' and event != 'All' and mode != 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Opponent'] == opponent) & (self.players['Event'] == event) &
                                (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team, opponent, event, mode
        if team != 'All' and opponent != 'All' and event != 'All' and mode != 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Opponent'] == opponent) & (self.players['Event'] == event) &
                                (self.players['Mode'] == mode)]
        # team, opponent, event, map
        if team != 'All' and opponent != 'All' and event != 'All' and mode == 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Opponent'] == opponent) & (self.players['Event'] == event) &
                                (self.players['Map'] == map)]
        # team, opponent, mode, map
        if team != 'All' and opponent != 'All' and event == 'All' and mode != 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Opponent'] == opponent) & (self.players['Mode'] == mode) &
                                (self.players['Map'] == map)]
        # team, event, mode, map
        if team != 'All' and opponent == 'All' and event != 'All' and mode != 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Event'] == event) & (self.players['Mode'] == mode) &
                                (self.players['Map'] == map)]
        # opponent, event, mode, map
        if team == 'All' and opponent != 'All' and event != 'All' and mode != 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Opponent'] == opponent) &
                                (self.players['Event'] == event) & (self.players['Mode'] == mode) &
                                (self.players['Map'] == map)]
        # team, opponent, event
        if team != 'All' and opponent != 'All' and event != 'All' and mode == 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Opponent'] == opponent) & (self.players['Event'] == event)]
        # team, opponent, mode
        if team != 'All' and opponent != 'All' and event == 'All' and mode != 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Opponent'] == opponent) & (self.players['Mode'] == mode)]
        # team, opponent, map
        if team != 'All' and opponent != 'All' and event == 'All' and mode == 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Opponent'] == opponent) & (self.players['Map'] == map)]
        # team, event, mode
        if team != 'All' and opponent == 'All' and event != 'All' and mode != 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # team, event, map
        if team != 'All' and opponent == 'All' and event != 'All' and mode == 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Event'] == event) & (self.players['Map'] == map)]
        # team, mode, map
        if team != 'All' and opponent == 'All' and event == 'All' and mode != 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # opponent, event, mode
        if team == 'All' and opponent != 'All' and event != 'All' and mode != 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Opponent'] == opponent) &
                                (self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # opponent, event, map
        if team == 'All' and opponent != 'All' and event != 'All' and mode == 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Opponent'] == opponent) &
                                (self.players['Event'] == event) & (self.players['Map'] == map)]
        # opponent, mode, map
        if team == 'All' and opponent != 'All' and event == 'All' and mode != 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Opponent'] == opponent) &
                                (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # event, mode, map
        if team == 'All' and opponent == 'All' and event != 'All' and mode != 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Event'] == event) &
                                (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team, opponent
        if team != 'All' and opponent != 'All' and event == 'All' and mode == 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Opponent'] == opponent)]
        # team, event
        if team != 'All' and opponent == 'All' and event != 'All' and mode == 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Event'] == event)]
        # team, mode
        if team != 'All' and opponent == 'All' and event == 'All' and mode != 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Mode'] == mode)]
        # team, map
        if team != 'All' and opponent == 'All' and event == 'All' and mode == 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team) &
                                (self.players['Map'] == map)]
        # opponent, event
        if team == 'All' and opponent != 'All' and event != 'All' and mode == 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Opponent'] == opponent) &
                                (self.players['Event'] == event)]
        # opponent, mode
        if team == 'All' and opponent != 'All' and event == 'All' and mode != 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Opponent'] == opponent) &
                                (self.players['Mode'] == mode)]
        # opponent, map
        if team == 'All' and opponent != 'All' and event == 'All' and mode == 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Opponent'] == opponent) &
                                (self.players['Map'] == map)]
        # event, mode
        if team == 'All' and opponent == 'All' and event != 'All' and mode != 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Event'] == event) &
                                (self.players['Mode'] == mode)]
        # event, map
        if team == 'All' and opponent == 'All' and event != 'All' and mode == 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Event'] == event) &
                                (self.players['Map'] == map)]
        # mode, map
        if team == 'All' and opponent == 'All' and event == 'All' and mode != 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Mode'] == mode) &
                                (self.players['Map'] == map)]
        # team
        if team != 'All' and opponent == 'All' and event == 'All' and mode == 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Team'] == team)]
        # opponent
        if team == 'All' and opponent != 'All' and event == 'All' and mode == 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Opponent'] == opponent)]
        # event
        if team == 'All' and opponent == 'All' and event != 'All' and mode == 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Event'] == event)]
        # mode
        if team == 'All' and opponent == 'All' and event == 'All' and mode != 'All' and map == 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Mode'] == mode)]
        # map
        if team == 'All' and opponent == 'All' and event == 'All' and mode == 'All' and map != 'All':
            return self.players[(self.players['Player'] == player) & (self.players['Map'] == map)]
        # player
        return self.players[self.players['Player'] == player]

    ############### MATCHUP PREVIEW ###############
    def getMatchupPreview(self, team1, team2):
        output = {team1: [0, 0, 0, 0, 0], team2: [0, 0, 0, 0, 0]}
        if team1 != team2:
            matchWins = self.matches[((self.matches['Team 1'] == team1) & (self.matches['Team 2'] == team2)) |
                                     ((self.matches['Team 2'] == team1) & (self.matches['Team 1'] == team2))]
            mapWins = self.maps[((self.maps['Team 1'] == team1) & (self.maps['Team 2'] == team2)) |
                                ((self.maps['Team 2'] == team1) & (self.maps['Team 1'] == team2))]
            # head to head
            # matches
            output[team1][0] = matchWins[matchWins['Winner'] == team1].shape[0]
            output[team2][0] = matchWins[matchWins['Winner'] == team2].shape[0]

            # maps
            output[team1][1] = mapWins[mapWins['Map Winner'] == team1].shape[0]
            output[team2][1] = mapWins[mapWins['Map Winner'] == team2].shape[0]

            # modes
            for k in range(3):
                output[team1][k + 2] = mapWins[(mapWins['Map Winner'] == team1) & (mapWins['Mode'] == self.modes[k])].shape[0]
                output[team2][k + 2] = mapWins[(mapWins['Map Winner'] == team2) & (mapWins['Mode'] == self.modes[k])].shape[0]

        return output

    ############### MAP PREVIEW ###############
    def getMapPreview(self, team1, team2, maps):
        team1Records = {'wins': [0, 0, 0, 0, 0], 'losses': [0, 0, 0, 0, 0]}
        team2Records = {'wins': [0, 0, 0, 0, 0], 'losses': [0, 0, 0, 0, 0]}
        headToHead = {team1: [0, 0, 0, 0, 0], team2: [0, 0, 0, 0, 0]}

        # team 1
        count = 0
        k = 0
        for map in maps:
            team1Records['wins'][k], team1Records['losses'][k] = self.getModeMapRecord(team1, "All", self.modes[count],
                                                                                       map)
            count = (count + 1) % 3
            k += 1
        # team 2
        count = 0
        k = 0
        for map in maps:
            team2Records['wins'][k], team2Records['losses'][k] = self.getModeMapRecord(team2, "All", self.modes[count],
                                                                                       map)
            count = (count + 1) % 3
            k += 1
        if team1 != team2:
            # head to head
            count = 0
            k = 0
            for map in maps:
                dataSubset = self.maps[((self.maps['Team 1'] == team1) & (self.maps['Team 2'] == team2) & (self.maps['Mode'] == self.modes[count]) & (self.maps['Map'] == map)) |
                                       ((self.maps['Team 2'] == team1) & (self.maps['Team 1'] == team2) & (self.maps['Mode'] == self.modes[count]) & (self.maps['Map'] == map))]
                try:
                    headToHead[team1][k] = dataSubset['Map Winner'].value_counts()[team1]
                except KeyError:
                    pass
                try:
                    headToHead[team2][k] = dataSubset['Map Winner'].value_counts()[team2]
                except KeyError:
                    pass
                count = (count + 1) % 3
                k += 1
        return team1Records, team2Records, headToHead

    ############### MODE MAP RECORD ###############
    def getModeMapRecord(self, team, event, mode, map):
        # event, mode, map
        if event != 'All' and mode != 'All' and map != 'All':
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
        # event, mode
        if event != 'All' and mode != 'All' and map == 'All':
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode))]
        # event, map
        if event != 'All' and mode == 'All' and map != 'All':
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Event'] == event) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Event'] == event) & (self.maps['Map'] == map))]
        # mode, map
        if event == 'All' and mode != 'All' and map != 'All':
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
        # event
        if event != 'All' and mode == 'All' and map == 'All':
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Event'] == event)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Event'] == event))]
        # mode
        if event == 'All' and mode != 'All' and map == 'All':
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Mode'] == mode)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Mode'] == mode))]
        # map
        if event == 'All' and mode == 'All' and map != 'All':
            data = self.maps[((self.maps['Team 1'] == team) & (self.maps['Map'] == map)) |
                             ((self.maps['Team 2'] == team) & (self.maps['Map'] == map))]
        wins = data[data['Map Winner'] == team].shape[0]
        losses = data.shape[0] - wins

        return wins, losses

    ############### GET LEADERBOARD ###############
    def getLeaderboard(self, category, leaderboard, event):
        wins = 0
        losses = 0
        kills = 0
        deaths = 0
        kd = 0.00
        if category == 'Team':
            teamRecords = {}
            if event == 'All':
                teamList = self.teams
            else:
                teamList = self.getEventTeams(event)
            for team in teamList:
                if leaderboard == 'Overall Record':
                    wins, losses = self.getMatchRecord(team, "All", event)
                elif leaderboard == 'Map Record':
                    wins, losses = self.getMapRecord(team, "All", event, "All", "All")
                elif leaderboard == 'K/D':
                    kd, kills, deaths = self.getTeamKD(team, event, "All")
                elif leaderboard in self.modes:
                    wins, losses = self.getTeamModeRecord(team, event, leaderboard)
                if leaderboard == 'Overall Record' or leaderboard == 'Map Record' or leaderboard in self.modes:
                    try:
                        winPercent = round((wins / (wins + losses)) * 100, 2)
                    except ZeroDivisionError:
                        winPercent = 0.00
                    teamRecords[team] = [winPercent, wins, losses]
                elif leaderboard == 'K/D':
                    teamRecords[team] = [kd, kills, deaths]
            return teamRecords
        if category == 'Player':
            playerRecords = {}
            if event == 'All':
                playerList = list(self.playerList)
            else:
                playerList = list(self.getEventPlayers(event))
            for player in playerList:
                if leaderboard == 'Overall Record':
                    wins, losses = self.getPlayerRecord(player, event)
                elif leaderboard == 'Map Record':
                    wins, losses = self.getPlayerMapRecord(player, event)
                elif leaderboard == 'K/D':
                    kd, kills, deaths = self.getPlayerKD(player, event, "All")
                elif leaderboard in self.modes:
                    kd, kills, deaths = self.getPlayerKD(player, event, leaderboard)
                if leaderboard == 'Overall Record' or leaderboard == 'Map Record':
                    try:
                        winPercent = round((wins / (wins + losses)) * 100, 2)
                    except ZeroDivisionError:
                        winPercent = 0.00
                    playerRecords[player] = [winPercent, wins, losses]
                elif leaderboard == 'K/D' or leaderboard in self.modes:
                    playerRecords[player] = [kd, kills, deaths]
            return playerRecords

    def getTeamEvents(self, team):
        # returns a list of events a team was at
        event1 = list(self.matches[self.matches['Team 1'] == team]['Event'].unique())
        event2 = list(self.matches[self.matches['Team 2'] == team]['Event'].unique())
        events = event1 + list(set(event2) - set(event1))
        return events

    def getTeamKD(self, team, event, mode):
        # event, mode
        if event != 'All' and mode != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # event
        if event != 'All' and mode == 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Event'] == event)]
        # mode
        if event == 'All' and mode != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Mode'] == mode)]
        # none
        if event == 'All' and mode == 'All':
            data = self.players[self.players['Team'] == team]
        kills = data['Kills'].sum()
        deaths = data['Deaths'].sum()
        kd = round(kills / deaths, 2)
        return kd, kills, deaths

    def getEventTeams(self, event):
        teams1 = list(self.matches[self.matches['Event'] == event]['Team 1'].unique())
        teams2 = list(self.matches[self.matches['Event'] == event]['Team 2'].unique())
        teams = teams1 + list(set(teams2) - set(teams1))
        return teams

    def getPlayerKD(self, player, event, mode):
        # event, mode
        if event != 'All' and mode != 'All':
            data = self.players[(self.players['Player'] == player) & (self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # event
        elif event != 'All':
            data = self.players[(self.players['Player'] == player) & (self.players['Event'] == event)]
        # mode
        elif mode != 'All':
            data = self.players[(self.players['Player'] == player) & (self.players['Mode'] == mode)]
        # none
        else:
            data = self.players[self.players['Player'] == player]
        kills = data['Kills'].sum()
        deaths = data['Deaths'].sum()
        kd = round(kills / deaths, 2)
        return kd, kills, deaths

    def getEventPlayers(self, event):
        return self.players[self.players['Event'] == event]['Player'].unique()

    ############### GET TEAM LEADERBOARD ###############
    def getTeamLeaderboard(self, type, opponent, event, mode, map):
        if type != 'Team K/D':
            if type == 'Match Win Percent':
                # opponent, event
                if opponent != 'All' and event != 'All':
                    data = self.matches[((self.matches['Team 1'] == opponent) & (self.matches['Event'] == event)) |
                                        ((self.matches['Team 2'] == opponent) & (self.matches['Event'] == event))]
                # opponent
                elif opponent != 'All':
                    data = self.matches[(self.matches['Team 1'] == opponent) | (self.matches['Team 2'] == opponent)]
                # event
                elif event != 'All':
                    data = self.matches[self.matches['Event'] == event]
                # none
                else:
                    data = self.matches
                return self.getTeamMatchRecords(data)
            else:
                # opponent, event, mode, map
                if opponent != 'All' and event != 'All' and mode != 'All' and map != 'All':
                    data = self.maps[((self.maps['Team 1'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                                     ((self.maps['Team 2'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
                # opponent, event, mode
                elif opponent != 'All' and event != 'All' and mode != 'All':
                    data = self.maps[((self.maps['Team 1'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode)) |
                                     ((self.maps['Team 2'] == opponent) & (self.maps['Event'] == event) & (self.maps['Mode'] == mode))]
                # opponent, event, map
                elif opponent != 'All' and event != 'All' and map != 'All':
                    data = self.maps[((self.maps['Team 1'] == opponent) & (self.maps['Event'] == event) & (self.maps['Map'] == map)) |
                                     ((self.maps['Team 2'] == opponent) & (self.maps['Event'] == event) & (self.maps['Map'] == map))]
                # opponent, mode, map
                elif opponent != 'All' and mode != 'All' and map != 'All':
                    data = self.maps[((self.maps['Team 1'] == opponent) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)) |
                                     ((self.maps['Team 2'] == opponent) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map))]
                # event, mode, map
                elif event != 'All' and mode != 'All' and map != 'All':
                    data = self.maps[(self.maps['Event'] == event) & (self.maps['Mode'] == mode) & (self.maps['Map'] == map)]
                # opponent, event
                elif opponent != 'All' and event != 'All':
                    data = self.maps[((self.maps['Team 1'] == opponent) & (self.maps['Event'] == event)) |
                                     ((self.maps['Team 2'] == opponent) & (self.maps['Event'] == event))]
                # opponent, mode
                elif opponent != 'All' and mode != 'All':
                    data = self.maps[((self.maps['Team 1'] == opponent) & (self.maps['Mode'] == mode)) |
                                     ((self.maps['Team 2'] == opponent) & (self.maps['Mode'] == mode))]
                # opponent, map
                elif opponent != 'All' and map != 'All':
                    data = self.maps[((self.maps['Team 1'] == opponent) & (self.maps['Map'] == map)) |
                                     ((self.maps['Team 2'] == opponent) & (self.maps['Map'] == map))]
                # event, mode
                elif event != 'All' and mode != 'All':
                    data = self.maps[(self.maps['Event'] == event) & (self.maps['Mode'] == mode)]
                # event, map
                elif event != 'All' and map != 'All':
                    data = self.maps[(self.maps['Event'] == event) & (self.maps['Map'] == map)]
                # mode, map
                elif mode != 'All' and map != 'All':
                    data = self.maps[(self.maps['Mode'] == mode) & (self.maps['Map'] == map)]
                # opponent
                elif opponent != 'All':
                    data = self.maps[(self.maps['Team 1'] == opponent) | (self.maps['Team 2'] == opponent)]
                # event
                elif event != 'All':
                    data = self.maps[self.maps['Event'] == event]
                # mode
                elif mode != 'All':
                    data = self.maps[self.maps['Mode'] == mode]
                # map
                elif map != 'All':
                    data = self.maps[self.maps['Map'] == map]
                # none
                else:
                    data = self.maps
                return self.getTeamMapRecords(data)
        else:
            # get team k/d subset for given options
            # opponent, event, mode, map
            if opponent != 'All' and event != 'All' and mode != 'All' and map != 'All':
                data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
            # opponent, event, mode
            elif opponent != 'All' and event != 'All' and mode != 'All':
                data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (self.players['Mode'] == mode)]
            # opponent, event, map
            elif opponent != 'All' and event != 'All' and map != 'All':
                data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (self.players['Map'] == map)]
            # opponent, mode, map
            elif opponent != 'All' and mode != 'All' and map != 'All':
                data = self.players[(self.players['Opponent'] == opponent) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
            # event, mode, map
            elif event != 'All' and mode != 'All' and map != 'All':
                data = self.players[(self.players['Event'] == event) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
            # opponent, event
            elif opponent != 'All' and event != 'All':
                data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event)]
            # opponent, mode
            elif opponent != 'All' and mode != 'All':
                data = self.players[(self.players['Opponent'] == opponent) & (self.players['Mode'] == mode)]
            # opponent, map
            elif opponent != 'All' and map != 'All':
                data = self.players[(self.players['Opponent'] == opponent) & (self.players['Map'] == map)]
            # event, mode
            elif event != 'All' and mode != 'All':
                data = self.players[(self.players['Event'] == event) & (self.players['Mode'] == mode)]
            # event, map
            elif event != 'All' and map != 'All':
                data = self.players[(self.players['Event'] == event) & (self.players['Map'] == map)]
            # mode, map
            elif mode != 'All' and map != 'All':
                data = self.players[(self.players['Mode'] == mode) & (self.players['Map'] == map)]
            # opponent
            elif opponent != 'All':
                data = self.players[self.players['Opponent'] == opponent]
            # event
            elif event != 'All':
                data = self.players[self.players['Event'] == event]
            # mode
            elif mode != 'All':
                data = self.players[self.players['Mode'] == mode]
            # map
            elif map != 'All':
                data = self.players[self.players['Map'] == map]
            # none
            else:
                data = self.players
            return self.getTeamKDRecords(data)

    def getTeamMatchRecords(self, data):
        records = {}
        for team in self.teams:
            teamData = data[(data['Team 1'] == team) | (data['Team 2'] == team)]
            if teamData.shape[0] > 0:
                wins = teamData[teamData['Winner'] == team].shape[0]
                losses = teamData.shape[0] - wins
                winPercent = round(wins / (wins + losses) * 100, 2)
                records[team] = [winPercent, wins, losses]
            else:
                records[team] = [0, 0, 0]
        return records

    def getTeamMapRecords(self, data):
        records = {}
        for team in self.teams:
            teamData = data[(data['Team 1'] == team) | (data['Team 2'] == team)]
            if teamData.shape[0] > 0:
                wins = teamData[teamData['Map Winner'] == team].shape[0]
                losses = teamData.shape[0] - wins
                winPercent = round(wins / (wins + losses) * 100, 2)
                records[team] = [winPercent, wins, losses]
            else:
                records[team] = [0, 0, 0]
        return records

    def getTeamKDRecords(self, data):
        records = {}
        for team in self.teams:
            teamData = data[data['Team'] == team]
            if teamData.shape[0] > 0:
                kills = teamData['Kills'].sum()
                deaths = teamData['Deaths'].sum()
                kd = round(kills / deaths, 2)
                records[team] = [kd, kills, deaths]
            else:
                records[team] = [0, 0, 0]
        return records

    ############### GET PLAYER LEADERBOARD ###############
    def getPlayerLeaderboard(self, type, team, opponent, event, mode, map):
        # team, opponent, event, mode, map
        if team != 'All' and opponent != 'All' and event != 'All' and mode != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team, opponent, event, mode
        elif team != 'All' and opponent != 'All' and event != 'All' and mode != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # team, opponent, event, map
        elif team != 'All' and opponent != 'All' and event != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (self.players['Map'] == map)]
        # team, opponent, mode, map
        elif team != 'All' and opponent != 'All' and mode != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team, event, mode, map
        elif team != 'All' and event != 'All' and mode != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Event'] == event) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # opponent, event, mode, map
        elif opponent != 'All' and event != 'All' and mode != 'All' and map != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team, opponent, event
        elif team != 'All' and opponent != 'All' and event != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (self.players['Event'] == event)]
        # team, opponent, mode
        elif team != 'All' and opponent != 'All' and mode != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (self.players['Mode'] == mode)]
        # team, opponent, map
        elif team != 'All' and opponent != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (self.players['Map'] == map)]
        # team, event, mode
        elif team != 'All' and event != 'All' and mode != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # team, event, map
        elif team != 'All' and event != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Event'] == event) & (self.players['Map'] == map)]
        # team, mode, map
        elif team != 'All' and mode != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # opponent, event, mode
        elif opponent != 'All' and event != 'All' and mode != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # opponent, event, map
        elif opponent != 'All' and event != 'All' and map != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (self.players['Map'] == map)]
        # opponent, mode, map
        elif opponent != 'All' and event != 'All' and mode != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # event, mode, map
        elif event != 'All' and mode != 'All' and map != 'All':
            data = self.players[(self.players['Event'] == event) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team, opponent
        elif team != 'All' and opponent != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent)]
        # team, event
        elif team != 'All' and event != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Event'] == event)]
        # team, mode
        elif team != 'All' and mode != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Mode'] == mode)]
        # team, map
        elif team != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Map'] == map)]
        # opponent, event
        elif opponent != 'All' and event != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event)]
        # opponent, mode
        elif opponent != 'All' and mode != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Mode'] == mode)]
        # opponent, map
        elif opponent != 'All' and map != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Map'] == map)]
        # event, mode
        elif event != 'All' and mode != 'All':
            data = self.players[(self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # event, map
        elif event != 'All' and map != 'All':
            data = self.players[(self.players['Event'] == event) & (self.players['Map'] == map)]
        # mode, map
        elif mode != 'All' and map != 'All':
            data = self.players[(self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team
        elif team != 'All':
            data = self.players[self.players['Team'] == team]
        # opponent
        elif opponent != 'All':
            data = self.players[self.players['Opponent'] == opponent]
        # event
        elif event != 'All':
            data = self.players[self.players['Event'] == event]
        # mode
        elif mode != 'All':
            data = self.players[self.players['Mode'] == mode]
        # map
        elif map != 'All':
            data = self.players[self.players['Map'] == map]
        # none
        else:
            data = self.players
        return self.getPlayerRecords(data, type)

    def getPlayerRecords(self, data, type):
        records = {}
        for player in self.playerList:
            playerData = data[data['Player'] == player]
            if playerData.shape[0] > 0:
                # add in check if type contains 'Avg'
                if type == 'K/D':
                    kills = playerData['Kills'].sum()
                    deaths = playerData['Deaths'].sum()
                    records[player] = round(kills / deaths, 2)
                elif 'Avg' in type:
                    if not np.isnan(playerData[type].mean()):
                        records[player] = round(playerData[type].mean(), 2)
                else:
                    records[player] = playerData[type].sum()
        return records

    ############### GET RECORDS ###############
    def getRecordsRange(self, team, opponent, event, mode, map):
        # team, opponent, event, mode, map
        if team != 'All' and opponent != 'All' and event != 'All' and mode != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (
                        self.players['Event'] == event) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team, opponent, event, mode
        elif team != 'All' and opponent != 'All' and event != 'All' and mode != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (
                        self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # team, opponent, event, map
        elif team != 'All' and opponent != 'All' and event != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (
                        self.players['Event'] == event) & (self.players['Map'] == map)]
        # team, opponent, mode, map
        elif team != 'All' and opponent != 'All' and mode != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (
                        self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team, event, mode, map
        elif team != 'All' and event != 'All' and mode != 'All' and map != 'All':
            data = self.players[
                (self.players['Team'] == team) & (self.players['Event'] == event) & (self.players['Mode'] == mode) & (
                            self.players['Map'] == map)]
        # opponent, event, mode, map
        elif opponent != 'All' and event != 'All' and mode != 'All' and map != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (
                        self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team, opponent, event
        elif team != 'All' and opponent != 'All' and event != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (
                        self.players['Event'] == event)]
        # team, opponent, mode
        elif team != 'All' and opponent != 'All' and mode != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (
                        self.players['Mode'] == mode)]
        # team, opponent, map
        elif team != 'All' and opponent != 'All' and map != 'All':
            data = self.players[
                (self.players['Team'] == team) & (self.players['Opponent'] == opponent) & (self.players['Map'] == map)]
        # team, event, mode
        elif team != 'All' and event != 'All' and mode != 'All':
            data = self.players[
                (self.players['Team'] == team) & (self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # team, event, map
        elif team != 'All' and event != 'All' and map != 'All':
            data = self.players[
                (self.players['Team'] == team) & (self.players['Event'] == event) & (self.players['Map'] == map)]
        # team, mode, map
        elif team != 'All' and mode != 'All' and map != 'All':
            data = self.players[
                (self.players['Team'] == team) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # opponent, event, mode
        elif opponent != 'All' and event != 'All' and mode != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (
                        self.players['Mode'] == mode)]
        # opponent, event, map
        elif opponent != 'All' and event != 'All' and map != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (
                        self.players['Map'] == map)]
        # opponent, mode, map
        elif opponent != 'All' and event != 'All' and mode != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event) & (
                        self.players['Mode'] == mode)]
        # event, mode, map
        elif event != 'All' and mode != 'All' and map != 'All':
            data = self.players[
                (self.players['Event'] == event) & (self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team, opponent
        elif team != 'All' and opponent != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Opponent'] == opponent)]
        # team, event
        elif team != 'All' and event != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Event'] == event)]
        # team, mode
        elif team != 'All' and mode != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Mode'] == mode)]
        # team, map
        elif team != 'All' and map != 'All':
            data = self.players[(self.players['Team'] == team) & (self.players['Map'] == map)]
        # opponent, event
        elif opponent != 'All' and event != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Event'] == event)]
        # opponent, mode
        elif opponent != 'All' and mode != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Mode'] == mode)]
        # opponent, map
        elif opponent != 'All' and map != 'All':
            data = self.players[(self.players['Opponent'] == opponent) & (self.players['Map'] == map)]
        # event, mode
        elif event != 'All' and mode != 'All':
            data = self.players[(self.players['Event'] == event) & (self.players['Mode'] == mode)]
        # event, map
        elif event != 'All' and map != 'All':
            data = self.players[(self.players['Event'] == event) & (self.players['Map'] == map)]
        # mode, map
        elif mode != 'All' and map != 'All':
            data = self.players[(self.players['Mode'] == mode) & (self.players['Map'] == map)]
        # team
        elif team != 'All':
            data = self.players[self.players['Team'] == team]
        # opponent
        elif opponent != 'All':
            data = self.players[self.players['Opponent'] == opponent]
        # event
        elif event != 'All':
            data = self.players[self.players['Event'] == event]
        # mode
        elif mode != 'All':
            data = self.players[self.players['Mode'] == mode]
        # map
        elif map != 'All':
            data = self.players[self.players['Map'] == map]
        # none
        else:
            data = self.players
        return data

    def getRecords(self, data, type):
        return data[data[type] == data[type].max()]

    def findMatch(self, matchID):
        return self.matches.loc[matchID]

    def findMap(self, matchID, mapID):
        return self.maps.loc[matchID, mapID]

    def findMatchMaps(self, matchID):
        return self.maps.loc[matchID]

    def findPlayersMatch(self, matchID):
        return self.players.loc[matchID]

    def findPlayersMap(self, matchID, mapID):
        return self.players.loc[matchID, mapID]

class Team:

    def __init__(self, name="Team"):
        stats = CoDStats()
        self.name = name
        self.wins = 0
        self.losses = 0
        self.mapWins = 0
        self.mapLosses = 0
        self.modeWins = [0, 0, 0]
        self.modeLosses = [0, 0, 0]
        if self.name != "Team":
            self.teamMatchData = stats.matches[(stats.matches['Team 1'] == self.name) | (stats.matches['Team 2'] == self.name)]
            self.wins = self.teamMatchData[self.teamMatchData['Winner'] == self.name].shape[0]
            self.losses = self.teamMatchData.shape[0] - self.wins

            self.teamMapData = stats.maps[(stats.maps['Team 1'] == self.name) | (stats.maps['Team 2'] == self.name)]
            self.mapWins = self.teamMapData[self.teamMapData['Map Winner'] == self.name].shape[0]
            self.mapLosses = self.teamMapData.shape[0] - self.mapWins

            for k in range(3):
                self.teamModeData = stats.maps[((stats.maps['Team 1'] == self.name) & (stats.maps['Mode'] == stats.modes[k])) |
                                               ((stats.maps['Team 2'] == self.name) & (stats.maps['Mode'] == stats.modes[k]))]
                self.modeWins[k] = self.teamModeData[self.teamModeData['Map Winner'] == self.name].shape[0]
                self.modeLosses[k] = self.teamModeData.shape[0] - self.modeWins[k]

class Player:

    def __init__(self, name="Player"):
        stats = CoDStats()
        self.name = name
        if name != "Player":
            self.playerData = stats.players[stats.players['Player'] == name]
            self.kills = self.playerData['Kills'].sum()
            self.deaths = self.playerData['Deaths'].sum()
            self.kd = round(self.kills / self.deaths, 2)
        else:
            self.kills = 0
            self.deaths = 0
            self.kd = 0

    def getPlayerTeams(self):
        return np.flip(self.playerData[self.playerData['Player'] == self.name]['Team'].unique())

    def getPlayerEvents(self):
        return self.playerData[self.playerData['Player'] == self.name]['Event'].unique()

    def getPlayerKD(self, data):
        print(data)
        kills = data['Kills'].sum()
        deaths = data['Deaths'].sum()
        kd = round(kills / deaths, 2)
        return kills, deaths, kd

    def getPlayerMapRecord(self, *args, **kwargs):
        # gets win loss record for optional data subset or for all data for player
        data = kwargs.get('data', None)
        if data is None:
            data = self.playerData
        return data[data['Map Result'] == 'Win'].shape[0], data[data['Map Result'] == 'Loss'].shape[0]

    def getPlayerMatchIDs(self):
        # returns dictionary with match ID as key and the team the player was on at the time
        stats = CoDStats()
        matchIDs = []
        matches = {}
        for match in list(self.playerData.index.values):
            if match[0] not in matchIDs:
                matchIDs.append(match[0])
        for id in matchIDs:
            data = stats.findPlayersMatch(id)
            matches[id] = list(data[data['Player'] == self.name]['Team'])[0]
        return matches

    def getPlayerMapIDs(self):
        stats = CoDStats()
        mapIDs = []
        maps = {}
        for map in list(self.playerData.index.values):
            if map[1] not in mapIDs:
                mapIDs.append([map[0], map[1]])
        for id in mapIDs:
            data = stats.findPlayersMap(id[0], id[1])
            maps[id[0], id[1]] = list(data[data['Player'] == self.name]['Team'])[0]
        return maps