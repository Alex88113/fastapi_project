import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


from src.fastapi.shames.user import UserBase
from src.fastapi.configs.user_database_config import user_db_settings

engine = create_async_engine(user_db_settings.USER_DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables() -> None:
    async with engine.begin() as session:
        await session.run_sync(UserBase.metadata.create_all)
 
async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(UserBase.metadata.drop_all)