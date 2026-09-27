from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import db_setting


def get_connection_args(ssl_mode: str) -> dict:
    valid_modes = {"disable", "allow", "prefer", "require", "verify-ca", "verify-full"}
    if ssl_mode in valid_modes:
        return {"ssl": ssl_mode}
    return {}


connect_args = get_connection_args(db_setting.DB_SSL_MODE)

engine = create_async_engine(
    db_setting.database_url,
    echo=True,  # Colocar en False en producción
    connect_args=connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_database():
    async with AsyncSessionLocal() as session:
        yield session
