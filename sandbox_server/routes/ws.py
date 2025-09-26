from flask_socketio import Namespace, emit

class WorkspaceNamespace(Namespace):
    def on_connect(self):
        emit("connected", {"message": "Connected to /ws/workspace"})

    def on_disconnect(self):
        pass


def init_socketio(socketio):
    socketio.on_namespace(WorkspaceNamespace("/ws/workspace"))