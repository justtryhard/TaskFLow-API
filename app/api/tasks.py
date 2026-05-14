from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead)
async def create_task(
    data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(TaskRepository(db))

    task = await service.create_task(
        title=data.title,
        description=data.description,
        user_id=current_user.id,
    )

    await db.commit()
    return task


@router.get("", response_model=list[TaskRead])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(TaskRepository(db))
    return await service.get_user_tasks(current_user.id)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(TaskRepository(db))
    task = await service.get_task(task_id, current_user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(TaskRepository(db))

    try:
        task = await service.update_task(
            task_id=task_id,
            user_id=current_user.id,
            title=data.title,
            description=data.description,
            status=data.status,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.commit()
    return task


@router.delete("/{task_id}", response_model=TaskRead)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TaskService(TaskRepository(db))
    task = await service.delete_task(task_id, current_user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.commit()
    return task