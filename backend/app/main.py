from fastapi import FastAPI
from api.v1.routes.routes import router
from db.session import engine, Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import os 
from fastapi.middleware.cors import CORSMiddleware

from permit import Permit

permit = Permit(
      pdp=os.getenv('PERMIT_PDP_URL'),
      token=os.getenv("PERMIT_API_KEY"),
  )

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



async def get_db():
    async with sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router, prefix="/api/v1")

