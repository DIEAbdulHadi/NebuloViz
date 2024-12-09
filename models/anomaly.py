from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from models.base import Base


class Anomaly(Base):
    """Model for storing detected anomalies."""

    __tablename__ = 'anomalies'

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    detected_at = Column(DateTime, default=datetime.utcnow)
