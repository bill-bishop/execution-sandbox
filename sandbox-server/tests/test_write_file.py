import os
from app import app

def test_write_file():
    client = app.test_client()
    test_filename = "test_write.txt"
    test_content = "This is a test."

    response = client.post("/write", json={"filename": test_filename, "content": test_content})
    
    assert response.status_code == 200
    assert response.get_json().get("status") == "success"

    # Verify the file was written
    file_path = f"/sandbox/{test_filename}"
    assert os.path.exists(file_path)
    with open(file_path, "r") as f:
        assert f.read() == test_content

    # Clean up
    os.remove(file_path)