from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from .routes import execute_worker, read_file, write_file, read_partial, workspace, ws
from .config import API_KEY
from .socket import socketio


app = Flask(__name__)

# TODO: restrict origins
CORS(app, supports_credentials=True)
socketio.init_app(app, cors_allowed_origins="*")

# Swagger setup
swagger = Swagger(app, template_file="openapi-swagger2.yml")

# Middleware for API key authentication
# @app.before_request
# def authenticate():
#     if request.path.startswith("/static") or request.path.startswith("/ws") or request.path.startswith("/apidocs"):
#         return  # Skip static files, websocket, and swagger docs
#
#     key = request.headers.get("API-Key")
#     if key != API_KEY:
#         return jsonify({"error": "Unauthorized"}), 401

# Register Blueprints
app.register_blueprint(execute_worker.bp)
app.register_blueprint(read_file.bp)
app.register_blueprint(write_file.bp)
app.register_blueprint(read_partial.bp)
app.register_blueprint(workspace.bp)

# Initialize WebSocket namespace
ws.init_socketio(socketio)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080)