import pytest
from pydantic import ValidationError

from app.schemas.login_dto import LoginDTO


def test_valid_login_dto():
    dto = LoginDTO(email="juan@example.com", password="cualquier-cosa")
    assert dto.email == "juan@example.com"


def test_invalid_email_rejected():
    with pytest.raises(ValidationError):
        LoginDTO(email="no-es-un-email", password="123")


def test_missing_password_rejected():
    with pytest.raises(ValidationError):
        LoginDTO(email="juan@example.com")
