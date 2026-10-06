from sqlalchemy import text

from app.db import session as session_module


async def test_engine_can_connect(engine):
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


async def test_session_executes_query(db_session, db_settings):
    result = await db_session.execute(text("SELECT current_database()"))
    assert result.scalar() == db_settings.DB_NAME


async def test_get_database_yields_working_session(engine):
    # `engine` garantiza que la DB y las tablas existen; aquí probamos el
    # generador real de la app (init_engine + AsyncSessionLocal).
    gen = session_module.get_database()
    try:
        session = await gen.__anext__()
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
    finally:
        await gen.aclose()
        await session_module.engine.dispose()
