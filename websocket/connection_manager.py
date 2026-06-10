from collections import defaultdict #used because normal dict give errro if key is not present it nehave exacly like c++ map
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connection = defaultdict(list)

    async def connect(self,channel_id:int,websocket:WebSocket):
        await websocket.accept()
        self.active_connection[channel_id].append(websocket)

    def disconnect(self,channel_id:int,websocket:WebSocket):
        self.active_connection[channel_id].remove(websocket)
        if not self.active_connection[channel_id]:
            del self.active_connection[channel_id]

    async def broadcast(self,channel_id:int,data:dict):
        for connection in self.active_connection.get(channel_id,[]):
            await connection.send_json(data)
    
manager = ConnectionManager()
