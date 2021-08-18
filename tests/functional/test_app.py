import pytest

from src.app import create_app, db
from src.models import UserModel


@pytest.fixture
def client():
    # Prepare before your test
    flaskr.app.config["TESTING"] = True
    with flaskr.app.test_client() as client:
        # Give control to your test
        yield client

def test_square(client):
    rv = client.get("/square?number=8")
    assert b"64" == rv.data