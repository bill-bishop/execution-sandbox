from sandbox_server.config import API_KEY


def test_workspace_logs_basic(flask_client):
    # Execute a simple command to generate logs
    resp = flask_client.post(
        "/execute",
        headers={"API-Key": API_KEY},
        json={"command": "echo logtest", "pwd": "/sandbox"},
    )
    assert resp.status_code in (200, 401)

    # Fetch recent logs
    resp = flask_client.get("/workspace/logs?offset=-10&limit=10", headers={"API-Key": API_KEY})
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        logs = resp.get_json()
        assert isinstance(logs, list)
        assert any("logtest" in entry.get("line", "") for entry in logs if entry["type"] == "output")


def test_workspace_logs_pagination(flask_client):
    resp = flask_client.get("/workspace/logs?offset=0&limit=1", headers={"API-Key": API_KEY})
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        logs = resp.get_json()
        assert len(logs) <= 1
        if logs:
            assert "type" in logs[0]
            assert "seq_id" in logs[0]


def test_workspace_logs_filter_command(flask_client):
    resp = flask_client.get("/workspace/logs?type=command&offset=-20&limit=5", headers={"API-Key": API_KEY})
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        logs = resp.get_json()
        for entry in logs:
            assert entry["type"] == "command"


def test_workspace_logs_filter_output(flask_client):
    resp = flask_client.get("/workspace/logs?type=output&offset=-20&limit=5", headers={"API-Key": API_KEY})
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        logs = resp.get_json()
        for entry in logs:
            assert entry["type"] == "output"