from flask import Flask
from flask_socketio import SocketIO

# Shared workspace log singleton
from . import workspace_log

socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    app = Flask(__name__)

    # Register blueprints
    from .routes import execute, execute_worker, read_file, write_file, read_partial, auth, auth_github
    app.register_blueprint(execute.bp, url_prefix="/api")
    app.register_blueprint(execute_worker.bp, url_prefix="/api")
    app.register_blueprint(read_file.bp, url_prefix="/api")
    app.register_blueprint(write_file.bp, url_prefix="/api")
    app.register_blueprint(read_partial.bp, url_prefix="/api")
    # app.register_blueprint(workspace.bp, url_prefix="/api")
    app.register_blueprint(auth.bp, url_prefix="/api")
    app.register_blueprint(auth_github.bp, url_prefix="/api")

    return app