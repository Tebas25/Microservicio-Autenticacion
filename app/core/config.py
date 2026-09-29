from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_SSL_MODE: str

    JWT_PRIVATE_KEY_PATH: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def private_key(self) -> str:
        with open(self.JWT_PRIVATE_KEY_PATH, "r") as f:
            return f.read()


@lru_cache
def get_db_settings() -> Settings:
    """
    Construye DbSettings de forma perezosa (solo cuando se llama, no al importar
    el módulo) y cachea el resultado (lru_cache) para no releer el entorno en
    cada llamada. En tests se puede limpiar el caché con get_db_settings.cache_clear().
    """
    return Settings()


@lru_cache
def get_jwt_setting() -> Settings:
    return Settings()
