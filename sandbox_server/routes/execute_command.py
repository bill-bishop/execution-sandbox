import subprocess
from flask import Blueprint, request, jsonify

bp = Blueprint("execute_command", __name__, url_prefix="/execute")

MAX_OUTPUT_CHARS = 100_000

@bp.route("", methods=["POST"])
def execute_command():
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "Missing command"}), 400

    command = data["command"]

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60  # avoid runaway commands
        )

        stdout = result.stdout or ""
        stderr = result.stderr or ""
        truncated = False

        if len(stdout) > MAX_OUTPUT_CHARS:
            stdout = stdout[:MAX_OUTPUT_CHARS] + "\n[TRUNCATED OUTPUT: use /logs for full output]"
            truncated = True

        if len(stderr) > MAX_OUTPUT_CHARS:
            stderr = stderr[:MAX_OUTPUT_CHARS] + "\n[TRUNCATED OUTPUT: use /logs for full output]"
            truncated = True

        return jsonify({
            "command": command,
            "returncode": result.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "truncated": truncated
        })

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Command timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500