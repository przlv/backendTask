import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

load_dotenv("python_env.env")

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = (
    f"postgresql+asyncpg://" f"{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
)
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def close_db_connection():
    await engine.dispose()
