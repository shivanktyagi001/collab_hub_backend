from fastapi import APIRouter,WebSocket,Depends,status
from websocket.connection_manager import manager
from websocket.events import message_created_event
from core.dependencies import get_db
from core.websocket_auth import get_ws_current_user
from services.message_service import create_message
from schemas.message import CreateMessageRequest
from sqlalchemy.orm import Session
import json

router = APIRouter(
    prefix="/ws",
    tags=["Websocket"]
)

@router.websocket("/channels/{channel_id}")
async def websocket_endpoint(websocket:WebSocket,channel_id:int,db:Session=Depends(get_db)):
    try:
        user = await get_ws_current_user(
            websocket,
            db,
        )
        await manager.connect(channel_id,websocket)
        
        while True:
            data = await websocket.receive_text()
            try:
                # Parse incoming message
                message_data = json.loads(data)
                content = message_data.get("content", "").strip()
                
                if not content:
                    await websocket.send_json({
                        "event": "error",
                        "detail": "Message content cannot be empty"
                    })
                    continue
                
                # Create message in database
                message_request = CreateMessageRequest(content=content)
                message = create_message(
                    db,
                    channel_id,
                    message_request,
                    user
                )
                
                # Broadcast to all connected clients
                await manager.broadcast(channel_id, message_created_event(message))
                
            except json.JSONDecodeError:
                await websocket.send_json({
                    "event": "error",
                    "detail": "Invalid JSON format"
                })
            except Exception as e:
                await websocket.send_json({
                    "event": "error",
                    "detail": str(e)
                })
                
    except Exception as e:
        manager.disconnect(channel_id, websocket)
        try:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        except:
            pass