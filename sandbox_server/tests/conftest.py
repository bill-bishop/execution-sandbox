import os
import sys
import pytest

# Ensure the /sandbox parent is on sys.path so sandbox_server is a package
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from sandbox_server.app import app, socketio
from sandbox_server.models import db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

@pytest.fixture(scope="session")
def flask_client():
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="session")
def socket_client():
    client = socketio.test_client(app, namespace="/ws/workspace")
    yield client
    if client.is_connected():
        client.disconnect()