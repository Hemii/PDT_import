from datetime import datetime
import geoalchemy2
import gzip
import json
import os
import sys

import jsonlines
from pathlib import Path

from sqlalchemy import exists
from sqlalchemy.testing import db

from src.connection import engine, Base, Session
from src.objects.account import Account
from src.objects.country import Country
from src.objects.hashtag import Hashtag
from src.objects.tweet import Tweet




ROOT_DIR = sys.path[1]
path = Path(os.path.join(ROOT_DIR, 'data'))
temp_files = (file for file in path.iterdir() if file.name.endswith('jsonl'))

for file in temp_files:
    count = 0
    session = Session()
    print(file)
    with jsonlines.open(file) as f:

        for item in f:
            count = count + 1
            print(count)
            # print(item)

            # # Vytvorenie objektu Account
            # account_id = item['user']['id']
            # screen_name = item['user']['screen_name']
            # name = item['user']['name']
            # description = item['user']['description']
            # followers_count = item['user']['followers_count']
            # friends_count = item['user']['friends_count']
            # statuses_count = item['user']['statuses_count']
            # user = Account(account_id, screen_name, name, description, followers_count, friends_count, statuses_count)

            # Vytvorenie objektu Hashtag
            hashtags = []
            hashtags = item['entities']['hashtags']


            # Vytvorenie objektu Country
            country_temp = None
            if item['place'] is not None:
                code = item['place']['country_code']
                name = item['place']['country']
                country_temp = Country(code,name)
                # print(code, name)


            # Vytvorenie objektu Tweet
            # id_str = item['id_str']
            # content = item['full_text']

            # location = None
            # if item['coordinates'] is not None:
            #     location = ST_SetSRID(ST_MakePoint(item['coordinates']['coordinates'][0],item['coordinates']['coordinates'][1]),4326)

            # retweet = item['retweet_count']
            # favorite = item['favorite_count']
            #
            # happend_at = None
            # if item['created_at'] is not None:
            #     happend_at = datetime.strptime(item['created_at'], '%a %b %d %X %z %Y')
            #     # print(happend_at)
            # else:
            #     happend_at = None
            # parent = None
            # if item['retweeted']:
            #     parent = item['retweeted_status']['id']

            #
            #
            # session = Session()

            # if session.query(exists().where(Account.id == user.id)).scalar():
            #     temp_account = Account.query.filter_by(id=Account.id).first()
            #     if
            # else:
            #     session.add(user)

            #
            # if not session.query(exists().where(Account.id == user.id)).scalar():
            #     session.add(user)
            # else:
            #     session.query(Account).filter(Account.id == user.id).update({Account.name: user.name })
            #     print("rovnaky user")

            for i in hashtags:
                temp_hash = Hashtag(i['text'])
                if not session.query(exists().where(Hashtag.value == temp_hash.value)).scalar():
                    session.add(temp_hash)

            if country_temp is not None:
                if not session.query(exists().where(Country.code == country_temp.code and Country.name == country_temp.name)).scalar():
                    session.add(country_temp)

            # if not session.query(exists().where(Tweet.id == Tweet.id)).scalar():
            #     obj_tweet = Tweet(id_str,
            #                       content,
            #                       location,
            #                       retweet,
            #                       favorite,
            #                       happend_at,
            #                       user.id,
            #                       None,
            #                       parent,
            #                       None,
            #                       None,
            #                       None,
            #                       user,
            #                       None)
            #     session.add(user)


            session.commit()
    session.close()
# session = Session()
# country = Country('US','United')
# session.add(country)
# country = Country('SK','Slovakia')
# session.add(country)
# #
# # if not session.query(exists().where(Country.code == country.code)).scalar():
# #     session.add(country)
# # else:
# #     session.query(Country).filter(Country.code == country.code).update({Country.name: country.name, Country.code: 'BL'})
# #
# session.commit()
# session.close()
