from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import Token, UserCreate, UserLogin, UserRead
from app.services.user_service import UserService
from app.services.rabbit_producer import publish_user_registered


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
        await publish_user_registered(user.email)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login(
    data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(UserRepository(db))
    user = await service.authenticate_user(data.email, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(subject=user.email)

    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
