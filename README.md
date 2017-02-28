What is this?
Capstone is a profile insights application for DogVacay hosts. 

This project is the culmination of my studies in the Programming in Python course offered through Thinkful. Some assets were created during my studies of the Data Science in Python course, also offered through Thinkful. 

Why?
What should our price be? How does rating impact bookings? What’s the average response time? When my wife and I signed-up as DogVacay hosts we had numerous questions such as these, wondering if and how answering these may impact our success as hosts.

Important 

extractor2.py
extractor2.py performs two critical function: extracting web content from a given both the  contains two important classes: ProfileExtractor and DVExtractor.

ProfileExtractor includes one method:
data_for_profile() - From a given url, data_for_profile uses BeautifulSoup to extract web page content from a host’s profile and creates a dictionary of values including price, number of reviews, their rating, their response time, and city - state?. 
When this method is called it returns 1) a dictionary of the host’s data and 2) a dataframe of the host’s city values, leveraging the  data_for_user method from DVExtractor class.

DV Extractor includes three methods:
crawl_cities() - From a given list of cities (ex. cities = [['tx', "austin"], ['ma', 'boston']], crawl_cities loops through every page for a given city, uses BeautifulSoup to extract web page content, and creates a ‘/crawl’ directory filled with scraped htm pages. 

data_for_cities() - The data_for_cities method takes the ‘crawl’ directory and loops through the scraped web content to extract specific values from a host’s listing including price, number of reviews, their rating, their response time, and city. This data is then assembled into a pandas dataframe, cleaned, and grouped by city. After grouping by city, we then find the min, mean, and max for the values.

data_for_user() - 


views.py 
views.py defines three app routes in order to render the landing page, submit extracted data to the database, and pull data to render the this data on the profile_analysis page. 