import os
import unittest
from urllib.parse import urlparse

# Configuring the app to use the testing database
os.environ["CONFIG_PATH"] = "capstone.config.TestingConfig"

import capstone
from capstone import app
from capstone import extractor2
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
        response = self.client.post("/", data={
            "url": "https://dogvacay.com/best-care-in-the-west-end-dog-boarding-242304?default_service=boarding",
            "price_min": "5",
            "price_mean":"10",
            "price_max": "100"
        })
        ### Add to test
        #"rating_min": "5",
        #"rating_mean": "1",
        #"rating_max":"2",
        #"review_min":"0",
        #"review_mean":"1",
        #"review_max": "2",
        #"response_time_min, "0",
        #"response_time_mean,"1,
        #"response_time_max,"2",
        #"city": "Boston",
        #"price": "40",
        #"rating": "5",
        #"review": "20",
        #"response_time":"2"

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/profile")
        entries = session.query(Entry).all()
        profile_analysis = session.query(Profile_Analysis).all()
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        test_profile = profile_analysis[0]
        self.assertEqual(entry.url, "https://dogvacay.com/best-care-in-the-west-end-dog-boarding-242304?default_service=boarding")
        self.assertEqual(test_profile.price_min, 5)
        self.assertEqual(test_profile.price_mean, 10)
        self.assertEqual(test_profile.price_max,100)
        ###Add to test
        #self.assertEqual(test_profile.rating_min, "0")
        #self.assertEqual(test_profile.rating_mean, "1")
        #self.assertEqual(test_profile.rating_max, "2")
        #self.assertEqual(test_profile.review_min,"0)
        #self.assertEqual(test_profile.review_mean,"1") 
        #self.assertEqual(test_profile.review_max, "2)
        #self.assertEqual(test_profile.response_time_min, "0")
        #self.assertEqual(test_profile.response_time_mean,"1)
        #self.assertEqual(test_profile.response_time_max,"2")
        #self.assertEqual(test_entry.city, "Boston")
        #self.assertEqual(test_entry.price, "40")
        #self.assertEqual(test_entry.rating, "5")
        #self.assertEqual(test_entry.review, "20")
        #self.assertEqual(test_entry.response_time, "2")
    
        
if __name__ == "__main__":
    unittest.main()