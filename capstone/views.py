from flask import render_template
from flask import request, redirect, url_for
from . import app
from .database import session, Profile_Analysis, Entry
import capstone
from capstone import extractor2
import os
from sqlalchemy import desc


@app.route("/", methods=["GET"])
def landing_page():
    return render_template("landing_page.html")

@app.route('/', methods=["POST"])
def analysis_for_user():
    if os.environ["CONFIG_PATH"] == "capstone.config.TestingConfig":
        data_dir = os.environ["TEST_DV_EXT"]
        dv_ext = extractor2.DVExtractor(data_dir)
    else:
        dv_ext = capstone.DVExtractor
    url = request.form['url']
    pr_ext = extractor2.ProfileExtractor(url)
    user_city_data = pr_ext.data_for_profile(dv_ext)[1]
    user_profile_data = pr_ext.data_for_profile(dv_ext)[0]
    profile_analysis = Profile_Analysis()
    profile_analysis.price_min = (user_city_data.loc['fee_min'])
    profile_analysis.price_mean = (user_city_data.loc['fee_median'])
    profile_analysis.price_max = (user_city_data.loc['fee_max'])
    profile_analysis.rating_min = (user_city_data.loc['rating_min'])
    profile_analysis.rating_mean = (user_city_data.loc['rating_median'])
    profile_analysis.rating_max = (user_city_data.loc['rating_max'])
    profile_analysis.review_min = (user_city_data.loc['review_min'])
    profile_analysis.review_mean = (user_city_data.loc['review_median'])
    profile_analysis.review_max = (user_city_data.loc['review_max'])
    profile_analysis.response_time_min = (
        user_city_data.loc['response_time_min'])
    profile_analysis.response_time_mean = (
        user_city_data.loc['response_time_median'])
    profile_analysis.response_time_max = (
        user_city_data.loc['response_time_max'])
    
    if session.query(Entry).filter_by(url=url).first():
        print("Entry exists for this url")
        e = session.query(Entry).get(url)
        profile_analysis.entry_url = e.url
    else:
        print("Creating an Entry for a new url")
        entry = Entry()
        entry.url = url
        entry.city = (user_profile_data)['city']
        entry.price = (user_profile_data)['fees']
        entry.rating = (user_profile_data)['ratings']
        entry.review = (user_profile_data)['reviews']
        entry.response_time = (user_profile_data)['times']
        profile_analysis.entry_url = entry.url
        session.add(entry)
    session.add(profile_analysis)
    session.query()
    session.commit()
    return redirect(url_for("profile_get", url=url))


@app.route("/profile", methods=["GET"])
def profile_get():
    url = request.args['url']
    profiles = session.query(Profile_Analysis).filter(Profile_Analysis.entry_url == url).order_by(desc(Profile_Analysis.timestamp)).all()
    profile = profiles[0]
    print("Fetched profile analysis with id timestamp : ", profile.id, profile.timestamp)
    price_min = profile.price_min
    price_mean = profile.price_mean
    price_max = profile.price_max
    rating_min = profile.rating_min
    rating_mean = profile.rating_mean
    rating_max = profile.rating_max
    review_min = profile.review_min
    review_mean = profile.review_mean
    review_max = profile.review_max
    user = session.query(Entry).get(url)
    city = user.city
    price = user.price
    if price == price_mean:
        price_result = "is on par with everyone else."
    elif price > price_mean:
        price_result = "is above average."
    else:
        price_result = "is below average."
    rating = user.rating
    if rating == rating_mean:
        rating_result = "is on par with everyone else."
    elif rating > rating_mean:
        rating_result = "is above average. Nice job!"
    else:
        rating_result = "is below average."
    review = user.review
    if review == review_mean:
        review_result = "is on par with everyone else."
    elif review > review_mean:
        review_result = "is above average. Congrats! But WTH,"
    else:
        review_result = "is below average."
    return render_template(
        "analysis_page.html",
        price_min=price_min,
        price_mean=price_mean,
        price_max=price_max,
        rating_min=rating_min,
        rating_mean=rating_mean,
        rating_max=rating_max,
        review_min=review_min,
        review_mean=review_mean,
        review_max=review_max,
        city=city,
        price=price,
        rating=rating,
        review=review,
        price_result=price_result,
        rating_result=rating_result,
        review_result=review_result
        )

@app.route("/about", methods=["GET"])
def about_page():
    return render_template("about_page.html")