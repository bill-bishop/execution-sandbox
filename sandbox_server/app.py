from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flask_jwt_extended import JWTManager

from .routes import all_blueprints
from .config import API_KEY
from .socket import socketio
from .models import db

app = Flask(__name__)

# TODO: restrict origins
CORS(app, supports_credentials=True)

# Swagger setup
swagger = Swagger(app, template_file="openapi-swagger2.yml")

# DB + JWT setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sandbox.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"

# ✅ Configure JWT to use cookies
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_NAME"] = "auth_token"
app.config["JWT_COOKIE_SECURE"] = True   # only allow over HTTPS
app.config["JWT_COOKIE_SAMESITE"] = "Lax"


db.init_app(app)
jwt = JWTManager(app)

# SocketIO instance, initialized in app.py
socketio.init_app(app)

print(f"socketio id: {id(socketio)}", flush=True)

# Initialize WebSocket namespace
from .routes import ws
ws.init_socketio(socketio)

# ✅ Register all Blueprints
for bp in all_blueprints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, host="0.0.0.0", port=8080)