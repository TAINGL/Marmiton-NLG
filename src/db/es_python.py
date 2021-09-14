# https://stackoverflow.com/questions/28675162/how-do-you-add-multiple-json-files-to-elasticsearch

import json
import sys
import os
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.helpers import bulk

# connect to ES on localhost on port 9200
es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=30)
if es.ping():
    print('Connected to ES')
else:
    print('Could not connect to ES')
    sys.exit()

## create index of recipe
df = pd.read_json (r"/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/marmiton_to_mongo.json")
data = df.T
data["id"] = data.index + 1
print(data.tail(10))
print(data.shape)

df_1 = data.iloc[:20750,:]
df_2 = data.iloc[20752:,:]
print("Shape of new dataframes - {} , {}".format(df_1.shape, df_2.shape)) # problem with row 20751

frames = [df_1, df_2]
df = pd.concat(frames)

df_test_1 = data.iloc[:6238,:]
df_test_2 = data.iloc[6239:12476,:]
df_test_3 = data.iloc[12477:18714,:]
df_test_4 = data.iloc[18714:,:]

# data = df_test_1.to_json('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/test/df_test_1.json',orient='records')
# data = df_test_2.to_json('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/test/df_test_2.json',orient='records')
# data = df_test_3.to_json('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/test/df_test_3.json',orient='records')
# data = df_test_4.to_json('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/test/df_test_4.json',orient='records')

# print('ok')

es_client = Elasticsearch(http_compress=True)


use_these_keys = ['id', 'titles', 'NER', 'instructions']
def filterKeys(document):
    return {key: document[key] for key in use_these_keys }

def doc_generator(file):
    f = open(file)
    data = json.load(f)
    for doc in data:
        # print(doc['id'])
        # print(doc)
        yield {
                "_index": 'recipe',
                "_type": "_doc",
                "_id" : doc['id'],
                "_source": doc,
            }

path = ['/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/test/df_test_1.json',
        '/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/test/df_test_2.json',
        '/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/test/df_test_3.json',
        '/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/test/df_test_4.json']

# helpers.bulk(es_client, doc_generator('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/test/df_test_4.json'))
res = es.count(index="recipe", doc_type="_doc")["count"]
print(res)