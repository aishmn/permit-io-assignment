from sqlalchemy.orm import Session
from db.models.user import User
from core.security import hash_password, verify_password, create_access_token
from core.config import config
from datetime import timedelta

def create_user(db: Session, username: str, password: str):
    hashed_password = hash_password(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def login(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)
    if user:
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    return None


def signup(db: Session, username: str, password: str):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return None
    
    hashed_password = hash_password(password)
    
    new_user = User(username=username, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user