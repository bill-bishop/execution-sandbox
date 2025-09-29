import re
import time
from sandbox_server.config import API_KEY


def test_websocket_receives_output(socket_client, flask_client):
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": "echo websocket-test", "pwd": "/sandbox"},
    )
    assert resp.status_code in (200, 401)

    time.sleep(0.5)
    received = socket_client.get_received("/ws/workspace")
    assert any(
        "websocket-test" in m["args"][0].get("line", "") for m in received if m["name"] == "event"
    )


def test_websocket_multiple_clients(flask_client, socket_client):
    from sandbox_server.app import socketio, app

    client2 = socketio.test_client(app, namespace="/ws/workspace")
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": "echo multicli", "pwd": "/sandbox"},
    )
    assert resp.status_code in (200, 401)
    time.sleep(0.5)

    msgs1 = socket_client.get_received("/ws/workspace")
    msgs2 = client2.get_received("/ws/workspace")
    assert any("multicli" in m["args"][0].get("line", "") for m in msgs1 if m["name"] == "event")
    assert any("multicli" in m["args"][0].get("line", "") for m in msgs2 if m["name"] == "event")
    client2.disconnect()


def test_websocket_preserves_ansi_sequences(flask_client, socket_client):
    # Run a command with ANSI output (red text)
    cmd = "echo -e '\033[31mREDTEST\033[0m'"
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": cmd, "pwd": "/sandbox"},
    )
    assert resp.status_code in (200, 401)

    time.sleep(0.5)
    received = socket_client.get_received("/ws/workspace")
    lines = [m["args"][0].get("line", "") for m in received if m["name"] == "event"]
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*m")

    # At least one line should contain a full ANSI sequence
    assert any(ansi_pattern.search(line) for line in lines), f"ANSI not preserved in lines: {lines}"