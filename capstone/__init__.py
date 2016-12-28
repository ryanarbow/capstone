import os

from flask import Flask

#create app
app = Flask(__name__)
#
config_path = os.environ.get("CONFIG_PATH", "capstone.config.DevelopmentConfig")
app.config.from_object(config_path)

#importing after the object has been created
#files will make use of app object
from . import views
from . import filters

 
from . import extractor2

DV_EXTRACTOR = extractor2.DVExtractor()