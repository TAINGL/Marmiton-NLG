# TO DO
import json
import logging
from pprint import pprint
from time import sleep

import requests
from elasticsearch import Elasticsearch


def search(es_object, index_name, search):
    res = es_object.search(index=index_name, body=search)
    pprint(res)


def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "recette": {
                "dynamic": "strict",
                "properties": {
                    "titles": {
                        "type": "text"}
                    },
                    "total times": {
                        "type": "integer"
                    },
                    "yields": {
                        "type": "text"
                    },
                    "ingredients": {
                        "type": "nested",
                        "properties": {
                            "step": {"type": "text"}
                            }
                        },
                    "instructions": {
                        "type": "text"
                    },
                    "images": {
                        "type": "text"
                    },
                    "host": {
                        "type": "text"
                    },
                    "links": {
                        "type": "text"
                    },
                    "ner": {
                        "type": "nested",
                        "properties": {
                            "step": {"type": "text"}
                    }
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    is_stored = True
    try:
        outcome = elastic_object.index(index=index_name, doc_type='salads', body=record)
        print(outcome)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
        is_stored = False
    finally:
        return is_stored


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connected')
    else:
        print('Awww it could not connect!')
    return _es


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

  
    # Opening JSON file
    with open('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/marmiton_ner.json') as json_file:
        result = json.load(json_file)

    es = connect_elasticsearch()
    if es is not None:
        if create_index(es, 'recipes'):
            out = store_record(es, 'recipes', result)
            print('Data indexed successfully')

    es = connect_elasticsearch()
    if es is not None:
        # search_object = {'query': {'match': {'calories': '102'}}}
        # search_object = {'_source': ['title'], 'query': {'match': {'calories': '102'}}}
        search_object = {'_source': ['title'], 'query': {'range': {'total times': {'gte': 20}}}}
        search(es, 'recipes', json.dumps(search_object))


