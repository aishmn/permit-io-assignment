from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from services.auth_service import login, signup
from pydantic import BaseModel, EmailStr
from permit import Permit
import os
import logging

permit = Permit(
      pdp="http://localhost:7766",
      token=os.getenv("PERMIT_API_KEY"),
  )

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str


@router.post("/login")
async def login_user(login_request: LoginRequest, db: Session = Depends(get_db)):
    token = await login(db, login_request.email, login_request.password)

    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return token

@router.post("/signup")
async def signup_user(signup_request: SignupRequest, db: Session = Depends(get_db)):
    user = await signup(
        db, 
        signup_request.email, 
        signup_request.password, 
        signup_request.first_name, 
        signup_request.last_name, 
        signup_request.role
    )

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    try:
        synced_user = await permit.api.users.sync({
            "key": signup_request.email,
            "email": signup_request.email,
            "first_name": signup_request.first_name,
            "last_name": signup_request.last_name,
        })
        logging.info(f"User synced with Permit.io: {synced_user}")

        await permit.api.users.assign_role({
            "user": signup_request.email,
            "role": signup_request.role,
            "tenant": "default",
        })
        
        logging.info(f"Role assigned to user {signup_request.email}: {signup_request.role}")
        
    except Exception as e:
        logging.error(f"Error syncing user with Permit.io: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to sync user with permission service")

    return {"message": "User created successfully"}