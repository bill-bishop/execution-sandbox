from flask_socketio import SocketIO

print("Initializing SocketIO")

socketio = SocketIO(cors_allowed_origins="*", logger=True, engineio_logger=True)

print(f"socketio id: {id(socketio)}", flush=True)
