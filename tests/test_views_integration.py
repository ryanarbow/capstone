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
       

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)
        
    

if __name__ == "__main__":
    unittest.main()