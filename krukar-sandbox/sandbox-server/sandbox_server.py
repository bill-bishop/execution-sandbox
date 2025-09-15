import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

SANDBOX_DIR = "/sandbox"

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()  # Parse JSON input
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

    # Ensure the working directory is valid
    if not os.path.isabs(pwd):
        pwd = os.path.join(SANDBOX_DIR, pwd)
    if not os.path.exists(pwd):
        return jsonify({
            "stdout": "",
            "stderr": "Working directory does not exist",
            "returncode": 400,
            "message": f"Command: `{command}`\n\nErrors:\n```\nWorking directory does not exist```"
        }), 400

    # Attempt to execute the command
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

@app.route("/read", methods=["GET"])
def read_file():
    filename = request.args.get("filename")
    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    filepath = os.path.join(SANDBOX_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File does not exist"}), 404

    try:
        with open(filepath, "r") as f:
            content = f.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/write", methods=["POST"])
def write_file_plain():
    # filename = request.args.get("filename")
    # if not filename:
    #     return jsonify({"error": "No filename provided"}), 400

    try:
        data = request.get_json()
        if not data or "content" not in data:
            return jsonify({"error": "No content provided"}), 400
        if "filename" not in data:
            return jsonify({"error": "No filename provided"}), 400

        filename = data["filename"]
        content = data["content"]
        filepath = os.path.join(SANDBOX_DIR, filename)
        
        with open(filepath, "w") as f:
            f.write(content)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
