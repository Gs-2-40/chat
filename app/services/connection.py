from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str: WebSocket] = dict()

    async def connect(self, socket_id: str, web_socket: WebSocket):
        await web_socket.accept()
        self.active_connections.update({socket_id: web_socket})

    async def disconnect(self, socket_id: str):
        connection = self.active_connections.pop(socket_id, None)
        if connection:
            await connection.close()

    async def send_single_message(self, message, socket_id: str):
        if str(socket_id) in self.active_connections:
            ws = self.active_connections.get(socket_id)
            await ws.send_text(message)
