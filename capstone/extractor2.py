import requests
from bs4 import BeautifulSoup
import os
import sys
import time
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}

class ProfileExtractor(object):
    def __init__(self, url):
        self.url = url
        
    def data_for_profile(self, dv_ext):
        r = requests.get(self.url)
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        #times = []
        #fees = []
        #reviews = []
        #ratings = []
        #city = []
        #states = []
        #Extract fee
        fee = soup.findAll('span', {'class': 'dv-selected-service-rate__price'})[0].text.strip()[1:]
        #Extract total number of reviews
        profile = soup.findAll('span', {'data-scroll-link': 'profile-reviews'})
        if profile is not None and len(profile) > 0:
            review = soup.findAll('span', {'data-scroll-link': 'profile-reviews'})[0].text.replace('Reviews', '').replace('Review', '').strip()
        else:
            review = 0
        #Extract response time
        response = soup.findAll('li', {'class': 'dv-profile-list__item'})
        if response is not None and len(response) > 0:
            response_time = soup.findAll('li', {'class': 'dv-profile-list__item'})[1].text.replace('Responds within', '').strip()
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
        #fees.append(fee)
        #reviews.append(review)
        #ratings.append(rating)
        #times.append(response_time)
        #city.append(town)
        #states.append(state)
        user_data = {"fees": fee,
                    "reviews":review,
                    "ratings":rating,
                    "times": response_time,
                    "city":town,
                    "states":state}
        #df1['response_time'] = df1['response_time'].map(lambda x: 1 if 'minutes' in x else 2 if 'hour' in x else 3)
        #df1['review'] = df1['review'].map(lambda x: 0 if 'Testimonial' in x else x)  
        return (user_data, dv_ext.data_for_user(town))

cities = [['tx', "austin"], [ 'ca' , 'los-angeles'], ['ma', 'boston']]

class DVExtractor(object):
    def __init__(self):
        self.data_dir = 'crawl/' 
        self.crawl_cities()
        self.c_df = self.data_for_cities()
    
    def crawl_cities(self):
        # this builds the crawled data for cities 
        datadir = 'crawl/'
        if not(os.path.isdir(datadir)):
            os.makedirs(datadir)

        for city in cities:
            k = city[0]
            v = city[1]
            running = True
            page = 1
            print(k, v)
            time.sleep(1)
            while running:
                url = "https://dogvacay.com/dog-boarding--" + str(k) + "--" + str(v) +"?p="+str(page)
                filename = datadir + str(k) + '-' + str(v) + '-' + str(page) + '.htm'
                if not(os.path.isfile(filename)):
                    sys.stdout.write('-')
                    r = requests.get(url, headers=headers)
                    time.sleep(1)
                    f = open(filename, 'wb')
                    f.write(r.text.encode('ascii', 'replace'))
                    f.close()
                    data = r.text
                else:
                    sys.stdout.write('.')
                    f = open(filename, 'r')
                    data = f.read()
                    f.close()
                soup = BeautifulSoup(data, "lxml")
                pagination_links = soup.findAll('a', {'class': 'pagination-link'})
                running = False
                for pl in pagination_links:
                    if pl.text.find('Next') == 0:
                        running = True
                page+=1

    def data_for_cities(self):
        #Create empty lists
        times = []
        fees = []
        reviews = []
        city = []
        ratings = []
        for src in os.listdir(self.data_dir):
            # all the code in pynb in #Data extraction phase
            # returns the pandas data frame
            filename = self.data_dir + src
            print('Processing: ' + filename)
            f = open(filename, 'r')
            data = f.read()
            f.close()
            soup = BeautifulSoup(data, 'lxml')
            sitters = soup.findAll('div', {'class': 'dv-host-list-item'}) 
            for sitter in sitters:
                rtwrap = sitter.findAll('i', {'class': 'dv-icon dv-icon__clock'})
                responder = sitter.findAll('li', {'class': 'dv-search-badge-item'})
                clock = len(rtwrap)
                if clock > 0:
                    response_time = responder[0].text.replace('Responds in', '').strip()
                else:
                    response_time = 0
                fee = sitter.findAll('span', {'class': "dv-host-list-item__price__amount"})[0].text.replace('/night', '').strip()[1:]
                review = sitter.find('span', {'class': 'dv-host-review'})
                if review is not None and len(review) > 0:
                    review = review.text.replace('Reviews', '').replace('Review', '').strip()
                else:
                    review = 0
                full_star = sitter.findAll('i', {'class': 'dv-icon__star'})
                rating = len(full_star)
                half_star = sitter.findAll('i', {'class': 'dv-icon__star-half'})
                if len(half_star) > 0:
                    rating += .5
                town = soup.findAll('span', {'class': 'dv-hero__title__location'})[0].text.strip().split(',')[0]
                fees.append(fee)
                reviews.append(review)
                ratings.append(rating)
                city.append(town)
                times.append(response_time)
        #Dataframe from dict of objects 
        df2 = pd.DataFrame({'fee':fees,
                           'review':reviews,
                           'rating':ratings,
                           'town':city, 
                           'response_time': times})
        df2['response_time'] = df2['response_time'].astype(str)
        df2['review'] = df2['review'].astype(str)
        df2['response_time'] = df2['response_time'].map(lambda x: 1 if 'minutes' in x else 2 if 'hour' in x else 3)
        df2['review'] = df2['review'].map(lambda x: 0 if 'Testimonial' in x else x)                   
        df2['response_time'] = df2['response_time'].astype(int)
        df2['rating'] = df2['rating'].astype(int)
        df2['fee'] = df2['fee'].astype(int)
        df2['review'] = df2['review'].astype(float)
        df_1 = df2.groupby('town').mean()
        df_2 = df2.groupby('town').max()
        df_3 = df2.groupby('town').min()
        df_1.rename(columns={'fee': 'fee_mean', 'rating': 'rating_mean', 'response_time': 'response_time_mean', 'review': 'review_mean'}, inplace=True)
        df_2.rename(columns={'fee': 'fee_max', 'rating': 'rating_max', 'response_time': 'response_time_max', 'review': 'review_max'}, inplace=True)
        df_3.rename(columns={'fee': 'fee_min', 'rating': 'rating_min', 'response_time': 'response_time_min', 'review': 'review_min'}, inplace=True)
        df2 = pd.concat([df_1, df_2, df_3], axis=1)
        print(df2)
        return df2

    def data_for_user(self, user_city):
        print("-----------")
        print(user_city)
        print(self.c_df)
        return self.c_df.loc[user_city]

#def test():
#    dv_ext = DVExtractor()
#    user_url = "https://dogvacay.com/best-care-in-the-west-end-dog-boarding-242304?default_service=boarding"
#    pr_ext = ProfileExtractor(user_url)
#    user_data = pr_ext.data_for_profile(dv_ext)
#    print("============ User Data:")
#    print(user_data)

#if __name__ == "__main__":
#    test()
    
