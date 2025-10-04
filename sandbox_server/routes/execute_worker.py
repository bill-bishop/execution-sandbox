import os
import pty
import subprocess
import time
import uuid
import select
from flask import Blueprint, request, jsonify

# Fixed import path (was: from sandbox_server import workspace_log)
from .. import workspace_log
from ..socket import socketio

bp = Blueprint("execute_worker", __name__, url_prefix="/execute/worker")

SANDBOX_DIR = "/sandbox"
BUFFER_LIMIT = 50 * 1024  # 50 KB


def run_command(job_id, command, pwd, on_output=None):
    if not os.path.isabs(pwd):
        pwd = os.path.join(SANDBOX_DIR, pwd)
    if not os.path.exists(pwd):
        return 1, "Working directory does not exist"

    COMMAND_TIMEOUT = int(os.environ.get("COMMAND_TIMEOUT", 60))

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
    start_time = time.time()
    killed = False

    while True:
        if time.time() - start_time > COMMAND_TIMEOUT:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            killed = True
            event = {
                "type": "output",
                "job_id": job_id,
                "command": command,
                "source": "api",
                "stream": "stderr",
                "line": "Process timed out and was killed",
            }
            workspace_log.append_event(event)
            socketio.emit("event", event, namespace="/ws/workspace", broadcast=True)
            break

        rlist, _, _ = select.select([master_fd], [], [], 0.1)
        if rlist:
            try:
                data_bytes = os.read(master_fd, 1024)
            except OSError:
                break

            if not data_bytes:
                break

            chunk = data_bytes.decode(errors="ignore")
            for line in chunk.splitlines():
                event = {
                    "type": "output",
                    "job_id": job_id,
                    "command": command,
                    "source": "api",
                    "stream": "stdout",
                    "line": line,
                }

                event = workspace_log.append_event(event)
                socketio.emit("event", event, namespace="/ws/workspace", broadcast=True)

                if on_output:
                    on_output(line)

            if len(stdout_buf) < BUFFER_LIMIT:
                stdout_buf += chunk
        else:
            if process.poll() is not None:
                break

    process.wait()
    os.close(master_fd)

    if killed:
        return -1, stdout_buf
    return process.returncode, stdout_buf


@bp.route("", methods=["POST"])
def execute_worker():
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "No command provided"}), 400

    command = data["command"]
    pwd = data.get("pwd", SANDBOX_DIR)
    job_id = str(uuid.uuid4())

    socketio.start_background_task(run_command, job_id, command, pwd)

    return jsonify({
        "job_id": job_id,
        "command": command,
        "returncode": None,
        "stdout": "--- Execution started, follow logs via /api/workspace/logs or WebSocket ---",
        "stderr": ""
    })