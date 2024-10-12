from fastapi import HTTPException, Depends, Request
from sqlalchemy.future import select
from db.models.user import User
from core.security import hash_password, verify_password, create_access_token
from core.config import config
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
import os

SECRET_KEY = os.getenv("JWT_SECRET")

async def create_user(db: AsyncSession, email: str, password: str, first_name: str, last_name: str, role: str):
    hashed_password = hash_password(password)
    new_user = User(email=email, hashed_password=hashed_password, first_name=first_name, last_name=last_name, role=role)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalar_one_or_none()
    
    if user and verify_password(password, user.hashed_password):
        return user
    return None

async def login(db: AsyncSession, email: str, password: str):
    user = await authenticate_user(db, email, password)
    
    if user:
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    return None

async def signup(db: AsyncSession, email: str, password: str, first_name: str, last_name: str, role: str):
    result = await db.execute(select(User).filter(User.email == email))
    existing_user = result.scalar_one_or_none() 
    
    if existing_user:
        return None
    
    hashed_password = hash_password(password)
    new_user = User(email=email, hashed_password=hashed_password, first_name=first_name, last_name=last_name, role=role)
    
    db.add(new_user)
    await db.commit()  
    await db.refresh(new_user)
    
    return new_user

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
