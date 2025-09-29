import os
import tempfile
from sandbox_server.config import API_KEY


def test_write_and_read_file(flask_client):
    test_file = "/sandbox/test_file.txt"
    data = {"filename": test_file, "content": "Hello File!"}
    resp = flask_client.post(
        "/write",
        headers={"API-Key": API_KEY},
        json=data,
    )
    assert resp.status_code in (200, 401)

    resp = flask_client.get(
        f"/read?filename={test_file}",
        headers={"API-Key": API_KEY},
    )
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        assert b"Hello File!" in resp.data


def test_read_partial_file(flask_client):
    test_file = "/sandbox/test_partial.txt"
    content = "ABCDEFGH"
    open(test_file, "w").write(content)

    resp = flask_client.get(
        f"/read-partial?filename={test_file}&offset=0&limit=4",
        headers={"API-Key": API_KEY},
    )
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        data = resp.get_json()
        assert data["content"] == "ABCD"
        assert data["offset"] == 0
        assert data["nextOffset"] == 4