import requests
from bs4 import BeautifulSoup
import os
import sys
import time
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}

cities = [['tx', "austin"] ,
          [ 'ca' , 'los-angeles'] ,
          [ 'ga' , 'atlanta'] ,
          [ 'ma' , 'boston'] ,
          [ 'nc' , 'charlotte'] ,
          [ 'tx' , 'dallas'] ,
          [ 'co' , 'denver'] ,
          [ 'tx' , 'houston'] ,
          [ 'fl' , 'miami'] ,
          [ 'mn' , 'minneapolis'] ,
          [ 'ny' , 'new-york'] ,
          [ 'pa' , 'philadelphia'] ,
          [ 'az' , 'phoenix'] ,
          [ 'or' , 'portland'] ,
          [ 'ca' , 'san-francisco'] ,
          [ 'ca' , 'san-diego'] ,
          [ 'wa' , 'seattle'] ,
          [ 'dc' , 'washington']]


class DVExtractor:
    def __init__(self):
        self.data_dir = 'crawl/' 
        self.data_for_cities()

    def data_for_cities(self):
        # this builds the crawled data for cities 
        datadir = 'crawl/'
        if not(os.path.isdir(datadir)):
            os.makedirs(datadir)

        for city in cities:
            k = city[0]
            v = city[1]
            running = True
            page = 1
            print('')
            print(k,v)
            time.sleep(1)
            while running:
                url = "https://dogvacay.com/dog-boarding--" + k + "--" + v +"?p="+str(page)
                filename = datadir + k + '-' + v + '-' + str(page) + '.htm'
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
                        #print(url)
                        #print(pl)
                page+=1


    def data_for_profile(self, user_profile_url):
        #Create empty lists
        times = []
        fees = []
        reviews = []
        repeats = []
        city = []
        ratings = []
        name = []
        urls = []
        hostids = []
        for src in os.listdir(self.data_dir):
        # all the code in pynb in #Data extraction phase
            # returns the pandas data frame
            filename = self.data_dir + src
            #print('Processing: ' + filename)
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
                repeat = sitter.find('span', {'class': 'dv-host-repeat'})
                if repeat is not None and len(repeat) > 0:
                    repeat = repeat.text.strip().replace('Repeat Guests', '').replace('Repeat Guest', '')
                else:
                    repeat = 0
                town = soup.findAll('span', {'class': 'dv-hero__title__location'})[0].text.strip().split(',')[0]
                endpoint = (sitter.get('data-href'))
                if endpoint is not None:
                    url = endpoint
                host = (sitter.get('data-host-id'))
                if host is not None:
                    hostid = host
                fees.append(fee)
                reviews.append(review)
                ratings.append(rating)
                repeats.append(repeat)
                city.append(town)
                times.append(response_time)
                urls.append(url)
                hostids.append(hostid)
        #Dataframe from dict of objects 
        df = pd.DataFrame({'fee':fees,
                           'review':reviews,
                           'rating':ratings,
                           'repeat':repeats,
                           'town':city, 
                           'response_time': times,
                           'url':urls,
                           'hostid':hostids})
def test():
    test1 = DVExtractor()
    test1.data_for_profile(nothingyet)

if __name__ == "__main__":
    test()

        