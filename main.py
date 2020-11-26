from flask import Flask, render_template, request, flash, redirect
from models import Schema

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/statsEntry")
def statsEntry():
    return render_template("statsEntry.html")

@app.route("/viewStats/")
def viewStats():
    results = Schema().getTeamMatches("Minnesota Rokkr")
    return render_template("viewStats.html", tables=[results.to_html(classes="data")])

if __name__ == "__main__":
    app.run(debug=True)