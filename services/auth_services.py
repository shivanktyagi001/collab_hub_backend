from core.security import hash_password,create_access_token,create_refresh_token,verify_password
from datetime import datetime,timedelta
from models.users import User
from models.refresh_token import RefreshToken
from schemas.auth import RegisterRequest,LoginRequest
from sqlalchemy.orm import Session
from database.dependency import get_db
from fastapi import Depends
from core.security import decode_token,create_access_token




def register_user(data:RegisterRequest,db:Session):
    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()
    if existing_user:
        raise ValueError("Email alredy registed")
    user = User(
        username= data.username,
        email= data.email,
        password_hash= hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(data:LoginRequest,db:Session):
   user = db.query(User).filter(
        User.email == data.email
    ).first()
   if not user:
       raise ValueError("Invalid credentials")
   if not verify_password(data.password,user.password_hash):
       raise ValueError(
            "Invalid credentials"
        )
   access_token = create_access_token(userId=user.id)
   refresh_token = create_refresh_token(userId=user.id)
   refresh_token_obj = RefreshToken(
        user_id=user.id,
        token_hash=refresh_token,
        expires_at=datetime.utcnow()
        + timedelta(days=7),
    )
   db.add(refresh_token_obj)
   db.commit()
   return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

def refresh_access_token(db:Session,refresh_token:str):
    payload = decode_token(refresh_token)
    if not payload:
        raise ValueError(
            "Invalid refresh token"
        )
    if  payload.get("type") != "refresh":
        raise ValueError("Invalid  token type")
    token_record = db.query(RefreshToken).filter(RefreshToken.token_hash == refresh_token).first()
    if not token_record:
        raise ValueError("Refresh token not found")
    if token_record.revoked:
        raise ValueError("Refresh token Revoked")
    if token_record.expires_at<datetime.utcnow():
        raise ValueError("Refresh Token expires")
    acces_token = create_access_token(token_record.user_id)
    return {
        "access_token":acces_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }



def logout_user(db:Session,refresh_token:str):
    token_record = db.query(RefreshToken).filter(RefreshToken.token_hash == refresh_token).first()
    if not token_record:
        raise ValueError("Refresh token not found")
    token_record.revoked = True
    db.commit()
    return{
        "message":"logout Successfully"
    }
