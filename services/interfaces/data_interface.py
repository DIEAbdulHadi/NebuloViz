from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from models.sales_order import SalesOrder


class DataServiceInterface(ABC):
    """Abstract base class for data services."""

    @abstractmethod
    async def add_sales_order(self, customer_name: str, items: List[Dict], user_id: int) -> SalesOrder:
        pass

    @abstractmethod
    async def get_sales_order(self, order_id: int) -> Optional[SalesOrder]:
        pass

    @abstractmethod
    async def get_all_sales_orders(self, limit: int = 10, offset: int = 0) -> List[SalesOrder]:
        pass

    @abstractmethod
    async def delete_sales_order(self, order_id: int) -> bool:
        pass
