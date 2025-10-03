from flask import Blueprint, redirect, request, jsonify, make_response
import os
import requests
from flask_jwt_extended import create_access_token
from ..models import db, User, Workspace

bp = Blueprint("auth_github", __name__)

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "changeme")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "changeme")
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


def _validate_target(target: str) -> str:
    if not target:
        return "/dashboard"
    if target.startswith("/") and not target.startswith("//"):
        return target
    return "/dashboard"


@bp.route("/auth/redirect/github")
def github_redirect():
    target = request.args.get("target", "/dashboard")
    redirect_uri = "https://hermesai.dev/api/auth/callback/github"
    url = (
        f"{GITHUB_AUTHORIZE_URL}?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=read:user user:email"
        f"&state={target}"
    )
    return redirect(url)


@bp.route("/auth/callback/github")
def github_callback():
    code = request.args.get("code")
    state = request.args.get("state", "/dashboard")
    target = _validate_target(state)

    if not code:
        return jsonify({"error": "Missing code"}), 400

    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
    }
    headers = {"Accept": "application/json"}
    token_resp = requests.post(GITHUB_TOKEN_URL, data=data, headers=headers)
    token_json = token_resp.json()

    access_token = token_json.get("access_token")
    if not access_token:
        return jsonify({"error": "Failed to get access token", "details": token_json}), 400

    # Fetch GitHub user profile
    user_resp = requests.get(GITHUB_USER_URL, headers={"Authorization": f"Bearer {access_token}"})
    user_json = user_resp.json()

    github_id = str(user_json.get("id"))
    login = user_json.get("login")
    email = user_json.get("email") or f"{login}@users.noreply.github.com"

    # Lookup or create user
    user = User.query.filter_by(provider="github", provider_id=github_id).first()
    if not user:
        user = User(email=email, provider="github", provider_id=github_id)
        db.session.add(user)
        db.session.commit()
        ws = Workspace(user_id=user.id, container_url=f"http://workspace_{user.id}:8080")
        db.session.add(ws)
        db.session.commit()

    # Create JWT using flask_jwt_extended
    app_token = create_access_token(identity=str(user.id))

    response = make_response(redirect(f"https://hermesai.dev{target}"))
    response.set_cookie(
        "auth_token",
        app_token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )
    return response