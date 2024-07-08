from app.config import config
from app.models import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(config.db_url)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

__all__ = ['engine', 'async_session']
