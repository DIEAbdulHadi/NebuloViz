from abc import ABC, abstractmethod
from typing import Optional, Dict, List
from models.user import User


class AuthServiceInterface(ABC):
    """Abstract base class for authentication services."""

    @abstractmethod
    def create_token(self, user_id: int, role: str, permissions: List[str]) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> Optional[Dict]:
        pass

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        pass
