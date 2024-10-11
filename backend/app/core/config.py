import os

class Config:
    PERMIT_API_KEY = os.getenv("PERMIT_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MIN", 10)
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    SECRET_KEY = os.getenv("JWT_SECRET", "JWT_SECRET_ACCESS_TOKEN")

config = Config()