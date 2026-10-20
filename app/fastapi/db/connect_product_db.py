import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.fastapi.shames.product import Base

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@database:5432/products_db")
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def get_session():
    async with async_session() as session:
        yield session