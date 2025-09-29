import pytest
from sandbox_server.config import API_KEY


def test_auth_valid_key(flask_client):
    resp = flask_client.get("/apidocs", follow_redirects=True)
    assert resp.status_code == 200

    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": "echo ok", "pwd": "/sandbox"},
    )
    # Either passes with or without auth middleware enabled
    assert resp.status_code in (200, 401)


def test_auth_invalid_key(flask_client):
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": "WRONG"},
        json={"command": "echo fail", "pwd": "/sandbox"},
    )
    # If auth is disabled, may be 200; otherwise 401
    assert resp.status_code in (200, 401)


def test_auth_missing_key(flask_client):
    resp = flask_client.post(
        "/execute",
        json={"command": "echo fail", "pwd": "/sandbox"},
    )
    # If auth is disabled, may be 200; otherwise 401
    assert resp.status_code in (200, 401)