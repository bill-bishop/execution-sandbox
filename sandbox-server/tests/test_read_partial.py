import os
from app import app

client = app.test_client()
headers = {"API-Key": "default-secret-key"}

def test_read_partial_file_chunks(tmp_path):
    # Create a temporary large file
    file_path = os.path.join("/sandbox", "test_large.txt")
    content = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 100  # 2600 chars
    with open(file_path, "w") as f:
        f.write(content)

    # First chunk
    resp1 = client.get("/read-partial?filename=test_large.txt&offset=0&limit=100", headers=headers)
    assert resp1.status_code == 200
    data1 = resp1.get_json()
    assert data1["offset"] == 0
    assert data1["nextOffset"] == 100
    assert data1["eof"] is False
    assert len(data1["content"]) == 100

    # Next chunk
    resp2 = client.get("/read-partial?filename=test_large.txt&offset=100&limit=200", headers=headers)
    assert resp2.status_code == 200
    data2 = resp2.get_json()
    assert data2["offset"] == 100
    assert data2["nextOffset"] == 300
    assert data2["eof"] is False
    assert len(data2["content"]) == 200

    # Final chunk until EOF
    filesize = os.path.getsize(file_path)
    resp3 = client.get(f"/read-partial?filename=test_large.txt&offset={filesize-50}&limit=100", headers=headers)
    assert resp3.status_code == 200
    data3 = resp3.get_json()
    assert data3["eof"] is True
    assert len(data3["content"]) <= 100