
def test_athome(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Salut!" in response.data

def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(email='usertest1@gmail.com', passwd='FlaskIsAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    #assert b"Salut {{ current_user.username }} !" in response.data

def login(test_client, email, password):
    """Login helper function"""
    return test_client.post(
        "/login",
        data=dict(email=email, password=password),
        follow_redirects=True,
    )

def logout(test_client):
    """Logout helper function"""
    return test_client.get("/logout", follow_redirects=True)

def test_login_logout(test_client):
    """Test login and logout using helper functions"""
    rv = login(test_client, email='usertest1@gmail.com', password='FlaskIsAwesome')
    assert b"You were logged in" in rv.data
    rv = logout(test_client)
    assert b"You were logged out" in rv.data
    rv = login(test_client, email='usertest3@gmail.com', password='FlaskIsAwesome')
    assert b"Invalid username" in rv.data
    rv = login(test_client, email='usertest1@gmail.com', passwd='FlaskIsAwesome' + "x")
    assert b"Invalid password" in rv.data






