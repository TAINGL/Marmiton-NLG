import sys
sys.path.append('/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/src/')

import pytest
import os

from src.app import create_app, db
from src.app import *
from src.app.models import UserModel
from src.settings import TestingConfig


filePath = '/Users/Johanna/Documents/SIMPLON DATA IA/TITRE PRO/PROJET CD/src/app/RecipeNLGTest.db'
if os.path.exists(filePath):
    os.remove(filePath)
    print('DB Test deleted!')
else:
    print("Can not delete the file as it doesn't exists")

@pytest.fixture(scope='module')
def new_user():
    user = UserModel('usertest1@gmail.com', 'FlaskIsAwesome')
    return user

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestingConfig)
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    #ctx.pop()

@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()
 
    # Insert user data
    user1 = UserModel(email='usertest1@gmail.com',username='Usertest1',plaintext_password='FlaskIsAwesome')
    user2 = UserModel(email='usertest2@gmail.com',username='Usertest2',plaintext_password='PaSsWoRd')
    #user1.set_password(plaintext_password='FlaskIsAwesome')
    #user2.set_password(plaintext_password='PaSsWoRd')
    db.session.add(user1)
    db.session.add(user2)
 
    # Commit the changes for the users
    db.session.commit()
 
    yield  # this is where the testing happens!
 
    db.drop_all()

@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(email='usertest1@gmail.com', password='FlaskIsAwesome'),
                     follow_redirects=True)

    yield  # this is where the testing happens!

    test_client.get('/logout', follow_redirects=True)
