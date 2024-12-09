import pytest
from services.auth_service import AuthService
from services.user_service import UserService
from utils.async_db import get_async_session
from models.user import User
from utils.permissions import VALID_PERMISSIONS
from sqlalchemy.exc import IntegrityError

@pytest.mark.asyncio
async def test_create_token():
    auth_service = AuthService()
    user_id = 1
    role = "admin"
    permissions = ["create_order", "view_order"]

    token = auth_service.create_token(user_id, role, permissions)
    assert isinstance(token, str)

def test_verify_token():
    auth_service = AuthService()
    user_id = 1
    role = "admin"
    permissions = ["create_order", "view_order"]

    token = auth_service.create_token(user_id, role, permissions)
    decoded = auth_service.verify_token(token)
    assert decoded["user_id"] == user_id
    assert decoded["role"] == role
    assert decoded["permissions"] == permissions

@pytest.mark.asyncio
async def test_authenticate_user():
    auth_service = AuthService()
    user_service = UserService()

    # Create test user
    username = "testuser_auth"
    password = "testpassword"
    role = "viewer"
    permissions = ["view_order"]

    # Ensure user does not already exist
    async with get_async_session() as session:
        result = await session.execute(
            select(User).where(User.username == username)
        )
        existing_user = result.scalars().first()
        if existing_user:
            await session.delete(existing_user)
            await session.commit()

    new_user = await user_service.create_user(username, password, role, permissions)
    authenticated_user = await auth_service.authenticate_user(username, password)
    assert authenticated_user.username == username

    # Clean up
    async with get_async_session() as session:
        await session.delete(new_user)
        await session.commit()
