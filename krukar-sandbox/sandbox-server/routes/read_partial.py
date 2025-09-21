import os
from flask import Blueprint, request, jsonify

bp = Blueprint("read_partial", __name__, url_prefix="/read-partial")

SANDBOX_DIR = "/sandbox"

@bp.route("", methods=["GET"])
def read_partial():
    filename = request.args.get("filename")
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 4096))

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    filepath = os.path.join(SANDBOX_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File does not exist"}), 404

    try:
        with open(filepath, "r") as f:
            f.seek(offset)
            content = f.read(limit)
            next_offset = f.tell()
            eof = next_offset >= os.path.getsize(filepath)

        return jsonify({
            "content": content,
            "offset": offset,
            "nextOffset": next_offset,
            "eof": eof
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500