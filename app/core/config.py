from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_SSL_MODE: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@lru_cache
def get_db_settings() -> DbSettings:
    """
    Construye DbSettings de forma perezosa (solo cuando se llama, no al importar
    el módulo) y cachea el resultado (lru_cache) para no releer el entorno en
    cada llamada. En tests se puede limpiar el caché con get_db_settings.cache_clear().
    """
    return DbSettings()
