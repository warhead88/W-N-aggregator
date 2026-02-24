from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager

from db.tables import Base

from config import Config

DATABASE_URL = f"postgresql+asyncpg://{Config.POSTGRES_USER}:{Config.POSTGRES_PASSWORD}@{Config.POSTGRES_HOST}:{Config.POSTGRES_PORT}/{Config.POSTGRES_DB}"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_async_session():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
