import os
from flask import Blueprint, request, jsonify

bp = Blueprint("read_file", __name__, url_prefix="/read")

SANDBOX_DIR = "/sandbox"
MAX_READ_SIZE = 51200  # 50 KB

@bp.route("", methods=["GET"])
def read_file():
    filename = request.args.get("filename")
    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    filepath = os.path.join(SANDBOX_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File does not exist"}), 404

    try:
        file_size = os.path.getsize(filepath)
        truncated = False

        with open(filepath, "r", errors="ignore") as f:
            if file_size > MAX_READ_SIZE:
                content = f.read(MAX_READ_SIZE)
                truncated = True
            else:
                content = f.read()

        if truncated:
            content += "\n\n[TRUNCATED OUTPUT: file too large. Use /read-partial to read in chunks.]"

        return jsonify({"content": content, "truncated": truncated, "size": file_size})

    except Exception as e:
        return jsonify({"error": str(e)}), 500