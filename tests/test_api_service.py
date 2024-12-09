import pytest
from httpx import AsyncClient
from services.api_service import app
from services.auth_service import AuthService
from services.user_service import UserService

@pytest.mark.asyncio
async def test_create_order_endpoint():
    auth_service = AuthService()
    user_service = UserService()

    # Create test user
    username = "testuser_api"
    password = "testpassword"
    role = "admin"
    permissions = ["create_order"]
    new_user = await user_service.create_user(username, password, role, permissions)

    # Get token
    token = auth_service.create_token(new_user.id, role, permissions)

    order_payload = {
        "customer_name": "API Test Customer",
        "items": [
            {"product_name": "Product A", "quantity": 2, "price": 10.0},
            {"product_name": "Product B", "quantity": 1, "price": 20.0}
        ]
    }

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(
            "/api/v1/orders/",
            json=order_payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "order_id" in data

    # Clean up
    await user_service.delete_user(new_user.id)

@pytest.mark.asyncio
async def test_predict_sales_endpoint():
    auth_service = AuthService()
    user_service = UserService()

    # Create test user
    username = "testuser_api_predict"
    password = "testpassword"
    role = "viewer"
    permissions = ["view_predictions"]
    new_user = await user_service.create_user(username, password, role, permissions)

    # Get token
    token = auth_service.create_token(new_user.id, role, permissions)

    future_dates = ["2023-12-01", "2023-12-02"]

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get(
            "/api/v1/ai/predict-sales/",
            params={"future_dates": future_dates},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data

    # Clean up
    await user_service.delete_user(new_user.id)
