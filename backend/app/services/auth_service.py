from sqlalchemy.future import select
from db.models.user import User
from core.security import hash_password, verify_password, create_access_token
from core.config import config
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(db: AsyncSession, username: str, password: str):
    hashed_password = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_password)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()
    
    if user and verify_password(password, user.hashed_password):
        return user
    return None

async def login(db: AsyncSession, username: str, password: str):
    user = await authenticate_user(db, username, password)
    
    if user:
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    return None

async def signup(db: AsyncSession, username: str, password: str):
    
    result = await db.execute(select(User).filter(User.username == username))
    existing_user = result.scalar_one_or_none() 
    
    if existing_user:
        return None
    
    hashed_password = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_password)
    
    db.add(new_user)
    await db.commit()  
    await db.refresh(new_user)
    
    return new_user
