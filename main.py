from fastapi import FastAPI
from services.api_service import app as api_app
from config.settings import settings

app = FastAPI(
    title="NebuloViz",
    description="Advanced Sales Dashboard",
    version="1.0.0"
)

# Include the API router
app.mount("/api/v1", api_app)

# Add any additional middleware, event handlers, etc.
