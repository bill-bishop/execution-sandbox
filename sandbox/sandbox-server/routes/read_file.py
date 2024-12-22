import os
from flask import Blueprint, request, jsonify

bp = Blueprint("read_file", __name__, url_prefix="/read")

SANDBOX_DIR = "/sandbox"

@bp.route("", methods=["GET"])
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