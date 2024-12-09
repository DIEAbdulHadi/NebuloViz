from typing import Optional, Dict, List
from services.interfaces.auth_interface import AuthServiceInterface
from config.settings import settings
from utils.logger import app_logger
from services.security.security import verify_password
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.async_db import get_async_session
import jwt
from datetime import datetime, timedelta


class AuthService(AuthServiceInterface):
    """Service for authentication-related operations."""

    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.expiry_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_token(self, user_id: int, role: str, permissions: List[str]) -> str:
        """Creates a JWT token for a user."""
        payload = {
            "user_id": user_id,
            "role": role,
            "permissions": permissions,
            "exp": datetime.utcnow() + timedelta(minutes=self.expiry_minutes),
            "iat": datetime.utcnow(),
            "iss": "NebuloViz"
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        app_logger.info("JWT token created", user_id=user_id, role=role)
        return token

    def verify_token(self, token: str) -> Optional[Dict]:
        """Verifies a JWT token and returns the decoded payload."""
        try:
            decoded = jwt.decode(
                token, self.secret_key,
                algorithms=[self.algorithm],
                issuer="NebuloViz"
            )
            app_logger.info("JWT token verified", user_id=decoded.get("user_id"))
            return decoded
        except jwt.ExpiredSignatureError:
            app_logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError:
            app_logger.warning("Invalid JWT token")
            return None
        except Exception as e:
            app_logger.error("Error verifying JWT token", error=str(e))
            return None

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticates a user by username and password."""
        async with get_async_session() as session:
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalars().first()
            if user and verify_password(password, user.hashed_password):
                app_logger.info("User authenticated", username=username)
                return user
            else:
                app_logger.warning("Authentication failed", username=username)
                return None
