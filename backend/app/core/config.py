import os

class Config:
    PERMIT_API_KEY = os.getenv("PERMIT_API_KEY")

config = Config()