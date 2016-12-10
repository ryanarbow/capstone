import requests
from bs4 import BeautifulSoup
import os
import sys
import time

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


    #def data_for_profile(self, user_profile_url):
    #    for src in os.listdir(self.data_dir):
        # all the code in pynb in #Data extraction phase
            # returns the pandas data frame


