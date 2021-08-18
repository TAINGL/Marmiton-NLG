from pymongo import MongoClient
from pymongo import ReturnDocument
from bson.objectid import ObjectId

import sys
sys.path.insert(0, '../scr/')
from config import MongodbConfig
sys.path.insert(0, '../utils/')
from split_csv import get_csv_file



from os import listdir
from os.path import isfile, join

import pymongo
import pandas as pd
import json

# If you work on local mongo compass write "local", 
# and if you work on mongo atlas write "altas" in MongodbConfig
URI = MongodbConfig("atlas")
client = pymongo.MongoClient(URI)

# Create Database if it's not already created
for database_name in client.list_database_names():  
    print("Database - "+database_name)
    
    if "marmiton" in database_name:
        print("The database exists.")
    else:
        db = client.marmiton
        print('The database is created.')
        
# Create collection in your database if it's not already created
for collection_name in client.get_database(database_name).list_collection_names():  
    print(collection_name)

    #collection_list = ['aperitif', 'boisson', 'dessert', 'entree', 'plat']
    collection_list = ['aperitif']
    
    for collection in collection_list:

        if collection in database_name:
            print("The collection exists.")
        else:
            collection = db.collection
            print('The collection is created.')


file_csv = get_csv_file('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/data/csv_split', '.csv')
print('file_csv', file_csv)
for f_csv in file_csv:
    data = pd.read_csv(f_csv)
    file_data = json.loads(data.to_json(orient='records'))
        
    # Inserting the loaded data in the Collection
    # if JSON contains data more than one entry
    # insert_many is used else inser_one is used
    if isinstance(file_data, list):
        collection.insert_many(file_data)  
        print("Json File inserted!" )
    else:
        collection.insert_one(file_data)