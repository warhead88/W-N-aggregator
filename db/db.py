from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager

from db.tables import Base

DATABASE_URL = "sqlite+aiosqlite:///./main.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
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
async def get_async_sesion():
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
