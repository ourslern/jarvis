from fastapi import WebSocket
import asyncio


class WSManager:
    def __init__(self):
        self.clients: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.clients.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.clients:
            self.clients.remove(ws)

    async def broadcast(self, event: str, payload):
        dead = []

        for client in self.clients:
            try:
                await client.send_json({
                    "event": event,
                    "payload": payload,
                })
            except Exception:
                dead.append(client)

        for client in dead:
            self.disconnect(client)


ws_manager = WSManager()
