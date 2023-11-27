import os

import pytest
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from bot.db.base import Base
from bot.db.models import ProductModel, UserModel


@pytest.fixture(scope="module")
async def test_db():
    # Create a new engine instance for test database
    engine = create_async_engine(os.getenv("DB_URL"), echo=True)

    # Create a sessionmaker that yields async sessions
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    # Create test database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    # Drop test database tables after tests are done
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_product(test_db):
    # The async generator needs to be iterated over to yield the session
    async for session in test_db:
        new_product = ProductModel(
            name="Test Product",
            photo_url="http://example.com/photo.jpg",
            price=9.99,
            description="A test product"
        )
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        assert new_product.id is not None


# Test to create a new user
@pytest.mark.asyncio
async def test_create_user(test_db):
    async for session in test_db:
        new_user = UserModel(
            telegram_id=123456789,
            name="Test User",
            username="testuser"
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        assert new_user.id is not None