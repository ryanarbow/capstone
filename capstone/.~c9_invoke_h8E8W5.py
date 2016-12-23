import requests
from bs4 import BeautifulSoup
import os
import sys
import time
import pandas as pd

class ProfileExtractor:
    def data_for_profile(self, user_profile_url):
        r = requests.get(user_profile_url)
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        times = []
        fees = []
        reviews = []
        ratings = []
        city = []
        states = []
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
        town = soup.findAll('div', {'class': 'dv-profile-booking__address'})[0].text.strip().split(',')[0]
        state = soup.findAll('div', {'class': 'dv-profile-booking__address'})[0].text.strip().split(',')[1].strip()[:2]
        fees.append(fee)
        reviews.append(review)
        ratings.append(rating)
        times.append(response_time)
        city.append(town)
        states.append(state)
    
        df = pd.DataFrame({'fee':fees,
                           'review':reviews,
                           'rating':ratings,
                           'response_time': times,
                           'town':city,
                           'state':states})
        print(df)
        
        
def test():
    test1 = ProfileExtractor()
    test1.data_for_profile("https://dogvacay.com/best-care-in-the-west-end-dog-boarding-242304?default_service=boarding")

if __name__ == "__main__":
    test()