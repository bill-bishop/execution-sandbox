from flask_socketio import Namespace, emit

class WorkspaceNamespace(Namespace):
    def on_connect(self):
        emit("connected", {"message": "Connected to /ws/workspace"})
        print("Client connected to /ws/workspace")

    def on_disconnect(self, reason=None):
        if reason:
            print(f"Client disconnected from /ws/workspace. Reason: {reason}")
        else:
            print("Client disconnected from /ws/workspace")

    def on_message(self, data):
        print(f"Received message on /ws/workspace: {data}")
        # You can also emit a response back to the client if needed
        emit("message_received", {"status": "ok"})


def init_socketio(socketio):
    socketio.on_namespace(WorkspaceNamespace("/ws/workspace"))