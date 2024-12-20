import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

SANDBOX_DIR = "./sandbox"

@app.route("/execute", methods=["POST"])
def execute():
    command = request.json.get("command")
    if not command:
        return jsonify({"error": "No command provided"}), 400

    # Ensure the command is run in the sandbox
    try:
        result = subprocess.run(
            command, cwd=SANDBOX_DIR, shell=True, capture_output=True, text=True, timeout=5
        )
        return jsonify({"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
def write_file():
    data = request.json
    filename = data.get("filename")
    content = data.get("content")
    if not filename or content is None:
        return jsonify({"error": "Invalid input"}), 400

    filepath = os.path.join(SANDBOX_DIR, filename)
    try:
        with open(filepath, "w") as f:
            f.write(content)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
