import httpx
import pytest_asyncio
from sqlalchemy import text

from app.db.session import get_database
from app.main import app

URL = "/api/v1/auth/create"
BODY = {
    "email": "juan@example.com",
    "password": "Abcdef1!",
    "complete_name": "Juan Sebastian Perez Gomez Lopez",
}


@pytest_asyncio.fixture
async def client(session_factory):
    async def override_get_database():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_database] = override_get_database
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


async def test_create_user_end_to_end(client, db_session):
    response = await client.post(URL, json=BODY)

    assert response.status_code == 201
    row = (
        await db_session.execute(
            text("SELECT email, password_hash FROM usuarios_admin")
        )
    ).one()
    assert row.email == BODY["email"]
    assert row.password_hash != BODY["password"]
    assert row.password_hash.startswith("$2b$")


async def test_create_user_twice_returns_409(client):
    first = await client.post(URL, json=BODY)
    second = await client.post(URL, json=BODY)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json() == {"detail": "Email ya registrado"}


LOGIN_URL = "/api/v1/auth/login"


class TestLoginEndToEnd:
    async def test_login_succeeds_with_correct_credentials(self, client):
        await client.post("/api/v1/auth/create", json=BODY)

        response = await client.post(
            LOGIN_URL, json={"email": BODY["email"], "password": BODY["password"]}
        )

        assert response.status_code == 200
        assert "access_token" in response.json()

    async def test_login_fails_with_wrong_password(self, client):
        await client.post("/api/v1/auth/create", json=BODY)

        response = await client.post(
            LOGIN_URL, json={"email": BODY["email"], "password": "OtraClave1!"}
        )

        assert response.status_code == 401

    async def test_login_fails_with_unknown_email(self, client):
        response = await client.post(
            LOGIN_URL, json={"email": "no-existe@example.com", "password": "Abcdef1!"}
        )

        assert response.status_code == 401
