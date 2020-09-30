from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Table
from sqlalchemy.orm import relationship
from src.connection import Base
from src.objects.tweet import tweet_mentions_association




class Account(Base):
    __tablename__ = 'accounts'

    id = Column(BigInteger, primary_key=True)
    screen_name = Column('screen_name', String(200))
    name = Column('name', String(200))
    description = Column('description', String)
    followers_count = Column('followers_count', Integer)
    friends_count = Column('friends_count', Integer)
    statuses_count = Column('statuses_count', Integer)
    tweet = relationship("Tweet", secondary=tweet_mentions_association)

    def __init__(self, id, screen_name, name, description, followers_count, friends_count, statuses_count):
        self.id = id
        self.screen_name = screen_name
        self.name = name
        self.description = description
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.statuses_count = statuses_count

    # def __init__(self, id, screen_name, name, description, followers_count, friends_count, statuses_count, tweet):
    #     self.id = id
    #     self.screen_name = screen_name
    #     self.name = name
    #     self.description = description
    #     self.followers_count = followers_count
    #     self.friends_count = friends_count
    #     self.statuses_count = statuses_count
    #     self.tweet = tweet
