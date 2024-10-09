from typing import AsyncGenerator
from config import DB_HOST, DB_PORT, DB_NAME, DB_PASS, DB_USER
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.asyncio import AsyncSession




from models.models import Food, Set

from sqlalchemy import select


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        print("open")
        yield session
        print("close")
