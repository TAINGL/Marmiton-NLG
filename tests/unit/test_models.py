from src.app.models import UserModel
from src.app import db, login

class test_UserModel(UserMixin, db.Model):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    def test_create_user(username, password, email):
        assert user.username == 'usertest'
        assert user.password_hash != 'FlaskIsAwesome'
        assert user.email == 'usertest@gmail.com'
        assert db.session.add(user)
        assert db.session.commit()


    # assert user.set_password('FlaskIsAwesome')

    
    
