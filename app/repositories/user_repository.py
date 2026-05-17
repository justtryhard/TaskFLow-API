import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.redis import get_redis

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str):
        cache_key = f"user:{email}"

        # 1. пробуем из Redis
        redis_client = get_redis()
        cached = await redis_client.get(cache_key)
        if cached:
            data = json.loads(cached)
            return User(**data)

        # 2. идём в БД
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        # 3. кладём в кэш
        if user:
            await redis_client.set(
                cache_key,
                json.dumps({
                    "id": user.id,
                    "email": user.email,
                    "hashed_password": user.hashed_password,
                    "is_active": user.is_active,
                }),
                ex=60,  # TTL 60 секунд
            )

        return user

    async def create(self, user: User):
        self.db.add(user)
        await self.db.flush()
        return user