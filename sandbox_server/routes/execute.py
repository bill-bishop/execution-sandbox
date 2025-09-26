import os
import pty
import subprocess
import uuid
from flask import Blueprint, request, jsonify
from ..socket import socketio
from .. import workspace_log

bp = Blueprint("execute", __name__, url_prefix="/execute")

SANDBOX_DIR = "/sandbox"
BUFFER_LIMIT = 50 * 1024  # 50 KB

@bp.route("", methods=["POST"])
def execute():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request: No JSON body provided"}), 400

    command = data.get("command")
    pwd = data.get("pwd", SANDBOX_DIR)
    if not command:
        return jsonify({"error": "No command provided"}), 400

    if not os.path.isabs(pwd):
        pwd = os.path.join(SANDBOX_DIR, pwd)
    if not os.path.exists(pwd):
        return jsonify({"error": "Working directory does not exist"}), 400

    job_id = str(uuid.uuid4())

    # Log and emit command event
    command_event = workspace_log.append_event({
        "type": "command",
        "job_id": job_id,
        "command": command,
        "source": "api",
    })
    socketio.emit("event", command_event, namespace="/ws/workspace")

    try:
        master_fd, slave_fd = pty.openpty()
        process = subprocess.Popen(
            command,
            cwd=pwd,
            shell=True,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            text=True,
            bufsize=1,
        )
        os.close(slave_fd)

        stdout_buf = ""
        while True:
            try:
                data_bytes = os.read(master_fd, 1024)
            except OSError:
                break

            if not data_bytes:
                break

            chunk = data_bytes.decode(errors="ignore")
            for line in chunk.splitlines():
                event = workspace_log.append_event({
                    "type": "output",
                    "job_id": job_id,
                    "command": command,
                    "source": "api",
                    "stream": "stdout",  # merged stream
                    "line": line,
                })
                socketio.emit("event", event, namespace="/ws/workspace")

            if len(stdout_buf) < BUFFER_LIMIT:
                stdout_buf += chunk

        process.wait(timeout=60)
        os.close(master_fd)

        return jsonify({
            "job_id": job_id,
            "command": command,
            "returncode": process.returncode,
            "stdout": stdout_buf[:BUFFER_LIMIT],
            "stderr": "",  # PTY merges streams
        })
    except subprocess.TimeoutExpired:
        process.kill()
        event = workspace_log.append_event({
            "type": "output",
            "job_id": job_id,
            "command": command,
            "source": "api",
            "stream": "stdout",
            "line": "Command timed out",
        })
        socketio.emit("event", event, namespace="/ws/workspace")
        return jsonify({"error": "Command timed out", "job_id": job_id}), 500
    except Exception as e:
        event = workspace_log.append_event({
            "type": "output",
            "job_id": job_id,
            "command": command,
            "source": "api",
            "stream": "stdout",
            "line": str(e),
        })
        socketio.emit("event", event, namespace="/ws/workspace")
        return jsonify({"error": str(e), "job_id": job_id}), 500