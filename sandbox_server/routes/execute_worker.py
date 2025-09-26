import os
import pty
import subprocess
import uuid
from flask import Blueprint, request, jsonify
from ..socket import socketio
from .. import workspace_log

bp = Blueprint("execute_worker", __name__, url_prefix="/execute/worker")

SANDBOX_DIR = "/sandbox"
BUFFER_LIMIT = 50 * 1024  # 50 KB


def run_command(job_id, command, pwd, on_output=None):
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
                    "stream": "stdout",
                    "line": line,
                })
                socketio.emit("event", event, namespace="/ws/workspace")
                if on_output:
                    on_output(line)

            if len(stdout_buf) < BUFFER_LIMIT:
                stdout_buf += chunk

        process.wait()
        os.close(master_fd)
        return process.returncode, stdout_buf
    except Exception as e:
        return 1, str(e)


@bp.route("", methods=["POST"])
def execute_worker():
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

    # Log command event
    command_event = workspace_log.append_event({
        "type": "command",
        "job_id": job_id,
        "command": command,
        "source": "api",
    })
    socketio.emit("event", command_event, namespace="/ws/workspace")

    returncode, stdout_buf = run_command(job_id, command, pwd)

    return jsonify({
        "job_id": job_id,
        "command": command,
        "returncode": returncode,
        "stdout": stdout_buf[:BUFFER_LIMIT],
        "stderr": "",
    })