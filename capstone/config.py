import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/capstone" #"postgresql://deepaksurti:deepaksurti@localhost:5432/dv-capstone"
    DEBUG = True
