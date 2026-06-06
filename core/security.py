from datetime import datetime,timedelta
from jose import jwt,JWTError
from passlib.context import CryptContext
from passlib.hash import bcrypt as bcrypt_hash
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated= "auto"
)

SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

def hash_password(password:str)->str:
    return pwd_context.hash(password)


def verify_password(plain_password:str,hashed_password:str)->bool:
    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        return bcrypt_hash.verify(plain_password, hashed_password)
    return pwd_context.verify(plain_password,hashed_password)


def create_access_token(userId:int)->str:
    expire  = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload ={
        "sub":str(userId),
        "type":"access",
        "exp":expire
    }
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

def create_refresh_token(userId:int)->str:
    expire= datetime.utcnow()+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload ={
        "sub":str(userId),
        "type":"refresh",
        "exp":expire
    }
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

def decode_token(token:str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None
