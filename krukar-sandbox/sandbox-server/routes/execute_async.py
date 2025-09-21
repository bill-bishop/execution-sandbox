import os
import subprocess
import uuid
import json
from flask import Blueprint, request, jsonify

bp = Blueprint("execute_async", __name__, url_prefix="/execute-async")

SANDBOX_DIR = "/sandbox"
LOGS_DIR = os.path.join(SANDBOX_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

@bp.route("", methods=["POST"])
def execute_async():
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "No command provided"}), 400

    command = data["command"]
    pwd = data.get("pwd", SANDBOX_DIR)
    if not os.path.isabs(pwd):
        pwd = os.path.join(SANDBOX_DIR, pwd)

    if not os.path.exists(pwd):
        return jsonify({"error": "Working directory does not exist"}), 400

    job_id = str(uuid.uuid4())
    log_file = os.path.join(LOGS_DIR, f"{job_id}.log")
    meta_file = os.path.join(LOGS_DIR, f"{job_id}.json")

    with open(log_file, "w") as lf:
        process = subprocess.Popen(
            command,
            cwd=pwd,
            shell=True,
            stdout=lf,
            stderr=lf,
            text=True,
        )

    metadata = {
        "job_id": job_id,
        "pid": process.pid,
        "status": "running",
        "returncode": None,
    }
    with open(meta_file, "w") as mf:
        json.dump(metadata, mf)

    return jsonify({"job_id": job_id}), 202


@bp.route("/status/<job_id>", methods=["GET"])
def job_status(job_id):
    meta_file = os.path.join(LOGS_DIR, f"{job_id}.json")
    if not os.path.exists(meta_file):
        return jsonify({"error": "Job not found"}), 404

    with open(meta_file, "r") as mf:
        metadata = json.load(mf)

    try:
        pid = metadata["pid"]
        ret = os.waitpid(pid, os.WNOHANG)[1]
        if ret != 0:
            metadata["status"] = "finished"
            metadata["returncode"] = ret >> 8
            with open(meta_file, "w") as mf:
                json.dump(metadata, mf)
    except ChildProcessError:
        # Already reaped
        if metadata["status"] == "running":
            metadata["status"] = "finished"
            with open(meta_file, "w") as mf:
                json.dump(metadata, mf)

    return jsonify(metadata)


@bp.route("/log/<job_id>", methods=["GET"])
def job_log(job_id):
    log_file = os.path.join(LOGS_DIR, f"{job_id}.log")
    if not os.path.exists(log_file):
        return jsonify({"error": "Log not found"}), 404

    with open(log_file, "r") as lf:
        content = lf.read()
    return jsonify({"content": content})