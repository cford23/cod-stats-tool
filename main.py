from flask import Flask, render_template, request, flash, redirect
from models import CoDStats, Team

app = Flask(__name__)

stats = CoDStats()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/statsEntry")
def statsEntry():
    return render_template("statsEntry.html")

@app.route("/viewMatches", methods=["GET", "POST"])
def viewMatches():
    if request.method == "POST":
        team = request.form.get("team")
        opponent = request.form.get("opponent")
        if team != "All" and opponent == "All":
            results = stats.getTeamMatches(team)
        elif team != "All" and opponent != "All":
            results = stats.getTeamOppMatches(team, opponent)
        else:
            results = stats.getAllMatches()
    else:
        results = stats.getAllMatches()
    return render_template("viewMatches.html", teams=stats.teams, tables=[results.to_html(classes="data")])

@app.route("/viewMaps", methods=["GET", "POST"])
def viewMaps():
    if request.method == "POST":
        team = request.form.get("team")
        mode = request.form.get("mode")
        if team != "All" and mode != "All": # team and mode
            results = stats.getTeamModeMaps(team, mode)
        elif team != "All" and mode == "All": # team
            results = CoDStats.getTeamMaps(team)
        elif team == "All" and mode != "All": # mode
            results = stats.getModeMaps(mode)
        else:
            results = stats.getTeamMaps(team)
    else:
        results = stats.getAllMaps()
    return render_template("viewMaps.html", teams=stats.teams, tables=[results.to_html(classes="data")])

@app.route("/viewPlayers", methods=["GET", "POST"])
def viewPlayers():
    kills = 0
    deaths = 0
    kd = 0
    player = ""
    if request.method == "POST" or request.method == "GET":
        player = request.form.get("player")
        kills, deaths, kd = stats.getPlayerKD(player)
    return render_template("viewPlayers.html", players=stats.playerList, kills=kills, player=player, deaths=deaths, kd=kd)

@app.route("/matchupPreview", methods=["GET", "POST"])
def matchupPreview():
    team1 = Team()
    team2 = Team()
    if request.method == "POST":
        team1 = Team(request.form.get("team1"))
        team2 = Team(request.form.get("team2"))
    return render_template("matchupPreview.html", team1=team1, team2=team2, stats=stats)

@app.route("/mapPreview", methods=["GET", "POST"])
def mapPreview():
    team1 = Team()
    team2 = Team()
    maps = []
    if request.method == "POST":
        team1 = Team(request.form.get('team1'))
        team2 = Team(request.form.get('team2'))
        maps = [request.form.get('map1'),
                request.form.get('map2'),
                request.form.get('map3'),
                request.form.get('map4'),
                request.form.get('map5')]
    return render_template("mapPreview.html", team1=team1, team2=team2, stats=stats, maps=maps)

if __name__ == "__main__":
    app.run(debug=True)