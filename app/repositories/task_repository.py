from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task: Task):
        self.db.add(task)
        await self.db.flush()
        return task

    async def get_by_id(self, task_id: int, user_id: int):
        result = await self.db.execute(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_all_by_user(self, user_id: int):
        result = await self.db.execute(
            select(Task).where(Task.user_id == user_id)
        )
        return result.scalars().all()

    async def delete(self, task: Task):
        await self.db.delete(task)