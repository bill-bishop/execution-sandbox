import os
from app import app

def test_read_file_valid_key():
    test_file = "/sandbox/test_read.txt"
    with open(test_file, "w") as f:
        f.write("Test content")

    client = app.test_client()
    headers = {"API-Key": "default-secret-key"}  # Valid API key
    response = client.get(f"/read?filename=test_read.txt", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("content") == "Test content"

    os.remove(test_file)

def test_read_file_invalid_key():
    client = app.test_client()
    headers = {"API-Key": "wrong-key"}  # Invalid API key
    response = client.get(f"/read?filename=test_read.txt", headers=headers)
    assert response.status_code == 401
    assert response.get_json().get("error") == "Unauthorized"