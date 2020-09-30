import gzip
import json
import os
import sys
import jsonlines
from pathlib import Path
from src.connection import engine, Base, Session
from src.objects.account import Account
from src.objects.country import Country
from src.objects.hashtag import Hashtag
from src.objects.tweet import Tweet

# session = Session()


ROOT_DIR = sys.path[1]
path = Path(os.path.join(ROOT_DIR, 'data'))
temp_files = (file for file in path.iterdir() if file.name.endswith('jsonl'))

for file in temp_files:
    with jsonlines.open(file) as f:
        for item in f:
            # print(item)
            # tweet = Tweet
            print(item['created_at'])
# # session.commit()
# # session.close()
