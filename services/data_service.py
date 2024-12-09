from services.interfaces.data_interface import DataServiceInterface
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.settings import settings
from utils.logger import app_logger
from typing import Optional, List, Dict
from models.sales_order import SalesOrder, SalesOrderLine
from services.cache_service import cache
from utils.async_db import get_async_session
from functools import wraps


def service_error_handler(func):
    """Decorator for centralized error handling in services."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            app_logger.error(f"Error in {func.__name__}", error=str(e))
            raise

    return wrapper


class DataService(DataServiceInterface):
    """Service for data-related operations using async operations."""

    @service_error_handler
    async def add_sales_order(self, customer_name: str, items: List[Dict], user_id: int) -> SalesOrder:
        """Adds a new sales order to the database."""
        async with get_async_session() as session:
            new_order = SalesOrder(customer_name=customer_name, user_id=user_id)
            for item in items:
                order_line = SalesOrderLine(
                    product_name=item['product_name'],
                    quantity=item['quantity'],
                    price=item['price']
                )
                new_order.items.append(order_line)
            session.add(new_order)
            await session.commit()
            await session.refresh(new_order)
            await cache.invalidate(["get_sales_order"])
            await cache.invalidate(["get_sales_orders"])
            app_logger.info("Sales order added", order_id=new_order.id, customer_name=customer_name)
            return new_order

    @service_error_handler
    @cache.cached(timeout=60)
    async def get_sales_order(self, order_id: int) -> Optional[SalesOrder]:
        """Retrieves a sales order by ID, with caching."""
        async with get_async_session() as session:
            result = await session.execute(select(SalesOrder).where(SalesOrder.id == order_id))
            order = result.scalars().first()
            if order:
                app_logger.info("Sales order retrieved", order_id=order_id)
            else:
                app_logger.warning("Sales order not found", order_id=order_id)
            return order

    @service_error_handler
    @cache.cached(timeout=60)
    async def get_all_sales_orders(self, limit: int = 10, offset: int = 0) -> List[SalesOrder]:
        """Retrieves all sales orders with pagination."""
        async with get_async_session() as session:
            result = await session.execute(select(SalesOrder).offset(offset).limit(limit))
            orders = result.scalars().all()
            app_logger.info("Retrieved sales orders", count=len(orders))
            return orders

    @service_error_handler
    async def delete_sales_order(self, order_id: int) -> bool:
        """Deletes a sales order by ID."""
        async with get_async_session() as session:
            result = await session.execute(select(SalesOrder).where(SalesOrder.id == order_id))
            order = result.scalars().first()
            if order:
                await session.delete(order)
                await session.commit()
                await cache.invalidate(["get_sales_order", str(order_id)])
                app_logger.info("Sales order deleted", order_id=order_id)
                return True
            else:
                app_logger.warning("Sales order to delete not found", order_id=order_id)
                return False
