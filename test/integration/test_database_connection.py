import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_engine_can_connect(engine):
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_session_executes_query(db_session):
    result = await db_session.execute(text("SELECT current_database()"))
    db_name = result.scalar()
    assert db_name == "auth_test_db"
