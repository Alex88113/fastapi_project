from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.fastapi.db.database import async_session
from src.fastapi.shames.task_shame import TaskShame, TaskOrm
from src.fastapi.db.database import create_tables

class TaskRepository:
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    async def add_task(self, task: TaskShame) -> None:
        async with self._session_factory() as conn:
            task_orm = TaskOrm(
                title=task.title,
                description=task.description,
                status=task.status
                )
            conn.add(task_orm)
            await conn.commit()
            await conn.refresh(task_orm)
            return task_orm
