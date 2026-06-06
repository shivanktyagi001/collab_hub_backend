from pydantic import BaseModel,EmailStr

class RegisterRequest(BaseModel):
    email:EmailStr
    username:str
    password:str


class LoginRequest(BaseModel):
    email:EmailStr
    password:str


class RefreshRequest(BaseModel):
    refresh_token:str
class LogoutRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    username:str
    model_config = {
        "from_attributes": True
    }


class TokenResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str = "bearer"