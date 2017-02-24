import os
import unittest
from urllib.parse import urlparse

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "capstone.config.TestingConfig"

from capstone import app
from capstone.database import Base, engine, session, Profile_Analysis, Entry
from capstone.extractor2 import *


class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)
       

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)
        
    def test_add_user_analysis(self):
        url = request.form['url']
        pr_ext = extractor2.ProfileExtractor(url)
        user_city_data = pr_ext.data_for_profile(capstone.DVExtractor)[1]
        user_profile_data = pr_ext.data_for_profile(capstone.DVExtractor)[0]
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
        profile_analysis.response_time_min = (user_city_data.loc['response_time_min'])
        profile_analysis.response_time_mean = (user_city_data.loc['response_time_mean'])
        profile_analysis.response_time_max = (user_city_data.loc['response_time_max'])
        entry = Entry()
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
        response = self.client.post("/")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")

        entry = entries[0]
        self.assertEqual(entry.title, "Test Entry")
        self.assertEqual(entry.content, "Test content")
        self.assertEqual(entry.author, self.user)

        entry = entries[0]
        
        
        
if __name__ == "__main__":
    unittest.main()