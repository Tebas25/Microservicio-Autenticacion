from app.db import session as session_module


class TestBuildEngine:
    def test_build_engine_returns_engine(self, monkeypatch):
        monkeypatch.setenv("DB_USER", "user")
        monkeypatch.setenv("DB_PASSWORD", "pass")
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_PORT", "5432")
        monkeypatch.setenv("DB_NAME", "mydb")
        monkeypatch.setenv("DB_SSL_MODE", "disable")
        session_module.get_db_settings.cache_clear()

        engine = session_module.build_engine()

        assert engine is not None
        assert "mydb" in str(engine.url)


class TestInitEngine:
    def setup_method(self):
        session_module.engine = None
        session_module.AsyncSessionLocal = None

    def test_init_engine_sets_globals(self, monkeypatch):
        monkeypatch.setenv("DB_USER", "user")
        monkeypatch.setenv("DB_PASSWORD", "pass")
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_PORT", "5432")
        monkeypatch.setenv("DB_NAME", "mydb")
        monkeypatch.setenv("DB_SSL_MODE", "disable")
        session_module.get_db_settings.cache_clear()

        result = session_module.init_engine()

        assert session_module.engine is not None
        assert session_module.AsyncSessionLocal is not None
        assert result is session_module.engine

    def test_init_engine_is_idempotent(self, monkeypatch):
        monkeypatch.setenv("DB_USER", "user")
        monkeypatch.setenv("DB_PASSWORD", "pass")
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_PORT", "5432")
        monkeypatch.setenv("DB_NAME", "mydb")
        monkeypatch.setenv("DB_SSL_MODE", "disable")
        session_module.get_db_settings.cache_clear()

        first = session_module.init_engine()
        second = session_module.init_engine()

        assert first is second  # no crea un segundo engine
