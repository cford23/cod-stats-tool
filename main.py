from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/statsEntry")
def statsEntry():
    return render_template("statsEntry.html")

@app.route("/displayStats")
def displayStats():
    return render_template("displayStats.html")

if __name__ == "__main__":
    app.run(debug=True)