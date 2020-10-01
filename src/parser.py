from datetime import datetime
import geoalchemy2
import gzip
import json
import os
import sys
import jsonlines
from pathlib import Path

from geoalchemy2 import WKTElement
from sqlalchemy import exists, func
from sqlalchemy.testing import db
from src.connection import engine, Base, Session
from src.objects.account import Account
from src.objects.country import Country
from src.objects.hashtag import Hashtag
from src.objects.tweet import Tweet





ROOT_DIR = sys.path[1]
path = Path(os.path.join(ROOT_DIR, 'data'))
temp_files = (file for file in path.iterdir() if file.name.endswith('jsonl'))

hashmap_accounts = {}
hashmap_hashtags = {}
hashmap_countries = {}
hashmap_tweets = {}

ROOT_DIR = sys.path[1]
path = Path(os.path.join(ROOT_DIR, 'test'))

session = Session()
hashmap_accounts = {}
hashmap_hashtags = {}
hashmap_countries = {}
hashmap_tweets = {}


def file_parser():
    files_for_parsing = (f for f in path.iterdir() if f.name.endswith('jsonl'))
    count = 0
    for file in files_for_parsing:
        with jsonlines.open(file) as f:
            for tweet in f:
                count = count + 1
                print(count)
                pars_tweet(tweet)
            session.commit()

def pars_tweet(tweet):
    tweet_id = tweet['id_str']

    if not tweet_id in hashmap_tweets:

        tweet_parent = None
        if 'retweeted_status' in tweet and tweet['retweeted_status'] is not None :

            tweet_parent = pars_tweet(tweet['retweeted_status'])

        tweet_location = None
        if tweet['coordinates'] is not None:
            tweet_location = WKTElement(
                f"POINT({tweet['coordinates']['coordinates'][0]} {tweet['coordinates']['coordinates'][1]})", srid=4326)

        created_tweet = Tweet(
            tweet_id,
            tweet['full_text'],
            tweet_location,
            tweet['retweet_count'],
            tweet['favorite_count'],
            tweet['created_at']
        )

        hashmap_tweets[created_tweet.id] = True

        if tweet['user'] is not None:
            mentioned_user_id = tweet['user']['id']
            if not mentioned_user_id in hashmap_accounts:
                account = Account(mentioned_user_id, tweet['user']['screen_name'], tweet['user']['name'],
                                  tweet['user']['description'], tweet['user']['followers_count'],
                                  tweet['user']['friends_count'], tweet['user']['statuses_count'])
                hashmap_accounts[mentioned_user_id] = 1

            else:
                account = session.query(Account).filter(Account.id == mentioned_user_id).scalar()

                if hashmap_accounts[mentioned_user_id] == 0:
                    hashmap_accounts[mentioned_user_id] = 1
                    account.description = tweet['user']['description']
                    account.followers_count = tweet['user']['followers_count']
                    account.friends_count = tweet['user']['friends_count']
                    account.statuses_count = tweet['user']['statuses_count']

            created_tweet.author = account

        if tweet['place'] is not None:
            place_code = tweet['place']['country_code']
            if not place_code in hashmap_countries:
                country = Country(place_code, tweet['place']['country'])
                hashmap_countries[place_code] = True

            else:
                country = session.query(Country).filter(Country.code == place_code).scalar()

            created_tweet.country = country

        if tweet['entities'] is not None and tweet['entities']['hashtags'] is not None:
            array_hashtags = []
            array_hashtags_ids = []
            for hashtag in tweet['entities']['hashtags']:

                hashtag_text = hashtag['text']

                if  hashtag_text in array_hashtags_ids:
                    continue

                if not hashtag_text in hashmap_hashtags:
                    hashmap_hashtags[hashtag_text] = True
                    created_hashtag = Hashtag(hashtag_text)
                    array_hashtags_ids.append(created_hashtag.value)
                else:
                    created_hashtag = session.query(Hashtag).filter(Hashtag.value == hashtag_text).scalar()

                array_hashtags.append(created_hashtag)

            created_tweet.hashtags = array_hashtags

        if tweet['entities'] is not None and tweet['entities']['user_mentions'] is not None:

            array_mentions = []
            array_mentions_ids = []

            for mentioned_user in tweet['entities']['user_mentions']:

                mentioned_user_id = mentioned_user['id']


                if (mentioned_user_id in array_mentions_ids or mentioned_user_id == created_tweet.author.id):
                    continue

                if not mentioned_user_id in hashmap_accounts:
                    account = Account(
                       mentioned_user['id'],
                       mentioned_user['screen_name'],
                       mentioned_user['name'],
                    )
                    hashmap_accounts[mentioned_user_id] = 0
                    array_mentions_ids.append(mentioned_user_id)
                else:
                    account = session.query(Account).filter(Account.id == mentioned_user_id).scalar()

                array_mentions.append(account)

            created_tweet.mentions = array_mentions

        # if tweet['entities'] is not None and tweet['entities']['user_mentions'] is not None:
        #     array_mentions = []
        #     array_mentions_ids = []
        #     for mention_user in tweet['entities']['user_mentions']:
        #         mention_user_id = mention_user['id']
        #
        #
        #         if mention_user_id == tweet['user']['id'] or mention_user_id in array_mentions_ids:
        #             continue
        #
        #         # print(hashmap_accounts[mention_user_id])
        #
        #         if not mention_user_id in hashmap_accounts :
        #             account = Account(user_id, mention_user['screen_name'], mention_user['name'])
        #             hashmap_accounts[mention_user_id] = 0
        #             array_mentions_ids.append(account.id)
        #         else:
        #             account = session.query(Account).filter(Account.id == mention_user_id).scalar()
        #         array_mentions.append(account)
        #
        #     print(array_mentions)
        #     created_tweet.mentions = array_mentions

        created_tweet.tweet = tweet_parent
        session.add(created_tweet)
        return created_tweet




file_parser()

session.close()
