import requests
import BeautifulSoup
import pandas as pd
import sqlite3 as lite
import os
import sys

class DVExtractor:
    def __init__(self):
        self.data_for_profile()

    def data_for_profile(self, url):
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        times = []
        fees = []
        reviews = []
        ratings = []
        #Extract fee
        fee = soup.findAll('span', {'class': 'dv-selected-service-rate__price'})[0].text.strip()
        #Extract total number of reviews
        profile = soup.findAll('span', {'data-scroll-link': 'profile-reviews'})
        if profile is not None and len(profile) > 0:
            review = soup.findAll('span', {'data-scroll-link': 'profile-reviews'})[0].text.strip()
        else:
            review = 0
        #Extract response time
        response = soup.findAll('li', {'class': 'dv-profile-list__item'})
        if response is not None and len(response) > 0:
            response_time = soup.findAll('li', {'class': 'dv-profile-list__item'})[1].text.strip()
        else:
            response_time = 0
        #Extract star rating
        stars = review_stars = soup.findAll('ul', {'class': 'rating dv-review-stars'})
        if stars is not None and len(stars) > 0:
            review_stars = soup.findAll('ul', {'class': 'rating dv-review-stars'})[0]
            full_star = review_stars.findAll('i', {'class': ' dv-icon dv-icon__star '})
            rating = len(full_star)
            half_star = soup.findAll('i', {'class': ' dv-icon dv-icon__star-half '})
            if len(half_star) > 0:
                rating += .5
        else:
            rating = 0
        fees.append(fee)
        reviews.append(review)
        ratings.append(rating)
        times.append(response_time)
    
        df = pd.DataFrame({'fee':fees,
                           'review':reviews,
                           'rating':ratings,
                           'response_time': times})
        print(df)
        
def test():
    test1 = DVExtractor()
    test1.data_for_profile("https://dogvacay.com/major-poochy-dog-services-dog-boarding-484614?default_service=boarding")

if __name__ == "__main__":
    test()