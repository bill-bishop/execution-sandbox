import time
import threading
import queue
import uuid
from flask import Blueprint, request, jsonify
from .. import workspace_log
from .execute_worker import run_command, SANDBOX_DIR

bp = Blueprint("execute_wrapper", __name__, url_prefix="/execute")


@bp.route("", methods=["POST"])
def execute_wrapper():
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "No command provided"}), 400

    command = data["command"]
    pwd = data.get("pwd", SANDBOX_DIR)
    job_id = str(uuid.uuid4())

    q = queue.Queue()

    def on_output(line):
        q.put(line)

    # Log command event right away
    command_event = workspace_log.append_event({
        "type": "command",
        "job_id": job_id,
        "command": command,
        "source": "api",
    })

    # Run worker in background thread
    thread = threading.Thread(
        target=run_command,
        args=(job_id, command, pwd, on_output),
        daemon=True,
    )
    thread.start()

    # Collect lines for a few seconds
    lines = []
    start = time.time()
    while time.time() - start < 3:
        try:
            line = q.get(timeout=0.2)
            lines.append(line)
        except queue.Empty:
            continue

    return jsonify({
        "job_id": job_id,
        "command": command,
        "stdout": "\n".join(lines),
        "returncode": None,  # still running
    })