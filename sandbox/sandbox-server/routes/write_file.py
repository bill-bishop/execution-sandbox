import os
from flask import Blueprint, request, jsonify

bp = Blueprint("write_file", __name__, url_prefix="/write")

SANDBOX_DIR = "/sandbox"

@bp.route("", methods=["POST"])
def write_file_plain():
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