from flask import render_template
from flask import request, redirect, url_for
from . import app
from .extractor2 import ProfileExtractor

@app.route("/")
def landing_page():
    return render_template("landing_page.html")

@app.route('/profile_analysis', methods=["GET"])
def analysis_for_user():
    url = request.form['url']
    profile_ext = ProfileExtractor()
    profile_ext.data_for_profile(url)
    return render_template("analysis_page.html")
