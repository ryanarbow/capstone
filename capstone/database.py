from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    city = Column(String)
    
class Profile(Base):
    __tablename__ = "username_profile"
    
    id = Column(Integer, primary_key=True)
    price_min = Column(Integer)
    price_max = Column(Integer)
    rating_min = Column(Integer)
    rating_max = Column(Integer)
    reviews_min = Column(Integer)
    reviews_max = Column(Integer)
    response_time_min = Column(Integer)
    response_time_max = Column(Integer)
    
Base.metadata.create_all(engine)
