from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from src.connection import Base
from src.objects.tweet import tweet_hashtag_association


class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(Integer, primary_key=True)
    value = Column('value', String)
    tweet = relationship("Tweet", secondary=tweet_hashtag_association)

    # def __init__(self, value,tweet):
    #     self.value = value
    #     self.tweet = tweet

    def __init__(self, value):
        self.value = value
