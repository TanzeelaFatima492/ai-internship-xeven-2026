import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.db.base import BaseDBModel
from app.core.config import settings

logger = logging.getLogger(__name__)

# Cached engine instance
_async_engine: AsyncEngine | None = None

def get_async_engine() -> AsyncEngine:
    """Return cached async database engine."""
    global _async_engine
    if _async_engine is None:
        _async_engine = create_async_engine(
            settings.database_url,
            future=True,
        )
    return _async_engine

async def get_async_session():
    """Yield an async database session."""
    async_session = async_sessionmaker(
        bind=get_async_engine(),
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise



async def initialize_database() -> None:
    """Create tables if they don't exist yet
    
    This uses a sync connection because the 'create_all' doesn't
    feature async yet.
    """
    async_engine = get_async_engine()
    async with async_engine.begin() as async_conn:
        try:
            await async_conn.run_sync(BaseDBModel.metadata.create_all)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")