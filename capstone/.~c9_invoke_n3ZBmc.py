from flask import render_template
from flask import request, redirect, url_for
from . import app
import capstone
from capstone import extractor2

@app.route("/", methods=["GET"])
def landing_page():
    return render_template("landing_page.html")

@app.route('/', methods=["POST"])
def analysis_for_user():
    url = request.form['url']
    pr_ext = extractor2.ProfileExtractor(url)
    user_data = pr_ext.data_for_profile(capstone.DVExtractor)
    return redirect(url_for("profile_get"))

@app.route("/profile", methods=["GET"])
def profile_get():
    return render_template("analysis_page.html", price_min="100")









