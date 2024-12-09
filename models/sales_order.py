from sqlalchemy import Column, Integer, String, ForeignKey, Float, Index, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


class SalesOrder(Base):
    """SalesOrder model representing a sales order."""

    __tablename__ = "sales_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    items = relationship("SalesOrderLine", back_populates="order", cascade="all, delete-orphan")


class SalesOrderLine(Base):
    """SalesOrderLine model representing items within a sales order."""

    __tablename__ = "sales_order_lines"

    id = Column(Integer, primary_key=True, index=True)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"))
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order = relationship("SalesOrder", back_populates="items")
