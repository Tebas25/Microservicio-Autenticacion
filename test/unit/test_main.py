from fastapi.testclient import TestClient
from app.main import app


class TestRootEndpoint:
    def test_root_returns_200(self, monkeypatch):
        monkeypatch.setenv("DB_USER", "user")
        monkeypatch.setenv("DB_PASSWORD", "pass")
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_PORT", "5432")
        monkeypatch.setenv("DB_NAME", "mydb")
        monkeypatch.setenv("DB_SSL_MODE", "disable")

        with TestClient(app) as client:
            response = client.get("/")
            assert response.status_code == 200

    def test_root_returns_expected_payload(self, monkeypatch):
        monkeypatch.setenv("DB_USER", "user")
        monkeypatch.setenv("DB_PASSWORD", "pass")
        monkeypatch.setenv("DB_HOST", "localhost")
        monkeypatch.setenv("DB_PORT", "5432")
        monkeypatch.setenv("DB_NAME", "mydb")
        monkeypatch.setenv("DB_SSL_MODE", "disable")

        with TestClient(app) as client:
            response = client.get("/")
            assert response.json() == {
                "status": "ok",
                "message": "Auth Service en línea. Guardia listo.",
            }
