from geoalchemy2 import Geometry
from sqlalchemy import Column, ForeignKey, Integer, String, column, TIMESTAMP, BigInteger, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.connection import Base

tweet_hashtag_association = Table('tweet_hashtag', Base.metadata,
                                  Column('hashtag_id', Integer, ForeignKey('hashtags.id')),
                                  Column('tweet_id', String(20), ForeignKey('tweets.id'))
                                  )

tweet_mentions_association = Table('tweet_mentions', Base.metadata,
                                   Column('account_id', Integer, ForeignKey('accounts.id')),
                                   Column('tweet_id', String(20), ForeignKey('tweets.id'))
                                   )


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
    country = relationship("Country", back_populates="mobile_phone")
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


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    code = Column('code', String(2))
    name = Column('name', String(200))
    tweet = relationship("Tweet")

    def __init__(self, code, name):
        self.code = code
        self.name = name


class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(Integer, primary_key=True)
    value = Column('value', String)
    tweets = relationship("Tweet", secondary=tweet_hashtag_association)

    def __init__(self, value):
        self.value = value


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(BigInteger, primary_key=True)
    screen_name = Column('screen_name', String(200))
    name = Column('name', String(200))
    description = Column('description', String)
    followers_count = Column('followers_count', Integer)
    friends_count = Column('friends_count', Integer)
    statuses_count = Column('statuses_count', Integer)
    tweets = relationship("Tweet", secondary=tweet_mentions_association)

    def __init__(self, screen_name, name, description, followers_count, friends_count, statuses_count):
        self.screen_name = screen_name
        self.name = name
        self.description = description
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.statuses_count = statuses_count
