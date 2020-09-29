from datetime import date
from src.connection import engine, Base
from src.objects import Tweet,Account,Hashtag,Country

Base.metadata.create_all(engine)

