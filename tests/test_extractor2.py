import os
import unittest
import datetime
import pandas as pd

# Configure your app to use the testing configuration
if not "CONFIG_PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "capstone.config.TestingConfig"

import capstone
from capstone.extractor2 import *

class ExtractorTests(unittest.TestCase):
    def test_data_for_profile(self):
        dv_ext = DVExtractor()
        user_url = "https://dogvacay.com/best-care-in-the-west-end-dog-boarding-242304?default_service=boarding"
        pr_ext = ProfileExtractor(user_url)
        user_city_data = pr_ext.data_for_profile(dv_ext)[0]
        self.assertEqual(user_city_data, {'ratings': 5, 'fees': '40', 'states': 'MA', 'reviews': '20', 'times': 2, 'city': 'Boston'})
        
    #def test_data_for_cities(self):
    #    dv_ext = DVExtractor()
    #    city_data = dv_ext.data_for_profile()
    #    self.assertEqual(city_data, df2)
        
if __name__ == "__main__":
    unittest.main()