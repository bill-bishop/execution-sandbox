from flask import Blueprint, redirect, request, jsonify
import os
import requests

bp = Blueprint("auth_github", __name__)

# Load GitHub OAuth config (client_id + client_secret should be env vars)
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "changeme")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "changeme")
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

# Step 1: redirect user to GitHub OAuth
@bp.route("/auth/redirect/github")
def github_redirect():
    redirect_uri = "https://dropcode.org/api/auth/callback/github"
    url = f"{GITHUB_AUTHORIZE_URL}?client_id={GITHUB_CLIENT_ID}&redirect_uri={redirect_uri}&scope=read:user user:email"
    return redirect(url)

# Step 2: GitHub redirects back here with ?code=...
@bp.route("/auth/callback/github")
def github_callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Missing code"}), 400

    # Exchange code for access token
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
    }
    headers = {"Accept": "application/json"}
    token_resp = requests.post(GITHUB_TOKEN_URL, data=data, headers=headers)
    token_json = token_resp.json()

    # Placeholder — later: lookup user profile, create/link user, issue JWT
    return jsonify(token_json)