import pymongo
import random
import sys

from elasticsearch import Elasticsearch
from bson.objectid import ObjectId

class mongoinit(object):

    URI = 'mongodb://localhost:27017/' #"mongodb://127.0.0.1:27017"

    @staticmethod
    def init():
        client = pymongo.MongoClient(mongoinit.URI)
        mongoinit.DATABASE = client['RecipeNLG']

    @staticmethod
    def insert(collection, data):
        mongoinit.DATABASE[collection].insert(data)
        
    @staticmethod
    def update_recipeNLG(collection, ref_id_doc, update_dic):
        mongoinit.DATABASE[collection].update({"_id":ref_id_doc},{"$set":update_dic})

    @staticmethod
    def find_one(collection, query):
        return mongoinit.DATABASE[collection].find_one(query)

    @staticmethod
    def find_similar(collection, query):
        return mongoinit.DATABASE[collection].find(query)

    @staticmethod
    def get_random_doc(collection):
        # coll refers to your collection
        count = mongoinit.DATABASE[collection].count()
        return mongoinit.DATABASE[collection].find()[random.randrange(count)]

    @staticmethod
    def get_last_doc(collection, ref_id_doc):
        report = mongoinit.DATABASE[collection].find_one(
            {'id_user': ref_id_doc},
            sort=[( '_id', pymongo.DESCENDING )])
        return report

    @staticmethod
    def update_one(collection, old_value, new_value):
        update_doc = mongoinit.DATABASE[collection].update_one(old_value, new_value)
        return update_doc

    def delete_one(collection, doc_id):
        delete_doc = mongoinit.DATABASE[collection].delete_one( {"_id": ObjectId(doc_id)})
        return delete_doc


class esinit(object):
    @staticmethod
    def init():
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=30) #, max_retries=10, retry_on_timeout=True
        if es.ping():
            print('Connected to ES')
        else:
            print('Could not connect to ES')
            sys.exit()

    @staticmethod
    def es_search(index, doc_type, titles, should_k):
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=30) #, max_retries=10, retry_on_timeout=True
        
        # body_all = {
        #     "query": {
        #         "bool" : {
        #         "must" : {
        #             "term" : { "titles" : titles }
        #         },
        #         "should" : [
        #             #{ "term" : { "titles" : titles } },
        #             { "term" : { "ingredients" : ingredients } },
        #         ],
        #         "minimum_should_match" : 1,
        #         "boost" : 1.0
        #         }
        #     }
        #     }

        # body_all = {
        #     "query": {
        #     "bool": {
        #             "must": {
        #                 "match": { "titles": titles }
        #     },
        #     "filter" : should_k,
        #        "minimum_should_match" : 1,
        #        "boost" : 1.0
        #         }
        #     }
        #     }

        body_all ={
            "query": {
                "bool": {
                "must": {
                    "bool" : { 
                    "should": should_k,
                    # [
                    #     { "match": { "title": "Elasticsearch" }},
                    #     { "match": { "title": "Solr" }} 
                    # ],
                    "must": { "match": { "titles": titles }} 
                    }
                },
                }
            }
            }

        res = es.search(index=index, doc_type=doc_type, body=body_all,size=1)
        return res

    @staticmethod
    def es_search_title(index, doc_type, keywords):
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=30) #, max_retries=10, retry_on_timeout=True
        body_title = {
            "query": {
                "multi_match": {
                    "query": keywords,
                    "fields": ["titles"]
                }
            }
        }
        res = es.search(index=index, doc_type=doc_type, body=body_title,size=1)
        return res

    @staticmethod
    def es_search_ing(index, doc_type, keywords):
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=30) #, max_retries=10, retry_on_timeout=True

        body_ing = {
            "query": {
                "multi_match": {
                    "query": keywords,
                    "fields": ["ingredients"]
                }
            }
        }
        res = es.search(index=index, doc_type=doc_type, body=body_ing,size=1)
        return res