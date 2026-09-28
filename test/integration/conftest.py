import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import app.models.user_entity
from app.core.config import get_db_settings
from app.db.session import Base, get_connection_args
import email_validator
import pytest


@pytest.fixture(autouse=True)
def _no_dns_email_validation(monkeypatch):
    monkeypatch.setattr(email_validator, "CHECK_DELIVERABILITY_DEFAULT", False)


@pytest.fixture
def db_settings():
    settings = get_db_settings()
    if "test" not in settings.DB_NAME.lower():
        pytest.fail(
            f"Las pruebas de integración borran tablas y '{settings.DB_NAME}' "
            "no parece una DB de test. Usa un nombre que contenga 'test'."
        )
    return settings


@pytest_asyncio.fixture
async def engine(db_settings):
    engine = create_async_engine(
        db_settings.database_url,
        connect_args=get_connection_args(db_settings.DB_SSL_MODE),
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
def session_factory(engine):
    return async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture
async def db_session(session_factory):
    async with session_factory() as session:
        yield session
