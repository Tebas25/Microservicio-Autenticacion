import pytest
from pydantic import ValidationError

from app.core.config import Settings, get_db_settings, get_jwt_setting

ENV = {
    "DB_USER": "user",
    "DB_PASSWORD": "pass",
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
    "DB_NAME": "mydb",
    "DB_SSL_MODE": "disable",
    "JWT_PRIVATE_KEY_PATH": "test/fixtures/test_jwt_private.pem",
    "JWT_ALGORITHM": "RS256",
    "JWT_EXPIRE_MINUTES": "30",
}


def set_env(monkeypatch, **overrides):
    values = {**ENV, **overrides}
    for key, value in values.items():
        monkeypatch.setenv(key, value)


class TestSettings:
    def test_loads_from_env(self, monkeypatch):
        set_env(monkeypatch)
        settings = get_db_settings()

        assert settings.DB_USER == "user"
        assert settings.DB_PORT == 5432
        assert settings.JWT_ALGORITHM == "RS256"
        assert settings.JWT_EXPIRE_MINUTES == 30

    def test_database_url_format(self, monkeypatch):
        set_env(monkeypatch)
        settings = get_db_settings()

        assert settings.database_url == (
            "postgresql+asyncpg://user:pass@localhost:5432/mydb"
        )

    def test_private_key_reads_file(self, monkeypatch, tmp_path):
        key_file = tmp_path / "key.pem"
        key_file.write_text("contenido-de-prueba")
        set_env(monkeypatch, JWT_PRIVATE_KEY_PATH=str(key_file))

        settings = get_jwt_setting()

        assert settings.private_key == "contenido-de-prueba"

    def test_get_db_settings_and_get_jwt_setting_share_values(self, monkeypatch):
        set_env(monkeypatch)

        assert get_db_settings().DB_USER == get_jwt_setting().DB_USER

    def test_missing_required_var_raises(self, monkeypatch):
        set_env(monkeypatch)
        monkeypatch.delenv("DB_USER", raising=False)

        with pytest.raises(ValidationError):
            Settings(_env_file=None)
