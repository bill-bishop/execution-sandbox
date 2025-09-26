import os
from sandbox_server import app
from sandbox_server import app

def test_write_file_valid_key():
    client = app.test_client()
    test_filename = "test_write.txt"
    test_content = "This is a test."

    headers = {"API-Key": "default-secret-key"}  # Valid API key
    response = client.post("/write", json={"filename": test_filename, "content": test_content}, headers=headers)
    assert response.status_code == 200
    assert response.get_json().get("status") == "success"

    file_path = f"/sandbox/{test_filename}"
    assert os.path.exists(file_path)
    with open(file_path, "r") as f:
        assert f.read() == test_content
    os.remove(file_path)

def test_write_file_invalid_key():
    client = app.test_client()
    test_filename = "test_write.txt"
    test_content = "This is a test."

    headers = {"API-Key": "wrong-key"}  # Invalid API key
    response = client.post("/write", json={"filename": test_filename, "content": test_content}, headers=headers)
    assert response.status_code == 401
    assert response.get_json().get("error") == "Unauthorized"