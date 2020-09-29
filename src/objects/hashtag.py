from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from src.connection import Base

tweet_hashtag_association = Table('tweet_hashtag', Base.metadata,
                                  Column('hashtag_id', Integer, ForeignKey('hashtags.id')),
                                  Column('tweet_id', String(20), ForeignKey('tweets.id'))
                                  )

class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(Integer, primary_key=True)
    value = Column('value', String)
    tweets = relationship("Tweet", secondary=tweet_hashtag_association)

    def __init__(self, value):
        self.value = value