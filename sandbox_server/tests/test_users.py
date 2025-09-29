from sandbox_server.models import db, User, Workspace
from flask_jwt_extended import create_access_token


def test_user_and_workspace_creation(flask_client):
    app = flask_client.application
    with app.app_context():
        u = User(email="test@example.com", provider="dummy", provider_id="123")
        db.session.add(u)
        db.session.commit()
        ws = Workspace(user_id=u.id, container_url="http://workspace_1:8080")
        db.session.add(ws)
        db.session.commit()

        assert u.id > 0
        assert ws.user_id == u.id


def test_me_endpoint(flask_client):
    app = flask_client.application
    with app.app_context():
        u = User(email="me@example.com", provider="dummy", provider_id="999")
        db.session.add(u)
        db.session.commit()
        token = create_access_token(identity=str(u.id))

    resp = flask_client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["email"] == "me@example.com"


def test_auth_login_creates_user_and_workspace(flask_client):
    resp = flask_client.post("/auth/login")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data

    app = flask_client.application
    with app.app_context():
        u = User.query.filter_by(email="testuser@example.com").first()
        assert u is not None
        assert len(u.workspaces) == 1


def test_me_requires_jwt(flask_client):
    resp = flask_client.get("/me")
    assert resp.status_code == 401


def test_auth_login_idempotent(flask_client):
    flask_client.post("/auth/login")
    flask_client.post("/auth/login")

    app = flask_client.application
    with app.app_context():
        u = User.query.filter_by(email="testuser@example.com").first()
        assert u is not None
        assert len(u.workspaces) == 1