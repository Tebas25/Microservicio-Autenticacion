from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_db_settings

_VALID_SSL_MODES = {"disable", "allow", "prefer", "require", "verify-ca", "verify-full"}


def get_connection_args(ssl_mode: str) -> dict:
    """Función pura: no depende de DbSettings, no dispara I/O. 100% testeable sin entorno."""
    return {"ssl": ssl_mode} if ssl_mode in _VALID_SSL_MODES else {}


def build_engine():
    """Construye el engine bajo demanda. No se ejecuta al importar el módulo."""
    settings = get_db_settings()
    return create_async_engine(
        settings.database_url,
        echo=True,  # Colocar en False en producción
        connect_args=get_connection_args(settings.DB_SSL_MODE),
    )


class Base(DeclarativeBase):
    pass


engine = None
AsyncSessionLocal = None


def init_engine():
    """Llamar una sola vez al arrancar la app (ej. en el lifespan de FastAPI)."""
    global engine, AsyncSessionLocal
    if engine is None:
        engine = build_engine()
        AsyncSessionLocal = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )
    return engine


async def get_database():
    if AsyncSessionLocal is None:
        init_engine()
    async with AsyncSessionLocal() as session:
        yield session
