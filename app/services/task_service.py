from app.models.task import Task, TaskStatus
from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, title: str, description: str | None, user_id: int):
        task = Task(
            title=title,
            description=description,
            user_id=user_id,
            status=TaskStatus.pending.value,
        )
        return await self.repo.create(task)

    async def get_user_tasks(self, user_id: int):
        return await self.repo.get_all_by_user(user_id)

    async def get_task(self, task_id: int, user_id: int):
        return await self.repo.get_by_id(task_id, user_id)

    async def update_task(
        self,
        task_id: int,
        user_id: int,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
    ):
        task = await self.repo.get_by_id(task_id, user_id)

        if not task:
            return None

        if title is not None:
            task.title = title

        if description is not None:
            task.description = description

        if status is not None:
            if status not in {item.value for item in TaskStatus}:
                raise ValueError("Invalid task status")
            task.status = status

        return task

    async def delete_task(self, task_id: int, user_id: int):
        task = await self.repo.get_by_id(task_id, user_id)

        if not task:
            return None

        await self.repo.delete(task)
        return task