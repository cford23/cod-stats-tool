from flask import Flask, render_template, request
from models import CoDStats, Team, Player
import pandas as pd

app = Flask(__name__)

stats = CoDStats()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/viewMatches", methods=["GET", "POST"])
def viewMatches():
    selectedItems = ['', '', '']
    wins = 0
    losses = 0
    if request.method == "POST" or request.method == "GET":
        team = request.form.get("team")
        selectedItems[0] = team
        opponent = request.form.get("opponent")
        selectedItems[1] = opponent
        event = request.form.get("event")
        selectedItems[2] = event
        results = stats.getMatches(team, opponent, event)
        length = results.shape[0]
        if team != 'All':
            wins, losses = stats.getViewMatchRecord(team, results)
    #return render_template("viewMatches.html", stats=stats, tables=[results.to_html(classes="data", index=False)], selectedItems=selectedItems, length=length, team=team, wins=wins, losses=losses)
    return render_template("viewMatches.html", stats=stats, data=results.to_dict(orient='records'),
                           selectedItems=selectedItems, length=length, team=team, wins=wins, losses=losses)

@app.route("/matchView/<matchID>")
def matchView(matchID):
    matchID = int(matchID)
    data = stats.getMatchData(matchID=matchID).iloc[0]
    mapData = stats.getMapData(matchID=matchID)
    playerData = stats.getPlayerData(matchID=matchID)
    team1 = data['Team 1']
    team2 = data['Team 2']
    team1Abbr = stats.teamAbbrs[data['Team 1']]
    team2Abbr = stats.teamAbbrs[data['Team 2']]

    overall = playerData.groupby(['Player', 'Team'])[['Score', 'Kills', 'Deaths', 'Damage']].sum()
    overall['K/D'] = round(overall['Kills'] / overall['Deaths'], 2)
    overall['Engagements'] = overall['Kills'] + overall['Deaths']
    overall['Difference'] = overall['Kills'] - overall['Deaths']
    overall = overall.reset_index()
    overall = pd.DataFrame(overall, columns=['Team', 'Player', 'Score', 'Kills', 'Deaths', 'K/D', 'Engagements', 'Difference', 'Damage'])
    overall = overall.sort_values(by='Team')

    return render_template("matchView.html", data=data.to_dict(), mapData=mapData.to_dict(orient='records'),
                           playerData=playerData.to_dict(orient='records'), team1=team1, team2=team2,
                           team1Abbr=team1Abbr, team2Abbr=team2Abbr, overall=overall.to_dict(orient='records'))

@app.route("/viewMaps", methods=["GET", "POST"])
def viewMaps():
    selectedItems = ['', '', '', '', '']
    wins = 0
    losses = 0
    if request.method == "POST" or request.method == "GET":
        team = request.form.get("team")
        opponent = request.form.get("opponent")
        event = request.form.get("event")
        mode = request.form.get("mode")
        map = request.form.get("map")

        selectedItems[0] = team
        selectedItems[1] = opponent
        selectedItems[2] = event
        selectedItems[3] = mode
        selectedItems[4] = map

        results = stats.getMaps(team, opponent, event, mode, map)
        length = results.shape[0]
        if team != 'All':
            wins, losses = stats.getViewMapRecord(team, results)
    return render_template("viewMaps.html", stats=stats, data=results.to_dict(orient='records'),
                           selectedItems=selectedItems, length=length, wins=wins, losses=losses, team=team)
    # return render_template("viewMaps.html", stats=stats, tables=[results.to_html(classes="data", index=False)], selectedItems=selectedItems, length=length, wins=wins, losses=losses, team=team)

@app.route("/viewPlayers", methods=["GET", "POST"])
def viewPlayers():
    player = Player()
    selectedItems = ['', '', '', '', '', '']
    playerTeams = []
    playerEvents = []
    kills = 0
    deaths = 0
    kd = 0
    mapRecord = [0, 0]
    results = stats.players.head(0)
    length = results.shape[0]
    if request.method == "POST":
        player = Player(request.form.get("player"))
        team = request.form.get("team")
        opponent = request.form.get("opponent")
        event = request.form.get("event")
        mode = request.form.get("mode")
        map = request.form.get("map")

        selectedItems[0] = player.name
        selectedItems[1] = team
        selectedItems[2] = opponent
        selectedItems[3] = event
        selectedItems[4] = mode
        selectedItems[5] = map

        playerTeams = player.getPlayerTeams()
        playerEvents = player.getPlayerEvents()
        results = stats.getPlayers(player.name, team, opponent, event, mode, map)
        results.dropna(how='all', axis=1, inplace=True)
        kills, deaths, kd = player.getPlayerKD(results)
        mapRecord[0], mapRecord[1] = player.getPlayerMapRecord(data=results)
        length = results.shape[0]
    return render_template("viewPlayers.html", player=player, stats=stats, tables=[results.to_html(classes="data", index=False)], playerTeams=playerTeams, playerEvents=playerEvents, selectedItems=selectedItems, kills=kills, deaths=deaths, kd=kd, length=length, mapRecord=mapRecord)

@app.route("/matchupPreview", methods=["GET", "POST"])
def matchupPreview():
    selectedItems = ['', '']
    team1 = Team()
    team2 = Team()
    results = stats.getMatchupPreview(team1.name, team2.name)
    if request.method == "POST":
        team1 = Team(request.form.get("team1"))
        team2 = Team(request.form.get("team2"))

        selectedItems[0] = team1.name
        selectedItems[1] = team2.name

        results = stats.getMatchupPreview(team1.name, team2.name)
    return render_template("matchupPreview.html", team1=team1, team2=team2, stats=stats, results=results, selectedItems=selectedItems)

@app.route("/mapPreview", methods=["GET", "POST"])
def mapPreview():
    team1 = Team()
    team2 = Team()
    maps = []
    team1Records = {'wins': [0, 0, 0, 0, 0], 'losses': [0, 0, 0, 0, 0]}
    team2Records = {'wins': [0, 0, 0, 0, 0], 'losses': [0, 0, 0, 0, 0]}
    headToHead = {team1.name: [0, 0, 0, 0, 0], team2.name: [0, 0, 0, 0, 0]}
    selectedItems = ['', '', ['', '', '', '', '']]

    if request.method == "POST":
        team1 = Team(request.form.get('team1'))
        team2 = Team(request.form.get('team2'))
        maps = [request.form.get('map1'),
                request.form.get('map2'),
                request.form.get('map3'),
                request.form.get('map4'),
                request.form.get('map5')]

        selectedItems[0] = team1.name
        selectedItems[1] = team2.name
        for k in range(5):
            selectedItems[2][k] = maps[k]

        team1Records, team2Records, headToHead = stats.getMapPreview(team1.name, team2.name, maps)
    return render_template("mapPreview.html", team1=team1, team2=team2, stats=stats, maps=maps, team1Records=team1Records, team2Records=team2Records, headToHead=headToHead, selectedItems=selectedItems)

@app.route("/teamLeaderboard", methods=["GET", "POST"])
def teamLeaderboard():
    selectedItems = ['Match Win Percent', '', '', '', '']
    results = {}

    if request.method == "POST":
        type = request.form.get('type')
        opponent = request.form.get('opponent')
        event = request.form.get('event')
        mode = request.form.get('mode')
        map = request.form.get('map')

        selectedItems[0] = type
        selectedItems[1] = opponent
        selectedItems[2] = event
        selectedItems[3] = mode
        selectedItems[4] = map

        results = stats.getTeamLeaderboard(type, opponent, event, mode, map)
        results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
        if opponent != 'All':
            del results[opponent]

    return render_template("teamLeaderboard.html", stats=stats, selectedItems=selectedItems, results=results)

@app.route("/playerLeaderboard", methods=["GET", "POST"])
def playerLeaderboard():
    results = {}
    selectedItems = ['Kills', '', '', '', '', '']

    types = list(stats.players.columns)
    startIndex = types.index('Score')
    types = types[startIndex:]
    types.remove('Map Result')

    if request.method == 'POST':
        type = request.form.get('type')
        team = request.form.get('team')
        opponent = request.form.get('opponent')
        event = request.form.get('event')
        mode = request.form.get('mode')
        map = request.form.get('map')

        selectedItems[0] = type
        selectedItems[1] = team
        selectedItems[2] = opponent
        selectedItems[3] = event
        selectedItems[4] = mode
        selectedItems[5] = map

        results = stats.getPlayerLeaderboard(type, team, opponent, event, mode, map)
        results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    return render_template("playerLeaderboard.html", stats=stats, results=results, types=types, selectedItems=selectedItems)

@app.route("/records", methods=["GET", "POST"])
def records():
    selectedItems = ['Kills', '', '', '', '', '']
    type = 'Kills'

    types = list(stats.players.columns)
    startIndex = types.index('Score')
    types = types[startIndex:]
    types.remove('Map Result')

    if request.method == 'POST' or request.method == 'GET':
        team = request.form.get('team')
        opponent = request.form.get('opponent')
        event = request.form.get('event')
        mode = request.form.get('mode')
        map = request.form.get('map')
        type = request.form.get('type')

        selectedItems[0] = type
        selectedItems[1] = team
        selectedItems[2] = opponent
        selectedItems[3] = event
        selectedItems[4] = mode
        selectedItems[5] = map

        data = stats.getRecordsRange(team, opponent, event, mode, map)
        if data.shape[0] != 0:
            typeRecords = stats.getRecords(data, type)
        else:
            typeRecords = data
        typeRecords.dropna(how='all', axis=1, inplace=True)

    return render_template("records.html", stats=stats, types=types, type=type, tables=[typeRecords.to_html(classes="data", index=False)], selectedItems=selectedItems)

if __name__ == "__main__":
    app.run()