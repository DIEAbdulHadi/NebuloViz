import pytest
from httpx import AsyncClient
from services.api_service import app
from services.auth_service import AuthService
from services.user_service import UserService

@pytest.mark.asyncio
async def test_endpoint_permission_denied():
    auth_service = AuthService()
    user_service = UserService()

    # Create test user without required permissions
    username = "testuser_no_permission"
    password = "testpassword"
    role = "viewer"
    permissions = []  # No permissions
    new_user = await user_service.create_user(username, password, role, permissions)

    # Get token
    token = auth_service.create_token(new_user.id, role, permissions)

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(
            "/api/v1/orders/",
            json={},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403  # Access forbidden

    # Clean up
    await user_service.delete_user(new_user.id)

@pytest.mark.asyncio
async def test_endpoint_rate_limiting():
    auth_service = AuthService()
    user_service = UserService()

    # Create test user with permissions
    username = "testuser_rate_limit"
    password = "testpassword"
    role = "admin"
    permissions = ["create_order"]
    new_user = await user_service.create_user(username, password, role, permissions)

    # Get token
    token = auth_service.create_token(new_user.id, role, permissions)

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        for _ in range(11):  # Exceed the limit of 10 requests per minute
            response = await client.post(
                "/api/v1/orders/",
                json={"customer_name": "Rate Limit Test", "items": []},
                headers={"Authorization": f"Bearer {token}"}
            )

        assert response.status_code == 429  # Too Many Requests

    # Clean up
    await user_service.delete_user(new_user.id)
