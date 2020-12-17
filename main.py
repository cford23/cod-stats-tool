from flask import Flask, render_template, request, flash, redirect
from models import CoDStats

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/statsEntry")
def statsEntry():
    return render_template("statsEntry.html")

@app.route("/viewStats", methods=["GET", "POST"])
def viewStats():
    if request.method == "POST":
        team = request.form.get("team")
        opponent = request.form.get("opponent")
        results = CoDStats().getTeamOppMatches(team, opponent)
    else:
        results = CoDStats().getAllMatches()
    return render_template("viewStats.html", tables=[results.to_html(classes="data")])

if __name__ == "__main__":
    app.run(debug=True)