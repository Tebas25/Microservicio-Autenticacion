from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRootEndpoint:
    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_expected_payload(self):
        response = client.get("/")
        data = response.json()
        assert data == {
            "status": "ok",
            "message": "Auth Service en línea. Guardia listo.",
        }

    def test_root_content_type_is_json(self):
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
