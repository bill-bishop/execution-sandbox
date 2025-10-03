import os
from flask import Blueprint, send_file, abort

bp = Blueprint("canvas", __name__)

CANVAS_DIR = "/.canvas"

@bp.route("/canvas", methods=["GET"])
def canvas_index():
    index_path = os.path.join(CANVAS_DIR, "index.html")
    if not os.path.exists(index_path):
        return "<h1>No Canvas Loaded</h1>", 200, {"Content-Type": "text/html"}
    return send_file(index_path, mimetype="text/html")


@bp.route("/canvas/assets/<path:filename>", methods=["GET"])
def canvas_assets(filename):
    asset_path = os.path.join(CANVAS_DIR, "assets", filename)
    if not os.path.exists(asset_path):
        abort(404)
    return send_file(asset_path)