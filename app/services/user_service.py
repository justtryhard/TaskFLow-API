from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, email: str, password: str):
        existing_user = await self.repo.get_by_email(email)
        if existing_user:
            raise ValueError("User already exists")

        user = User(
            email=email,
            hashed_password=hash_password(password),
        )

        return await self.repo.create(user)