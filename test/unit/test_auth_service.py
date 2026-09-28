from unittest.mock import AsyncMock

import bcrypt
import pytest

from app.core.db_exceptions import EmailAlreadyExists
from app.schemas.auth_dto import CreateUserDTO
from app.services.auth_service import AuthService


@pytest.fixture
def dto():
    return CreateUserDTO(
        email="juan@example.com",
        password="Abcdef1!",
        complete_name="Juan Sebastian Perez Gomez Lopez",
    )


@pytest.fixture
def fast_bcrypt(monkeypatch):
    real_gensalt = bcrypt.gensalt
    monkeypatch.setattr(
        bcrypt, "gensalt", lambda rounds=12, prefix=b"2b": real_gensalt(4, prefix)
    )


async def test_create_new_user_hashes_password(dto, fast_bcrypt):
    repo = AsyncMock()
    repo.create_new_user.return_value = "usuario-creado"
    service = AuthService(repo)

    result = await service.create_new_user(dto)

    kwargs = repo.create_new_user.await_args.kwargs
    assert kwargs["email"] == dto.email
    assert kwargs["complete_name"] == dto.complete_name
    assert kwargs["password_hash"] != dto.password
    assert bcrypt.checkpw(
        dto.password.encode("utf-8"), kwargs["password_hash"].encode("utf-8")
    )
    assert result == "usuario-creado"


async def test_create_new_user_propagates_email_already_exists(dto, fast_bcrypt):
    repo = AsyncMock()
    repo.create_new_user.side_effect = EmailAlreadyExists(dto.email)
    service = AuthService(repo)

    with pytest.raises(EmailAlreadyExists):
        await service.create_new_user(dto)
