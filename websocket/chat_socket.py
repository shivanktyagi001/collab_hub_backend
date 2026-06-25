from fastapi import APIRouter,WebSocket,Depends,status
from websocket.connection_manager import manager
from websocket.redis_pubsub import publish_event, ensure_channel_subscription, stop_channel_subscription
from websocket.events import (
    message_created_event,typing_started_event,typing_stopped_event,
    user_offline_event,user_online_event

)
from core.dependencies import get_db
from core.websocket_auth import get_ws_current_user
from services.message_service import create_message
from schemas.message import CreateMessageRequest
from sqlalchemy.orm import Session
import json
from websocket.presence import presence_manager

router = APIRouter(
    prefix="/ws",
    tags=["Websocket"]
)

@router.websocket("/channels/{channel_id}")
async def websocket_endpoint(websocket:WebSocket,channel_id:int,db:Session=Depends(get_db)):
    user = None
    try:
        user = await get_ws_current_user(
            websocket,
            db,
        )
        await manager.connect(channel_id,websocket)
        await ensure_channel_subscription(channel_id)
        become_online = presence_manager.connect(user.id)
        
        if become_online:
            await publish_event(channel_id, user_online_event(user))
        while True:
            data = await websocket.receive_text()
            try:
                # Parse incoming message
                message_data = json.loads(data)
                content = message_data.get("content", "").strip()
                event = message_data.get("event")
                if event == "send_message":
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
                    await publish_event(channel_id, message_created_event(message))
                elif event == "typing_started":
                    await publish_event(channel_id, typing_started_event(user))
                elif event == "typing_stopped":
                    await publish_event(channel_id, typing_stopped_event(user))
                else:
                    await websocket.send_json({
                        "event": "error",
                        "detail": "Unknown event type"
                    }) 
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
                
    except Exception:
        if user is not None:
            became_offline = presence_manager.disconnect(user.id)
            if became_offline:
                await publish_event(channel_id, user_offline_event(user))

        try:
            manager.disconnect(channel_id, websocket)
            if channel_id not in manager.active_connection:
                await stop_channel_subscription(channel_id)
        except (KeyError, ValueError):
            pass

        try:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        except Exception:
            pass