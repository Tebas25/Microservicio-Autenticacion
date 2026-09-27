import pytest
from pydantic import ValidationError
from app.core.config import get_db_settings


class TestDbSettings:
    def setup_method(self):
        get_db_settings.cache_clear()

    def test_loads_from_env(self, monkeypatch):
        monkeypatch.setenv("DB_USER", "user")
        monkeypatch.setenv("DB_PASSWORD", "pass")
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_PORT", "5432")
        monkeypatch.setenv("DB_NAME", "mydb")
        monkeypatch.setenv("DB_SSL_MODE", "disable")

        settings = get_db_settings()

        assert settings.DB_USER == "user"
        assert settings.DB_PORT == 5432

    def test_database_url_format(self, monkeypatch):
        monkeypatch.setenv("DB_USER", "user")
        monkeypatch.setenv("DB_PASSWORD", "pass")
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_PORT", "5432")
        monkeypatch.setenv("DB_NAME", "mydb")
        monkeypatch.setenv("DB_SSL_MODE", "disable")

        settings = get_db_settings()

        assert settings.database_url == (
            "postgresql+asyncpg://user:pass@localhost:5432/mydb"
        )

    def test_missing_required_var_raises(self, monkeypatch):
        monkeypatch.delenv("DB_USER", raising=False)
        monkeypatch.setenv("DB_PASSWORD", "pass")
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_PORT", "5432")
        monkeypatch.setenv("DB_NAME", "mydb")
        monkeypatch.setenv("DB_SSL_MODE", "disable")

        from app.core.config import DbSettings

        with pytest.raises(ValidationError):
            DbSettings(_env_file=None)
