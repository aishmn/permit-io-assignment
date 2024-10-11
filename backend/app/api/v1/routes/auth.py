from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from services.auth_service import login, signup
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str



class SignupRequest(BaseModel):
    username: str
    password: str

    
@router.post("/login")
async def login_user(login_request: LoginRequest, db: Session = Depends(get_db)):
    token = await login(db, login_request.username, login_request.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return token


@router.post("/signup")
async def signup_user(signup_request: SignupRequest, db: Session = Depends(get_db)):
    user = await signup(db, signup_request.username, signup_request.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return {"message": "User created successfully"}