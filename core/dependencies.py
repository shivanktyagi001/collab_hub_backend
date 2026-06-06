from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from database.dependency import get_db
from models.users import User

from core.security import decode_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(token: str = Depends( oauth2_scheme),db: Session = Depends(get_db),):
    print("TOKEN RECEIVED:", token)
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid access token"
        )
    user_id = int(
        payload["sub"]
    )

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