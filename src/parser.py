import gzip
import json
# from src.objects import *

with gzip.open('coronavirus-tweet-id-2020-08-01-06.jsonl.gz', 'r') as json_file:
    json_list = list(json_file)

for json_str in json_list:
    result = json.loads(json_str.decode('utf-8'))
    print("result: {}".format(result))
    print(isinstance(result, dict))