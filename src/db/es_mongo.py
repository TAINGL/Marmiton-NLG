# TO DO
# simplernerd.com/migrate-mongo elasticsearch

from pymongo import MongoClient
from elasticsearch import Elasticsearch
import os

# Mongo Config
client = MongoClient('hostname', 27017)
db = client.RecipeNLG
collection = db.recipe
#client = MongoClient(os.environ['MONGO_URI'])
#db = client[os.environ['MONGO_DB']]
#collection = db[os.environ['MONGO_COLLECTION']]

# Elasticsearch Config
es_host = 'http://127.0.0.1:9200'
es = Elasticsearch([es_host])
es_index = 'recipe'
#es_host = os.environ['ELASTICSEARCH_URI']
#es = Elasticsearch([es_host])
#es_index = os.environ['ELASTICSEARCH_INDEX']

from elasticsearch import helpers
import json

def migrate():
  res = collection.find()
  # number of docs to migrate
  num_docs = 24955
  actions = []
  for i in range(num_docs):
      doc = res[i]
      mongo_id = doc['_id']
      doc.pop('_id', None)
      actions.append({
          "_index": es_index,
          "_id": mongo_id,
          "_source": json.dumps(doc)
      })
  helpers.bulk(es, actions)

migrate()
print("it's done")  