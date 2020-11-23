from flask import Flask, render_template
from models import Schema

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/statsEntry")
def statsEntry():
    return render_template("statsEntry.html", tables=[Schema().matches.to_html(classes="data")], titles=Schema().matches.columns.values)

@app.route("/displayStats")
def displayStats():
    return render_template("displayStats.html")

if __name__ == "__main__":
    Schema()
    app.run(debug=True)