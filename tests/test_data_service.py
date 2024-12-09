import pytest
from services.data_service import DataService
from models.sales_order import SalesOrder
from utils.async_db import get_async_session
from sqlalchemy.exc import NoResultFound
from asyncio import sleep

@pytest.mark.asyncio
async def test_add_and_get_sales_order():
    data_service = DataService()
    customer_name = "Test Customer"
    items = [
        {"product_name": "Product A", "quantity": 2, "price": 10.0},
        {"product_name": "Product B", "quantity": 1, "price": 20.0},
    ]
    user_id = 1  # Assuming a test user exists with ID 1

    # Add sales order
    new_order = await data_service.add_sales_order(customer_name, items, user_id)
    assert new_order.customer_name == customer_name
    assert len(new_order.items) == 2

    # Get sales order
    fetched_order = await data_service.get_sales_order(new_order.id)
    assert fetched_order.id == new_order.id

    # Test caching by fetching again (should hit cache)
    fetched_order_cached = await data_service.get_sales_order(new_order.id)
    assert fetched_order_cached.id == new_order.id

    # Clean up test data
    async with get_async_session() as session:
        await session.delete(new_order)
        await session.commit()

@pytest.mark.asyncio
async def test_get_all_sales_orders():
    data_service = DataService()
    # Add multiple orders for testing
    orders_to_add = []
    for i in range(5):
        order = await data_service.add_sales_order(
            f"Customer {i}",
            [{"product_name": f"Product {i}", "quantity": i + 1, "price": 10.0 * (i + 1)}],
            user_id=1
        )
        orders_to_add.append(order)

    orders = await data_service.get_all_sales_orders(limit=5, offset=0)
    assert len(orders) >= 5

    # Clean up test data
    async with get_async_session() as session:
        for order in orders_to_add:
            await session.delete(order)
        await session.commit()

@pytest.mark.asyncio
async def test_delete_sales_order():
    data_service = DataService()
    # Create a test order
    new_order = await data_service.add_sales_order(
        "Delete Test Customer",
        [{"product_name": "Product X", "quantity": 1, "price": 100.0}],
        user_id=1
    )
    # Delete the order
    result = await data_service.delete_sales_order(new_order.id)
    assert result is True

    # Try fetching the deleted order
    fetched_order = await data_service.get_sales_order(new_order.id)
    assert fetched_order is None
