# utils/async_db.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# Replace 'postgresql://' with 'postgresql+asyncpg://' for async support
async_engine = create_async_engine(
    settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://'),
    echo=False,
    future=True
)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    """Provides a new asynchronous database session."""
    async with AsyncSessionLocal() as session:
        yield session
