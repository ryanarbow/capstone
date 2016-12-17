from flask import render_template

from . import app

@app.route("/")
def landing_page():
    return render_template("landing_page.html")

@app.route("/user/", methods=["GET"])
def analysis_page():
    return render_template("analysis_page.html")