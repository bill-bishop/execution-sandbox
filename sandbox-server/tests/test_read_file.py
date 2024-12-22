import os
from app import app

def test_read_file():
    # Create a temporary file for testing
    test_file = "/sandbox/test_read.txt"
    with open(test_file, "w") as f:
        f.write("Test content")

    client = app.test_client()
    response = client.get(f"/read?filename=test_read.txt")
    
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("content") == "Test content"

    # Clean up
    os.remove(test_file)