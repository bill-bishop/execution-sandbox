import os
import subprocess
from flask import Blueprint, request, jsonify

bp = Blueprint("execute", __name__, url_prefix="/execute")

SANDBOX_DIR = "/sandbox"

@bp.route("", methods=["POST"])
def execute():
    data = request.get_json()
    if not data:
        return jsonify({
            "stdout": "",
            "stderr": "Invalid request: No JSON body provided",
            "returncode": 400,
            "message": "Command: None\n\nErrors:\n```\nInvalid request: No JSON body provided```"
        }), 400

    command = data.get("command")
    pwd = data.get("pwd", SANDBOX_DIR)

    if not command:
        return jsonify({
            "stdout": "",
            "stderr": "No command provided",
            "returncode": 400,
            "message": "Command: None\n\nErrors:\n```\nNo command provided```"
        }), 400

    if not os.path.isabs(pwd):
        pwd = os.path.join(SANDBOX_DIR, pwd)
    if not os.path.exists(pwd):
        return jsonify({
            "stdout": "",
            "stderr": "Working directory does not exist",
            "returncode": 400,
            "message": f"Command: `{command}`\n\nErrors:\n```\nWorking directory does not exist```"
        }), 400

    try:
        result = subprocess.run(
            command, cwd=pwd, shell=True, capture_output=True, text=True, timeout=35
        )
        message = (
            f"Command: `{command}`\n\n"
            f"Output:\n```\n{result.stdout}```\n\n"
            f"Errors:\n```\n{result.stderr}```\n\n"
            f"Return Code: {result.returncode}"
        )
        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "message": message
        })
    except subprocess.TimeoutExpired:
        message = (
            f"Command: `{command}`\n\n"
            f"Errors:\n```\nCommand timed out after 35 seconds```"
        )
        return jsonify({
            "stdout": "",
            "stderr": "Command timed out after 35 seconds",
            "returncode": 500,
            "message": message
        }), 500
    except Exception as e:
        message = (
            f"Command: `{command}`\n\n"
            f"Errors:\n```\n{str(e)}```"
        )
        return jsonify({
            "stdout": "",
            "stderr": str(e),
            "returncode": 500,
            "message": message
        }), 500