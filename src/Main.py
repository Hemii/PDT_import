from src.connection import engine, Base,Session
from src.objects.account import Account
from src.objects.country import Country
from src.objects.hashtag import Hashtag
from src.objects.tweet import Tweet


session = Session()

hashtag = Hashtag('fero')


session.add(hashtag)

session.commit()
session.close()