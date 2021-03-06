from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Entry(Base):
    __tablename__ = "entry"

    #id = Column(Integer, primary_key=True)
    url = Column(String, primary_key=True)
    city = Column(String)
    price = Column(Integer)
    rating = Column(Integer)
    review = Column(Integer)
    response_time = Column(Integer)
    city_profile = relationship("Profile_Analysis", backref="entry")
    
class Profile_Analysis(Base):
    __tablename__ = "profile_analysis"
    
    id = Column(Integer, primary_key=True)
    price_min = Column(Integer)
    price_mean = Column(Integer)
    price_max = Column(Integer)
    rating_min = Column(Integer)
    rating_mean = Column(Integer)
    rating_max = Column(Integer)
    review_min = Column(Integer)
    review_mean = Column(Integer)
    review_max = Column(Integer)
    response_time_min = Column(Integer)
    response_time_mean = Column(Integer)
    response_time_max = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    entry_url = Column(String, ForeignKey('entry.url'))
    
#Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)
