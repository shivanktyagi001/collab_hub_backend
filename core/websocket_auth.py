from fastapi import WebSocket, HTTPException
from sqlalchemy.orm import Session

from core.security import decode_token
from models.users import User


async def get_ws_current_user(
    websocket: WebSocket,
    db: Session,
):
    token = websocket.query_params.get("token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token missing",
        )

    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid access token",
        )

    user_id = int(payload["sub"])

    user = db.get(
        User,
        user_id,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user