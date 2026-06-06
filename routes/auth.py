from fastapi import APIRouter,Depends,HTTPException

from sqlalchemy.orm import Session
from database.dependency import get_db
from schemas.auth import RegisterRequest,LoginRequest,UserResponse,TokenResponse,RefreshRequest,LogoutRequest
from services.auth_services import register_user,login_user,refresh_access_token,logout_user
from fastapi.security import OAuth2PasswordRequestForm
from core.dependencies import get_current_user
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", response_model=UserResponse,)
def register(
    data:RegisterRequest,
    db:Session=Depends(get_db),

):
    try:
        return register_user(data,db)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@router.post("/login",response_model=TokenResponse)
def login(form_data:OAuth2PasswordRequestForm=Depends(),
          db:Session=Depends(get_db)):
    try:
        data = LoginRequest(
           email= form_data.username,
            password=form_data.password
        )


        return login_user(data,db)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.get("/me", response_model=UserResponse,)
def me(current_user=Depends( get_current_user)):
    return current_user


@router.post("/refresh",response_model=TokenResponse)
def refresh(request:RefreshRequest,db:Session=Depends(get_db)):
    try:
        return refresh_access_token(db,request.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.post("/logout")
def logout(request:LogoutRequest,db:Session=Depends(get_db)):
    try:
        return logout_user(db,request.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


    