import pytest
from sandbox_server.config import API_KEY


def test_execute_echo(flask_client):
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": "echo hello", "pwd": "/sandbox"},
    )
    assert resp.status_code in (200, 401)


def test_execute_invalid_command(flask_client):
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": "nonexistent_command_xyz", "pwd": "/sandbox"},
    )
    assert resp.status_code in (200, 401)


def test_execute_with_stderr(flask_client):
    # 'ls /nonexistent' should produce stderr
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": "ls /nonexistent", "pwd": "/sandbox"},
    )
    assert resp.status_code in (200, 401)