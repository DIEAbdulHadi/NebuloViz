import pytest
from services.ai_insights import AIInsights
from services.data_service import DataService
from unittest.mock import AsyncMock, patch
from pandas import DataFrame

@pytest.mark.asyncio
async def test_predict_sales():
    ai_insights = AIInsights()

    # Mock the training method
    ai_insights.train_sales_forecast_model = AsyncMock()
    ai_insights.sales_model = AsyncMock()
    ai_insights.sales_model.predict = lambda x: [100.0, 110.0]

    future_dates = ["2023-12-01", "2023-12-02"]
    predictions = ai_insights.predict_sales(future_dates)
    assert predictions == [100.0, 110.0]

@pytest.mark.asyncio
async def test_segment_customers():
    ai_insights = AIInsights()

    # Mock the training method
    ai_insights.train_customer_segmentation_model = AsyncMock()
    ai_insights.kmeans_model = AsyncMock()
    ai_insights.kmeans_model.predict = lambda x: [0, 1]

    # Mock data_service to return test orders
    test_orders = [
        AsyncMock(customer_name="Customer A", items=[AsyncMock(quantity=1, price=100.0)]),
        AsyncMock(customer_name="Customer B", items=[AsyncMock(quantity=2, price=50.0)])
    ]

    ai_insights.data_service.get_all_sales_orders = AsyncMock(return_value=test_orders)

    segments = ai_insights.segment_customers()
    assert isinstance(segments, DataFrame)
    assert not segments.empty
