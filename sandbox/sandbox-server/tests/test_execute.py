import json
from app import app

def test_execute():
    client = app.test_client()
    response = client.post("/execute", json={"command": "echo Hello World"})
    
    assert response.status_code == 200
    data = response.get_json()
    assert "Hello World" in data.get("stdout", "")