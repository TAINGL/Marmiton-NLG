from flask_login import LoginManager
from src.app.models import UserModel

"""
This file (test_users.py) contains the functional tests for the `users` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the `users` blueprint.
"""

def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Connexion' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='usertest1@gmail.com', password='FlaskIsAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Salut Usertest1 !' in response.data
    assert b'RecipeNLG' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data

    # assert b'You should be redirected automatically to target URL: ' in response.data
    # print(response.data)

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert b'Logout' not in response.data
    assert b'Connexion' in response.data
    assert b'Login' in response.data
    # print(response.data)


def test_invalid_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='usertest1@gmail.com', password='FlaskIsNotAwesome'),
                                follow_redirects=True)
    assert response.status_code == 400
    assert b'Logout' not in response.data
    assert b'Connexion' in response.data
    assert b'Login' in response.data
    # assert b'Entrer le titre de la recette' in response.data
    # print(response.data)


def test_login_already_logged_in(test_client, init_database, login_default_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST) when the user is already logged in
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login',
                                data=dict(email='usertest1@gmail.com', password='FlaskIsAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Salut Usertest1 !' in response.data
    assert b'RecipeNLG' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data


    response = test_client.post('/login',
                                data=dict(email='usertest1@gmail.com', password='FlaskIsAwesome'),
                                follow_redirects=True)    
    assert b'Salut Usertest1 !' in response.data
    assert b'RecipeNLG' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data


def test_valid_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/signup',
                                data=dict(username='Usertest3',
                                          email='usertest3@yahoo.com',
                                          password='FlaskIsGreat',
                                          confirm='FlaskIsGreat'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Salut Usertest3 !' in response.data
    assert b'RecipeNLG' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data

    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' not in response.data
    assert b'Connexion' in response.data
    assert b'Login' in response.data


def test_invalid_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to with invalid credentials (POST)
    THEN check an error message is returned to the user
    """
    response = test_client.post('/signup',
                                data=dict(username='Usertest4',
                                          email='usertest4@hotmail.com',
                                          password='FlaskIsGreat',
                                          confirm='FlskIsGreat'),   # Does NOT match!
                                follow_redirects=True)
    assert response.status_code == 400
    assert b'[Field must be equal to password.]' in response.data
    assert b'Inscription' in response.data
    assert b'Register' in response.data

def test_duplicate_registration(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST) using an email address already registered
    THEN check an error message is returned to the user
    """
    # Register the new account
    response = test_client.post('/signup',
                     data=dict(username='Usertest5',
                               email='usertest5@hey.com',
                               password='FlaskIsTheBest',
                               confirm='FlaskIsTheBest'),
                     follow_redirects=True)
    assert response.status_code == 200
    assert b'Salut Usertest5 !' in response.data
    assert b'RecipeNLG' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data

    # Logout the new account session
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' not in response.data
    assert b'Connexion' in response.data
    assert b'Login' in response.data 
                     
    # Try registering with the same email address
    response = test_client.post('/signup',
                                data=dict(username='Usertest5',
                                          email='usertest5@hey.com',
                                          password='FlaskIsStillTheBest',
                                          confirm='FlaskIsStillTheBest'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'This member already exists!' in response.data
    assert b'Click here to register' in response.data
    assert b'Click here to login' in response.data

