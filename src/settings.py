# https://www.askpython.com/python/python-dotenv-module

## importing the load_dotenv from the python-dotenv module
from dotenv import load_dotenv
 
## using existing module to specify location of the .env file
from pathlib import Path
import os

import sys
import uuid
 
app_dir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
 
# retrieving keys and adding them to the project
# from the .env file through their key names
SECRET_KEY = os.getenv("SECRET_KEY")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
ADMIN_ACCESS = os.getenv('ADMIN_ACCESS')

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ##### Flask-Mail configurations #####
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME') 
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') 
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEVELOPMENT_DATABASE_URI')
    LOGIN_DISABLED = False
    

class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TESTING_DATABASE_URI')
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False
    #SESSION_COOKIE_SECURE = False
    

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('PRODUCTION_DATABASE_URI')

class atlas:
    DB_ADMIN = os.getenv('DB_ADMIN')
    DB_PASS = os.getenv('DB_PASS')
    DB_CLUSTER = os.getenv('DB_CLUSTER')

class localdb:
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

class MongodbConfig(atlas):
    URI = 'mongodb+srv://Recipe_user:nsTM1cebYyLJW46U@cluster0.qkqbq.mongodb.net/test?retryWrites=true&w=majority'

class MongodbConfig(localdb):
    URI = 'mongodb://localhost:27017/RecipeNLG'

class EsConfig():
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')