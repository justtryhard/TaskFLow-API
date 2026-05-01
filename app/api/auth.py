from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(UserRepository(db))

    try:
        user = await service.create_user(data.email, data.password)
        await db.commit()
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))