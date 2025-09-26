import pytest
from sandbox_server import app, socketio
from sandbox_server.config import API_KEY


@pytest.fixture(scope="module")
def test_client():
    client = socketio.test_client(app, namespace="/ws/workspace")
    yield client
    if client.is_connected():
        client.disconnect()


def test_execute_command_emits_websocket(test_client):
    """Running /execute should emit stdout events over WebSocket."""
    flask_client = app.test_client()
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": "echo hello", "pwd": "/sandbox"},
    )
    assert resp.status_code == 200
    messages = test_client.get_received("/ws/workspace")
    assert any("hello" in m["args"][0].get("line", "") for m in messages if "line" in m["args"][0])


def test_execute_command_error_emits_output(test_client):
    """Errors from /execute should also emit events (merged stream)."""
    flask_client = app.test_client()
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": "nonexistent_command", "pwd": "/sandbox"},
    )
    assert resp.status_code != 500  # even with error, server should handle gracefully
    messages = test_client.get_received("/ws/workspace")
    assert any(m["args"][0].get("line") for m in messages if "line" in m["args"][0])


def test_websocket_event_structure(test_client):
    """All emitted events should include the correct fields depending on type."""
    flask_client = app.test_client()
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": "echo structured", "pwd": "/sandbox"},
    )
    assert resp.status_code == 200
    messages = test_client.get_received("/ws/workspace")
    assert messages, "No messages received from WebSocket"

    for msg in messages:
        event = msg["args"][0]
        if event["type"] == "command":
            for field in ["seq_id", "type", "command"]:
                assert field in event
        elif event["type"] == "output":
            for field in ["seq_id", "type", "command", "stream", "line"]:
                assert field in event