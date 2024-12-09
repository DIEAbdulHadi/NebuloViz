from sqlalchemy import Column, Integer, String, JSON
from models.base import Base


class User(Base):
    """User model representing application users."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="viewer")
    permissions = Column(JSON)  # Specific permissions
    preferences = Column(JSON)  # User preferences
