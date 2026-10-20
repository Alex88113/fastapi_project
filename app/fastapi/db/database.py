from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.fastapi.shames.task_shame import Base

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/tasks_db")
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)