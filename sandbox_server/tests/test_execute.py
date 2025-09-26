import os
from sandbox_server import app

def test_execute_valid_key():
    client = app.test_client()
    headers = {"API-Key": "default-secret-key"}  # Valid API key
    response = client.post("/execute/worker", json={"command": "echo Hello World"}, headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert "Hello World" in data.get("stdout", "")

def test_execute_invalid_key():
    client = app.test_client()
    headers = {"API-Key": "wrong-key"}  # Invalid API key
    response = client.post("/execute/worker", json={"command": "echo Hello World"}, headers=headers)
    assert response.status_code == 401
    assert response.get_json().get("error") == "Unauthorized"