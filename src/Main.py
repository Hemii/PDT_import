from datetime import date
from src.connection import engine, Base,Session
from src.objects.country import Country
from src.objects.tweet import Tweet
from src.objects.account import Account
from src.objects.hashtag import Hashtag

# Base.metadata.create_all(engine)

session = Session()

Hashtag = Hashtag("Fero")


session.add(Hashtag)

session.commit()
session.close()