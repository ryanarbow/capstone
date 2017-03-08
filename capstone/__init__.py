import os

from flask import Flask

#create app
app = Flask(__name__)
#
config_path = os.environ.get("CONFIG_PATH", "capstone.config.DevelopmentConfig")
os.environ["CONFIG_PATH"] = config_path
app.config.from_object(config_path)

#importing after the object has been created
#files will make use of app object
from . import views
#from . import filters

 
from . import extractor2

DVExtractor = extractor2.DVExtractor()