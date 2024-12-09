import pytest
from services.anomaly_detector import AnomalyDetector
from models.anomaly import Anomaly
from utils.async_db import get_async_session
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_detect_anomaly():
    detector = AnomalyDetector()

    # Mock historical data
    with patch.object(detector, 'get_historical_data', return_value=[100, 105, 110, 95, 90]):
        is_anomaly = await detector.detect_anomaly(150)
        assert is_anomaly is True

        is_anomaly = await detector.detect_anomaly(100)
        assert is_anomaly is False

@pytest.mark.asyncio
async def test_process_data():
    detector = AnomalyDetector()

    # Mock methods
    detector.detect_anomaly = AsyncMock(return_value=True)
    detector.store_anomaly = AsyncMock()
    detector.notification_service.send_anomaly_alert = AsyncMock()

    await detector.process_data(200)

    detector.detect_anomaly.assert_called_once_with(200)
    detector.store_anomaly.assert_awaited_once()
    detector.notification_service.send_anomaly_alert.assert_awaited_once()

@pytest.mark.asyncio
async def test_store_anomaly():
    detector = AnomalyDetector()
    value = 150.0

    await detector.store_anomaly(value)

    # Verify anomaly is stored
    async with get_async_session() as session:
        result = await session.execute(
            "SELECT value FROM anomalies WHERE value = :value", {"value": value}
        )
        anomaly = result.fetchone()
        assert anomaly is not None

        # Clean up
        await session.execute(
            "DELETE FROM anomalies WHERE value = :value", {"value": value}
        )
        await session.commit()
