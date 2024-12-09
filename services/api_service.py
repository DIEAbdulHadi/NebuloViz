from fastapi import FastAPI, Depends, HTTPException, status, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from services.auth_service import AuthService
from services.data_service import DataService
from services.ai_insights import AIInsights
from pydantic import BaseModel, Field
from utils.logger import app_logger
from typing import List, Dict
from config.settings import settings
import aioredis

# Versioned API prefix
API_VERSION = "/api/v1"

app = FastAPI(
    title="NebuloViz API",
    version="1.0.0",
    description="API documentation for NebuloViz.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS settings
origins = ["*"]  # Update with allowed origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize rate limiter
@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool(settings.REDIS_URL)
    await FastAPILimiter.init(redis)

auth_service = AuthService()
data_service = DataService()
ai_insights = AIInsights()


class Item(BaseModel):
    product_name: str = Field(..., example="Widget A")
    quantity: int = Field(..., example=10)
    price: float = Field(..., example=99.99)


class SalesOrderRequest(BaseModel):
    customer_name: str = Field(..., example="John Doe")
    items: List[Item]


def get_current_user(authorization: str = Header(None)):
    """Retrieves the current authenticated user based on the JWT token."""
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    token = authorization.split(" ")[1]
    decoded = auth_service.verify_token(token)
    if decoded is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return decoded


def has_permission(user, required_permissions: List[str]) -> bool:
    """Checks if the user has the required permissions."""
    return set(required_permissions).issubset(set(user.get('permissions', [])))


def requires_permissions(required_permissions: List[str]):
    """Decorator to enforce permission-based access control."""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            user = get_current_user()
            if not has_permission(user, required_permissions):
                raise HTTPException(status_code=403, detail="Access forbidden")
            return await func(*args, **kwargs)
        return wrapper

    return decorator


@app.post(
    API_VERSION + "/orders/",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    response_model=Dict[str, int],
    summary="Create a new sales order",
    description="Creates a new sales order with the provided customer name and items."
)
@requires_permissions(["create_order"])
async def create_order(order: SalesOrderRequest, user=Depends(get_current_user)):
    """Creates a new sales order."""
    try:
        new_order = await data_service.add_sales_order(
            order.customer_name,
            [item.dict() for item in order.items],
            user_id=user["user_id"]
        )
        return {"order_id": new_order.id}
    except Exception as e:
        app_logger.error("Error creating order", error=str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    API_VERSION + "/ai/predict-sales/",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    response_model=Dict[str, List[float]],
    summary="Predict future sales",
    description="Predicts future sales based on provided dates."
)
@requires_permissions(["view_predictions"])
async def predict_sales(future_dates: List[str], user=Depends(get_current_user)):
    """Predicts future sales based on provided dates."""
    try:
        predictions = ai_insights.predict_sales(future_dates)
        return {"predictions": predictions}
    except Exception as e:
        app_logger.error("Error predicting sales", error=str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    API_VERSION + "/ai/segment-customers/",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    response_model=List[Dict],
    summary="Segment customers",
    description="Segments customers using clustering algorithms."
)
@requires_permissions(["view_segments"])
async def segment_customers(user=Depends(get_current_user)):
    """Segments customers using clustering algorithms."""
    try:
        segments = ai_insights.segment_customers()
        return segments.to_dict(orient='records')
    except Exception as e:
        app_logger.error("Error segmenting customers", error=str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
