import os
from sandbox_server import app

def test_valid_api_key():
    client = app.test_client()
    headers = {"API-Key": "default-secret-key"}  # Matches config.py
    response = client.get("/read?filename=test_read.txt", headers=headers)
    assert response.status_code in [200, 404]  # File may not exist, but should be authorized

def test_invalid_api_key():
    client = app.test_client()
    headers = {"API-Key": "wrong-key"}
    response = client.get("/read?filename=test_read.txt", headers=headers)
    assert response.status_code == 401
    assert response.get_json().get("error") == "Unauthorized"