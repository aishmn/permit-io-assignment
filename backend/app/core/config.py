import os

class Config:
    PERMIT_API_KEY = os.getenv("PERMIT_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
