# backend/app/main.py
from fastapi import FastAPI
from api.v1.routes.routes import router
from db.session import engine, Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from permit import Permit

permit = Permit(
    pdp="http://localhost:7766",  
    token="YOUR_PERMIT_API_KEY"    
)


app = FastAPI()

async def get_db():
    async with sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router, prefix="/api/v1")

