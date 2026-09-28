import pytest
from pydantic import ValidationError

from app.schemas.auth_dto import CreateUserDTO

VALID_NAME = "Juan Sebastian Perez Gomez Lopez"


def build(**overrides):
    data = {
        "email": "juan@example.com",
        "password": "Abcdef1!",
        "complete_name": VALID_NAME,
    }
    data.update(overrides)
    return CreateUserDTO(**data)


def test_valid_dto():
    dto = build()
    assert dto.email == "juan@example.com"
    assert dto.password == "Abcdef1!"


@pytest.mark.parametrize(
    "password",
    [
        "abcdef1!",  # sin mayúscula
        "ABCDEF1!",  # sin minúscula
        "Abcdefg!",  # sin número
        "Abcdefg1",  # sin carácter especial
    ],
)
def test_weak_password_rejected(password):
    with pytest.raises(ValidationError, match="contraseña"):
        build(password=password)


@pytest.mark.parametrize("password", ["Ab1!", "Abcdefghijklmnop1!"])
def test_password_length_limits(password):
    with pytest.raises(ValidationError):
        build(password=password)


def test_invalid_email_rejected():
    with pytest.raises(ValidationError):
        build(email="no-es-un-email")


def test_short_name_rejected():
    with pytest.raises(ValidationError):
        build(complete_name="Juan")
