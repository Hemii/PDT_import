from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, BigInteger, Table
from sqlalchemy.orm import relationship
from src.connection import Base
from geoalchemy2 import Geometry

tweet_hashtag_association = Table('tweet_hashtag', Base.metadata,
                                  Column('hashtag_id', Integer, ForeignKey('hashtags.id')),
                                  Column('tweet_id', String(20), ForeignKey('tweets.id'))
                                  )

tweet_mentions_association = Table('tweet_mentions', Base.metadata,
                                   Column('account_id', BigInteger, ForeignKey('accounts.id')),
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

    author = relationship("Account")
    country = relationship("Country")
    tweet = relationship("Tweet", remote_side=[id])
    hashtags = relationship("Hashtag", secondary=tweet_hashtag_association)
    mentions = relationship("Account", secondary=tweet_mentions_association)

    def __init__(self,id, content, location, retweet, favorite, happened_at):
        self.id = id
        self.content = content
        self.location = location
        self.retweet_count = retweet
        self.favorite_count = favorite
        self.happened_at = happened_at






