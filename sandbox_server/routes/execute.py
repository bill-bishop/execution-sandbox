import time
import queue
import uuid
from flask import Blueprint, request, jsonify
from .execute_worker import run_command, SANDBOX_DIR
from ..socket import socketio

bp = Blueprint("execute_wrapper", __name__, url_prefix="/execute")


@bp.route("", methods=["POST"])
def execute_wrapper():
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "No command provided"}), 400

    command = data["command"]
    pwd = data.get("pwd", SANDBOX_DIR)
    job_id = str(uuid.uuid4())

    # Debug emit — should always be visible
    socketio.emit(
        "event",
        {"type": "command", "job_id": job_id, "command": command},
        namespace="/ws/workspace",
        broadcast=True,
    )

    q = queue.Queue()
    result = {"returncode": None}

    def on_output(line):
        q.put(line)

    def runner():
        rc, _ = run_command(job_id, command, pwd, on_output)
        result["returncode"] = rc
        q.put(None)  # signal completion

    # Run worker in background task (Socket.IO-aware)
    socketio.start_background_task(runner)

    # Collect lines for up to 3 seconds or until completion
    lines = []
    start = time.time()
    finished = False
    while time.time() - start < 3:
        try:
            line = q.get(timeout=0.2)
            if line is None:  # completion signal
                finished = True
                break
            lines.append(line)
        except queue.Empty:
            continue

    # Add cut-off marker if still running
    if not finished:
        lines.append("--- Process still running ---")

    return jsonify({
        "job_id": job_id,
        "command": command,
        "stdout": "\n".join(lines),
        "returncode": result["returncode"],
    })