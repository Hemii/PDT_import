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

    def __init__(self, id, screen_name, name, description=None, followers_count=None, friends_count=None,
                 statuses_count=None):
        self.id = id
        self.screen_name = screen_name
        self.name = name
        self.description = description
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.statuses_count = statuses_count

    def __str__(self):
        return f"id: {self.id}\nscreen_name: {self.screen_name}\nname: {self.name}\ndescription: {self.description}\nfollowers_count: {self.followers_count}\nfriends_count: {self.friends_count}\nstatuses_count: {self.statuses_count}\n"

    def __repr__(self):
        return str(self)
