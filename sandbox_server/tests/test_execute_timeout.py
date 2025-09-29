import os
from sandbox_server.routes import execute_worker
from sandbox_server import workspace_log


def test_execute_timeout(monkeypatch):
    # Force timeout to 1 second for testing
    monkeypatch.setenv("COMMAND_TIMEOUT", "1")

    job_id = "test-timeout"
    cmd = "sleep 5"
    rc, out = execute_worker.run_command(job_id, cmd, "/sandbox")

    assert rc == -1  # killed by timeout


def test_execute_timeout_event(monkeypatch):
    # Force timeout to 1 second for testing
    monkeypatch.setenv("COMMAND_TIMEOUT", "1")

    job_id = "test-timeout-event"
    cmd = "sleep 5"
    rc, out = execute_worker.run_command(job_id, cmd, "/sandbox")

    assert rc == -1

    events = workspace_log.get_logs(-10, 10)
    assert any("Process timed out and was killed" in e.get("line", "") for e in events)