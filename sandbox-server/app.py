from flask import Flask
from routes import execute, read_file, write_file

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(execute.bp)
app.register_blueprint(read_file.bp)
app.register_blueprint(write_file.bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)