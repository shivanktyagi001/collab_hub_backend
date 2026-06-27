from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from core.rate_limiter import rate_limit_send_message
from sqlalchemy.orm import Session
from websocket.redis_pubsub import publish_event
from core.dependencies import (
    get_db,
    get_current_user
)
from websocket.connection_manager import manager
from websocket.events import message_created_event
from models.users import User
from core.producer import publish_message
from schemas.message import (
    CreateMessageRequest,
    UpdateMessageRequest,
    MessageResponse
)

from services.message_service import (
    create_message,
    list_messages,
    get_message,
    update_message,
    delete_message
)

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

@router.post(
    "/channel/{channel_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED
)
async def send_message_route(
    channel_id: int,
    request: CreateMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new message in a channel"""
    try:
        await rate_limit_send_message(current_user.id)
        message =  create_message(
            db,
            channel_id,
            request,
            current_user
        )
        await publish_event(channel_id, message_created_event(message))
        await publish_message(
            "analytics_queue",
            {
                "message_id": message.id,
                "channel_id": channel_id,
                "sender_id": current_user.id,
            }
        )
        return message
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create message"
        )

@router.get(
    "/channel/{channel_id}",
    response_model=list[MessageResponse],
    status_code=status.HTTP_200_OK
)
def list_messages_route(
    channel_id: int,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get all messages from a channel with pagination (default limit: 10, offset: 0)"""
    try:
        if limit <= 0 or limit > 100:
            limit = 10
        if offset < 0:
            offset = 0
        
        return list_messages(
            db,
            channel_id,
            limit,
            offset
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch messages"
        )

@router.get(
    "/{message_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK
)
def get_message_route(
    message_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific message by ID"""
    try:
        return get_message(
            db,
            message_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch message"
        )

@router.patch(
    "/{message_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK
)
def update_message_route(
    message_id: int,
    request: UpdateMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a message (only message owner can update)"""
    try:
        return update_message(
            db,
            message_id,
            request,
            current_user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update message"
        )

@router.delete(
    "/{message_id}",
    status_code=status.HTTP_200_OK
)
def delete_message_route(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a message (soft delete - only message owner can delete)"""
    try:
        return delete_message(
            db,
            message_id,
            current_user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete message"
        )