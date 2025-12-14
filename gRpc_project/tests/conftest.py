import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from server.data.database import Base

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

#@pytest.fixture(scope="function")
@pytest_asyncio.fixture
async def async_session():
    # Create engine
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session factory
    async_session_factory = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    # Provide a session to the test
    async with async_session_factory() as session:
        yield session

    # Drop tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()