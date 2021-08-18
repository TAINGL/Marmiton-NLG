import pymongo
import random

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
