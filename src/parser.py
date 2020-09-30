from datetime import datetime
import geoalchemy2
import gzip
import json
import os
import sys
import jsonlines
from pathlib import Path
from sqlalchemy import exists, func
from sqlalchemy.testing import db
from src.connection import engine, Base, Session
from src.objects.account import Account
from src.objects.country import Country
from src.objects.hashtag import Hashtag
from src.objects.tweet import Tweet


def parser_acc(line):
    account_id = line['user']['id']
    screen_name = line['user']['screen_name']
    name = line['user']['name']
    description = line['user']['description']
    followers_count = line['user']['followers_count']
    friends_count = line['user']['friends_count']
    statuses_count = line['user']['statuses_count']
    return Account(account_id, screen_name, name, description, followers_count, friends_count, statuses_count)


def parser_country(line):
    if line['place'] is not None:
        code = line['place']['country_code']
        name = line['place']['country']
        return Country(code, name)


def parser_tweet(line):
    id_str = line['id_str']
    content = line['full_text']

    location = None
    if line['coordinates'] is not None:
        location = func.ST_SetSRID(
            geoalchemy2.types.Geometry.ST_MakePoint(line['coordinates']['coordinates'][0], line['coordinates']['coordinates'][1]), 4326)

    retweet = line['retweet_count']
    favorite = line['favorite_count']

    happend_at = None
    if line['created_at'] is not None:
        happend_at = datetime.strptime(line['created_at'], '%a %b %d %X %z %Y')
        # print(happend_at)
    else:
        happend_at = None
    parent = None
    if line['retweeted']:
        parent = line['retweeted_status']['id']
    tweet_temp = Tweet
    return

ROOT_DIR = sys.path[1]
path = Path(os.path.join(ROOT_DIR, 'data'))
temp_files = (file for file in path.iterdir() if file.name.endswith('jsonl'))

list_of_accounts = {}
list_of_hashtags = {}
list_of_countries = {}
list_of_tweets = {}

for file, iterator in zip(temp_files, range(0, 4)):
    iterator = iterator + 1
    count = 0
    session = Session()
    print(file)

    with jsonlines.open(file) as f:

        for line in f:
            count = count + 1
            print(count)

            # Vytvorenie objektu Account
            user = parser_acc(line)
            list_of_accounts[user.id] = user

            # Vytvorenie objektu Hashtag
            hashtags = []
            hashtags = line['entities']['hashtags']
            for i in hashtags:
                temp_hash = Hashtag(i['text'])
                list_of_hashtags[temp_hash.value] = temp_hash

            # Vytvorenie objektu Country
            country_temp = parser_country(line)
            list_of_countries[country_temp.code] = country_temp

            # Vytvorenie objektu Tweet
            tweet_temp = parser_tweet(line)
            list_of_tweets[tweet_temp.id] = tweet_temp




        # session.bulk_save_objects(list(list_of_accounts.values()))
        # session.bulk_save_objects(list(list_of_hashtags.values()))
        # session.bulk_save_objects(list(list_of_countries.values()))

        print("account", sys.getsizeof(list(list_of_accounts.values())))
        print("account", sys.getsizeof(list(list_of_hashtags.values())))
        print("account", sys.getsizeof(list(list_of_countries.values())))

        #
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
        #
        # for i in hashtags:
        #     temp_hash = Hashtag(i['text'])
        #     if not session.query(exists().where(Hashtag.value == temp_hash.value)).scalar():
        #         session.add(temp_hash)
        #
        # if country_temp is not None:
        #     if not session.query(exists().where(Country.code == country_temp.code and Country.name == country_temp.name)).scalar():
        #         session.add(country_temp)

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
