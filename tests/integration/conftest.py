import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import DbSettings


@pytest.fixture(scope="session")
def db_settings() -> DbSettings:
    return DbSettings()


@pytest_asyncio.fixture(scope="session")
async def engine(db_settings):
    engine = create_async_engine(db_settings.database_url, echo=False)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine):
    session_local = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_local() as session:
        yield session
