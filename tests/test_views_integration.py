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
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/profile")
        entries = session.query(Entry).all()
        profile_analysis = session.query(Profile_Analysis).all()
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        test_profile = profile_analysis[0]
        self.assertEqual(entry.url, "https://dogvacay.com/best-care-in-the-west-end-dog-boarding-242304?default_service=boarding")
        #self.assertEqual(test_profile.price_min, 15)
        #self.assertEqual(test_profile.price_mean, 38.317221)
        #self.assertEqual(test_profile.price_max, 100)
        #self.assertEqual(test_profile.rating_min, 0)
        #self.assertEqual(test_profile.rating_mean, 3.613293)
        #self.assertEqual(test_profile.rating_max, 5)
        #self.assertEqual(test_profile.review_min, 0.0)
        #self.assertEqual(test_profile.review_mean,8.425982) 
        #self.assertEqual(test_profile.review_max, 104.0)
        #self.assertEqual(test_profile.response_time_min, 1)
        #self.assertEqual(test_profile.response_time_mean, 1.691843)
        #self.assertEqual(test_profile.response_time_max, 3)
        self.assertEqual(entry.city, "Boston")
        self.assertEqual(entry.price, 40)
        self.assertEqual(entry.rating, 5)
        self.assertEqual(entry.review, 21)
        self.assertEqual(entry.response_time, 2)
        
    def test_profile_get(self):
        response = self.client.post("/", data={
            "url": "https://dogvacay.com/best-care-in-the-west-end-dog-boarding-242304?default_service=boarding",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/profile")
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
if __name__ == "__main__":
    unittest.main()