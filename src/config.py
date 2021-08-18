# import configparser

import os
import configparser

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '12414f2aec219ca80b7e7e8f6b105f0a'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ##### Flask-Mail configurations #####
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'tainglaura.contact@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or  \
        'sqlite:///RecipeNLG.db'
    

class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
        'sqlite:///RecipeNLG.db'    

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or  \
        'sqlite:///RecipeNLG.db'

class atlas:
    DB_ADMIN = 'Recipe_user'
    DB_PASS = 'nsTM1cebYyLJW46U'
    DB_CLUSTER = 'cluster0.qkqbq.mongodb.net/test?retryWrites=true&w=majority'

class localdb:
    DB_HOST = 'localhost'
    DB_PORT = 27017
    DB_NAME = 'RecipeNLG'

class MongodbConfig(atlas):
    URI = 'mongodb+srv://Recipe_user:nsTM1cebYyLJW46U@cluster0.qkqbq.mongodb.net/test?retryWrites=true&w=majority'

class MongodbConfig(localdb):
    URI = 'mongodb://localhost:27017/RecipeNLG'
    #URI = 'mongodb://{}:{}/{}'.format(DB_HOST, DB_PORT,DB_NAME)

class EsConfig():
    ELASTICSEARCH_URL = 'http://localhost:9200' # os.environ.get('ELASTICSEARCH_URL') 
    


