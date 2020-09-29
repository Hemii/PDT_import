from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, BigInteger
from sqlalchemy.orm import relationship
from src.connection import Base

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    code = Column('code', String(2))
    name = Column('name', String(200))
    tweet = relationship("Tweet")

    def __init__(self, code, name):
        self.code = code
        self.name = name