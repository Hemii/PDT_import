from src.connection import engine, Base,Session
from src.objects.account import Account
from src.objects.country import Country
from src.objects.hashtag import Hashtag
from src.objects.tweet import Tweet


session = Session()

# hashtag = Hashtag('fero')
# country = Country('US','United State')
# account = Account('5','bla','Blabko','Text',15,15,15)
# account1 = Account('6','blaaa','Blaaaabko','Teaaxt',1,1,1)
hashtag = session.query(Hashtag).filter(Hashtag.value == 'fero').scalar()
print(hashtag)
country = session.query(Country).filter(Country.code == 'US').scalar()
account = session.query(Account).filter(Account.id == 5).scalar()
account1 = session.query(Account).filter(Account.id == 6).scalar()

tweet = Tweet('545','text',None,56,65,None)

tweet.hashtags = [hashtag]
tweet.country = country
tweet.author = account
tweet.mentions = [account1]

session.add(tweet)

session.commit()
session.close()
