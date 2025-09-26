import pytest
from sandbox_server import app
from sandbox_server.config import API_KEY


def test_execute_replaces_async():
    """Verify that /execute works as the unified replacement for async execution."""
    flask_client = app.test_client()
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": "echo Hello Unified", "pwd": "/sandbox"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "Hello Unified" in data["stdout"]