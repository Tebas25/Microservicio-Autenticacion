from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_auth_service
from app.core.db_exceptions import EmailAlreadyExists
from app.main import app

URL = "/api/v1/auth/create"
VALID_BODY = {
    "email": "juan@example.com",
    "password": "Abcdef1!",
    "complete_name": "Juan Sebastian Perez Gomez Lopez",
}


@pytest.fixture
def service():
    return AsyncMock()


@pytest.fixture
def client(service):
    app.dependency_overrides[get_auth_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_user_returns_201(client, service):
    response = client.post(URL, json=VALID_BODY)

    assert response.status_code == 201
    assert response.json() == {"mensaje": "Usuario creado con éxito"}
    service.create_new_user.assert_awaited_once()


def test_create_user_duplicate_email_returns_409(client, service):
    service.create_new_user.side_effect = EmailAlreadyExists("juan@example.com")

    response = client.post(URL, json=VALID_BODY)

    assert response.status_code == 409
    assert response.json() == {"detail": "Email ya registrado"}


@pytest.mark.parametrize(
    "override",
    [
        {"email": "no-es-email"},
        {"password": "debil"},
        {"complete_name": "Juan"},
    ],
)
def test_create_user_invalid_body_returns_422(client, service, override):
    response = client.post(URL, json={**VALID_BODY, **override})

    assert response.status_code == 422
    service.create_new_user.assert_not_awaited()


def test_create_user_missing_field_returns_422(client, service):
    body = {k: v for k, v in VALID_BODY.items() if k != "email"}

    response = client.post(URL, json=body)

    assert response.status_code == 422
