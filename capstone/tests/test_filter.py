import os
import unittest
import datetime

# Configure your app to use the testing configuration
if not "CONFIG_PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "capstone.config.TestingConfig"

import capstone
from capstone.extractor2 import *

class FilterTests(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()