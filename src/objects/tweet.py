from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, BigInteger
from sqlalchemy.orm import relationship
from src.connection import Base
from geoalchemy2 import Geometry

class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(String(20), primary_key=True)
    content = Column('content', String)
    location = Column('location', Geometry(geometry_type='POINT', srid=4326))
    retweet_count = Column('retweet_count', Integer)
    favorite_count = Column('favorite_count', Integer)
    happened_at = Column('happened_at', TIMESTAMP(timezone=True))
    author_id = Column(BigInteger, ForeignKey('accounts.id'))
    country_id = Column(Integer, ForeignKey('countries.id'))
    parent_id = Column(String(20), ForeignKey('tweets.id'))
    country = relationship("Country")
    author = relationship("Account")
    tweet = relationship("Tweet")

    def __init__(self, content, location, retweet, favorite, happened_at, author, country, parent):
        self.content = content
        self.location = location
        self.retweet_count = retweet
        self.favorite_count = favorite
        self.happened_at = happened_at
        self.author_id = author
        self.country_id = country
        self.parent_id = parent
