from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import db, User, Workspace

bp = Blueprint("auth", __name__)

SUPPORTED_PROVIDERS = ["google", "github", "apple", "facebook", "discord"]

@bp.route("/auth/providers", methods=["GET"])
def providers():
    return jsonify(SUPPORTED_PROVIDERS)

# Dummy login endpoint (simulates OAuth)
@bp.route("/auth/login", methods=["POST"])
def login():
    # In real implementation, handle OAuth callback
    email = "testuser@example.com"
    provider = "dummy"
    provider_id = "12345"

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, provider=provider, provider_id=provider_id)
        db.session.add(user)
        db.session.commit()
        ws = Workspace(user_id=user.id, container_url=f"http://workspace_{user.id}:8080")
        db.session.add(ws)
        db.session.commit()

    token = create_access_token(identity=user.id)
    return jsonify(access_token=token)


@bp.route("/me")
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = User.query.get(uid)
    return {
        "id": user.id,
        "email": user.email,
        "workspaces": [ws.container_url for ws in user.workspaces],
    }