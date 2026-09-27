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


class TestCORSConfiguration:
    def test_cors_headers_present_on_preflight(self):
        response = client.options(
            "/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "*"
