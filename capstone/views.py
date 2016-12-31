from flask import render_template
from flask import request, redirect, url_for
from . import app
from .database import session, User, Profile_Analysis
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
    profile_analysis = session.query(Profile_Analysis).filter_by(id=id)
    profile_analysis.price_min = (user_data.loc['fee_min'])
    profile_analysis.price_mean = (user_data.loc['fee_mean']) 
    profile_analysis.price_max = (user_data.loc['fee_max'])
    profile_analysis.rating_min = (user_data.loc['rating_min'])
    profile_analysis.rating_mean = (user_data.loc['rating_mean'])
    profile_analysis.rating_max = (user_data.loc['rating_max'])
    profile_analysis.review_min = (user_data.loc['review_min'])
    profile_analysis.review_mean = (user_data.loc['review_mean'])
    profile_analysis.review_max = (user_data.loc['review_max'])
    profile_analysis.response_time_min = (user_data.loc['response_time_min'])
    profile_analysis.response_time_mean = (user_data.loc['response_time_mean'])
    profile_analysis.response_time_max = (user_data.loc['response_time_max'])
    session.save(profile_analysis)
    session.commit()
    return redirect(url_for("profile_get"))
    
@app.route("/profile", methods=["GET"])
def profile_get(id):
    profile_analysis = session.query(Profile_Analysis).get(id)
    price_min = profile_analysis.price_min
    price_mean = profile_analysis.price_mean
    price_max = profile_analysis.price_max
    rating_min = profile_analysis.rating_min
    rating_mean = profile_analysis.rating_mean 
    rating_max = profile_analysis.rating_max 
    review_min =profile_analysis.review_min 
    review_mean = profile_analysis.review_mean
    review_max = profile_analysis.review_max
    response_time_min = profile_analysis.response_time_min
    response_time_mean = profile_analysis.response_time_mean
    response_time_max = profile_analysis.response_time_max
    return render_template("analysis_page.html", price_min=price_min)
