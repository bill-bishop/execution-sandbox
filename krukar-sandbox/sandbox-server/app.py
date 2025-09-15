from flask import Flask, request, jsonify
from routes import execute, read_file, write_file
from config import API_KEY

app = Flask(__name__)

# Middleware for API key authentication
# @app.before_request
# def authenticate():
#     if request.path.startswith("/static"):
#         return  # Skip static files

    # key = request.headers.get("API-Key")
    # if key != API_KEY:
    #     return jsonify({"error": "Unauthorized"}), 401

# Register Blueprints
app.register_blueprint(execute.bp)
app.register_blueprint(read_file.bp)
app.register_blueprint(write_file.bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)