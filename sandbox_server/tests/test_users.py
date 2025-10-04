import pytest
from flask_jwt_extended import create_access_token
from sandbox_server.models import db, User

@pytest.mark.usefixtures("flask_client")
def test_me_requires_jwt(flask_client):
    resp = flask_client.get("/auth/me")
    assert resp.status_code == 401

@pytest.mark.usefixtures("flask_client")
def test_me_endpoint(flask_client):
    app = flask_client.application
    with app.app_context():
        u = User(email="me@example.com", provider="dummy", provider_id="999")
        db.session.add(u)
        db.session.commit()
        token = create_access_token(identity=str(u.id))

    # Use cookie-based JWT to match production behavior
    flask_client.set_cookie("/", "auth_token", token)

    resp = flask_client.get("/auth/me")
    assert resp.status_code == 200