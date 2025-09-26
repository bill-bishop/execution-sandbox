from flask import Blueprint, request, jsonify
from .. import workspace_log

bp = Blueprint("workspace", __name__, url_prefix="/workspace")

@bp.route("/logs", methods=["GET"])
def get_logs():
    try:
        offset = int(request.args.get("offset", 0))
    except ValueError:
        offset = 0
    try:
        limit = int(request.args.get("limit", 100))
    except ValueError:
        limit = 100

    logs = workspace_log.get_logs(offset=offset, limit=limit)
    return jsonify(logs)