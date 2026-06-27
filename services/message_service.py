from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.message import Message
from models.channel import Channel
from models.users import User
from schemas.message import CreateMessageRequest, UpdateMessageRequest


def create_message(
        db: Session,
        channel_id: int,
        request: CreateMessageRequest,
        curr_user: User
):
    """Create a new message in a channel"""
    try:
        if not request.content or not request.content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message content cannot be empty"
            )
        
        channel = db.query(Channel).filter(
            Channel.id == channel_id
        ).first()

        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found"
            )
        
        message = Message(
            channel_id=channel_id,
            sender_id=curr_user.id,
            content=request.content.strip()
        )
       
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while creating message"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating message"
        )


def list_messages(
        db: Session,
        channel_id: int,
        limit: int = 10,
        offset: int = 0
):
    """List all messages in a channel with pagination"""
    try:
        channel = db.query(Channel).filter(
            Channel.id == channel_id
        ).first()
        
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found"
            )
        
        return db.query(Message).filter(
            Message.channel_id == channel_id
        ).order_by(
            Message.created_at.asc()
        ).limit(limit).offset(offset).all()
    
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while fetching messages"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching messages"
        )


def get_message(
        db: Session,
        message_id: int
):
    """Get a specific message by ID"""
    try:
        if message_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid message ID"
            )
        
        message = db.query(Message).filter(
            Message.id == message_id
        ).first()

        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        return message
    
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while fetching message"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching message"
        )


def update_message(
        db: Session,
        message_id: int,
        request: UpdateMessageRequest,
        curr_user: User
):
    """Update a message (only by sender)"""
    try:
        if message_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid message ID"
            )
        
        if not request.content or not request.content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message content cannot be empty"
            )
        
        message = db.query(Message).filter(
            Message.id == message_id
        ).first()

        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        if message.sender_id != curr_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to update this message"
            )
        
        if message.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update a deleted message"
            )
        
        message.content = request.content.strip()
        message.edited = True

        db.commit()
        db.refresh(message)

        return message
    
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while updating message"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating message"
        )


def delete_message(
        db: Session,
        message_id: int,
        curr_user: User
):
    """Delete a message (soft delete - only by sender)"""
    try:
        if message_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid message ID"
            )
        
        message = db.query(Message).filter(
            Message.id == message_id
        ).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        if message.sender_id != curr_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to delete this message"
            )
        
        if message.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message is already deleted"
            )
        
        message.is_deleted = True
        message.content = "[Message deleted]"
        db.commit()

        return {
            "message": "Message deleted successfully",
            "message_id": message.id
        }
    
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while deleting message"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting message"
        )