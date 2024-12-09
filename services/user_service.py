from models.user import User
from utils.permissions import VALID_PERMISSIONS
from utils.async_db import get_async_session
from services.security.security import hash_password
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from utils.logger import app_logger


class UserService:
    """Service for user-related operations."""

    async def create_user(self, username: str, password: str, role: str, permissions: List[str]) -> User:
        """Creates a new user with validated permissions."""
        sanitized_permissions = [perm for perm in permissions if perm in VALID_PERMISSIONS]
        hashed_password = hash_password(password)
        new_user = User(
            username=username,
            hashed_password=hashed_password,
            role=role,
            permissions=sanitized_permissions
        )
        async with get_async_session() as session:
            session.add(new_user)
            try:
                await session.commit()
                await session.refresh(new_user)
                app_logger.info("User created", username=username)
                return new_user
            except IntegrityError:
                await session.rollback()
                app_logger.error("Username already exists", username=username)
                raise ValueError("Username already exists")
