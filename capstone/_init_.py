from flask import Flask

#create app
app = Flask(__name__)

#importing after the object has been created
#files will make use of app object
from . import views
from . import filters