import os
import unittest
from urllib.parse import urlparse

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "capstone.config.TestingConfig"

from capstone import app
from capstone.database import Base, engine, session, Profile_Analysis, Entry


class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.profile_analysis = Profile_Analysis(
                                id = "1",
                                price_min = "2",
                                price_mean = "3",
                                price_max = "4",
                                rating_min = "5",
                                rating_mean = "6",
                                rating_max = "7",
                                review_min = "8",
                                review_mean = "9",
                                review_max = "10",
                                response_time_min = "11",
                                response_time_mean = "12",
                                response_time_max = "13",
                                timestamp = "2017-02-05 17:26:17.74689",
                                entry_url = "url")
        session.add(self.profile_analysis)
        session.commit()

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

if __name__ == "__main__":
    unittest.main()