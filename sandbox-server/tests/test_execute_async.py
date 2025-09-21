import os
import time
import json
from app import app

client = app.test_client()

headers = {"API-Key": "default-secret-key"}


def test_execute_async_lifecycle():
    # Submit async job
    response = client.post(
        "/execute-async", json={"command": "echo Hello Async"}, headers=headers
    )
    assert response.status_code == 202
    job_id = response.get_json()["job_id"]

    # Poll status until finished or timeout
    for _ in range(10):
        status_resp = client.get(f"/execute-async/status/{job_id}", headers=headers)
        assert status_resp.status_code == 200
        data = status_resp.get_json()
        if data["status"] == "finished":
            break
        time.sleep(0.5)
    else:
        assert False, "Job did not finish in time"

    # Check log output
    log_resp = client.get(f"/execute-async/log/{job_id}", headers=headers)
    assert log_resp.status_code == 200
    log_data = log_resp.get_json()
    assert "Hello Async" in log_data["content"]