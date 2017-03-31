from flask import render_template
from flask import request, redirect, url_for
from . import app
from .database import session, Profile_Analysis, Entry
import capstone
from capstone import extractor2
import os


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
    profile_analysis.price_mean = (user_city_data.loc['fee_mean'])
    profile_analysis.price_max = (user_city_data.loc['fee_max'])
    profile_analysis.rating_min = (user_city_data.loc['rating_min'])
    profile_analysis.rating_mean = (user_city_data.loc['rating_mean'])
    profile_analysis.rating_max = (user_city_data.loc['rating_max'])
    profile_analysis.review_min = (user_city_data.loc['review_min'])
    profile_analysis.review_mean = (user_city_data.loc['review_mean'])
    profile_analysis.review_max = (user_city_data.loc['review_max'])
    profile_analysis.response_time_min = (
        user_city_data.loc['response_time_min'])
    profile_analysis.response_time_mean = (
        user_city_data.loc['response_time_mean'])
    profile_analysis.response_time_max = (
        user_city_data.loc['response_time_max'])
    
    entry = Entry()
    if session.query(Entry).filter_by(url=url).first():
        session.query(Entry).get(url)
    else:
        entry.url = url
        entry.city = (user_profile_data)['city']
        entry.price = (user_profile_data)['fees']
        entry.rating = (user_profile_data)['ratings']
        entry.review = (user_profile_data)['reviews']
        entry.response_time = (user_profile_data)['times']
        session.add(entry)
    session.add(profile_analysis)
    session.query()
    session.commit()
    return redirect(url_for("profile_get", url=url))


@app.route("/profile", methods=["GET"])
def profile_get():
    url = request.args['url']
    profile = session.query(Profile_Analysis).get(1)
    price_min = profile.price_min
    price_mean = profile.price_mean
    price_max = profile.price_max
    rating_min = profile.rating_min
    rating_mean = profile.rating_mean
    rating_max = profile.rating_max
    review_min = profile.review_min
    review_mean = profile.review_mean
    review_max = profile.review_max
    response_time_min = profile.response_time_min
    if response_time_min == 1:
        response_min = 'minutes'
    elif response_time_min == 2:
        response_min = 'hour'
    else:
        response_min = 'days'
    response_time_mean = profile.response_time_mean
    if response_time_mean == 1:
        response_mean = 'minutes'
    elif response_time_mean == 2:
        response_mean = 'hour'
    else:
        response_mean = 'days'
    response_time_max = profile.response_time_max
    if response_time_max == 1:
        response_max = 'minutes'
    elif response_time_max == 2:
        response_max = 'hour'
    else:
        response_max = 'days'
    user = session.query(Entry).get(url)
    city = user.city
    price = user.price
    rating = user.rating
    review = user.review
    response_time = user.response_time
    if response_time == 1:
        response = 'minutes'
    elif response_time == 2:
        response = 'hour'
    else:
        response = 'days'
    if price == price_mean:
        result = "is on par with everyone else."
    elif price > price_mean:
        result = "is above the average price"
    else:
        result = "is below the average price"

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
        response_time_min=response_time_min,
        response_time_mean=response_time_mean,
        response_time_max=response_time_max,
        response_min=response_min,
        response_mean=response_mean,
        response_max=response_max,
        city=city,
        price=price,
        rating=rating,
        review=review,
        response_time=response_time,
        response=response,
        )
