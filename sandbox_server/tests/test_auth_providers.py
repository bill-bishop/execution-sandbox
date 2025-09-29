import json

def test_auth_providers(flask_client):
    resp = flask_client.get("/auth/providers")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert set(["google","github","apple","facebook","discord"]).issubset(set(data))