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


db_setting = DbSettings()
