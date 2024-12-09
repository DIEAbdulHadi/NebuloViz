import numpy as np
from utils.logger import app_logger
from services.notification_service import NotificationService
from services.cache_service import cache
from confluent_kafka import Consumer, KafkaError, TopicPartition
from models.anomaly import Anomaly
from utils.async_db import get_async_session
from config.settings import settings
import asyncio


class AnomalyDetector:
    """Service for detecting anomalies in real-time."""

    def __init__(self):
        self.notification_service = NotificationService()
        self.kafka_consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'group.id': 'anomaly_detector_group',
            'auto.offset.reset': 'earliest',
            'enable.partition.eof': False,
        })
        self.kafka_consumer.subscribe(['sales_data'])

    async def consume_stream(self):
        """Consumes data from Kafka and processes it."""
        while True:
            msg = self.kafka_consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                app_logger.error("Kafka error", error=str(msg.error()))
                continue
            data = float(msg.value().decode('utf-8'))
            await self.process_data(data)

    async def process_data(self, value: float):
        """Processes incoming data and checks for anomalies."""
        is_anomaly = await self.detect_anomaly(value)
        if is_anomaly:
            app_logger.warning("Anomaly detected", value=value)
            await self.store_anomaly(value)
            await self.notification_service.send_anomaly_alert(value)

    async def store_anomaly(self, value: float):
        """Stores the detected anomaly in the database."""
        async with get_async_session() as session:
            anomaly = Anomaly(value=value)
            session.add(anomaly)
            await session.commit()
            app_logger.info("Anomaly stored", value=value)

    @cache.cached(timeout=3600)
    async def get_historical_data(self):
        """Retrieves historical data for adaptive thresholding."""
        # Fetch data from the database
        async with get_async_session() as session:
            result = await session.execute("SELECT value FROM anomalies")
            data = [row[0] for row in result.fetchall()]
            return np.array(data)

    async def calculate_dynamic_threshold(self):
        """Calculates an adaptive threshold based on historical data."""
        data = await self.get_historical_data()
        if data.size == 0:
            return 0.0
        mean = np.mean(data)
        std_dev = np.std(data)
        threshold = mean + (2 * std_dev)  # 95% confidence interval
        return threshold

    async def detect_anomaly(self, current_value: float) -> bool:
        """Detects if the current value is an anomaly."""
        threshold = await self.calculate_dynamic_threshold()
        return current_value > threshold
