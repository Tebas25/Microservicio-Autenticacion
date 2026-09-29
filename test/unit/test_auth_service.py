from unittest.mock import AsyncMock

import bcrypt
import jwt
import pytest

from app.core.config import Settings
from app.core.db_exceptions import EmailAlreadyExists, InvalidCredentialsError
from app.models.user_entity import UsuarioAdmin
from app.schemas.auth_dto import CreateUserDTO
from app.schemas.login_dto import LoginDTO
from app.services.auth_service import AuthService


@pytest.fixture
def create_dto():
    return CreateUserDTO(
        email="juan@example.com",
        password="Abcdef1!",
        complete_name="Juan Sebastian Perez Gomez Lopez",
    )


@pytest.fixture
def login_dto():
    return LoginDTO(email="juan@example.com", password="Abcdef1!")


@pytest.fixture
def fast_bcrypt(monkeypatch):
    real_gensalt = bcrypt.gensalt
    monkeypatch.setattr(
        bcrypt, "gensalt", lambda rounds=12, prefix=b"2b": real_gensalt(4, prefix)
    )


JWT_TEST_PUBLIC_KEY = open("test/fixtures/test_jwt_public.pem").read()


@pytest.fixture
def jwt_settings():
    return Settings(
        DB_USER="u",
        DB_PASSWORD="p",
        DB_HOST="h",
        DB_PORT=5432,
        DB_NAME="n",
        DB_SSL_MODE="disable",
        JWT_PRIVATE_KEY_PATH="test/fixtures/test_jwt_private.pem",
        JWT_ALGORITHM="RS256",
        JWT_EXPIRE_MINUTES=30,
    )


def make_db_user(password: str, estado: bool = True) -> UsuarioAdmin:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(4))
    return UsuarioAdmin(
        email="juan@example.com",
        password_hash=hashed.decode("utf-8"),
        nombre_completo="Juan Sebastian Perez Gomez Lopez",
        estado=estado,
    )


class TestCreateNewUser:
    async def test_hashes_password(self, create_dto, fast_bcrypt, jwt_settings):
        repo = AsyncMock()
        repo.create_new_user.return_value = "usuario-creado"
        service = AuthService(repo, jwt_settings)

        result = await service.create_new_user(create_dto)

        kwargs = repo.create_new_user.await_args.kwargs
        assert kwargs["password_hash"] != create_dto.password
        assert bcrypt.checkpw(
            create_dto.password.encode("utf-8"), kwargs["password_hash"].encode("utf-8")
        )
        assert result == "usuario-creado"

    async def test_propagates_email_already_exists(
        self, create_dto, fast_bcrypt, jwt_settings
    ):
        repo = AsyncMock()
        repo.create_new_user.side_effect = EmailAlreadyExists(create_dto.email)
        service = AuthService(repo, jwt_settings)

        with pytest.raises(EmailAlreadyExists):
            await service.create_new_user(create_dto)


class TestLoginUser:
    async def test_returns_valid_jwt_on_success(self, login_dto, jwt_settings):
        repo = AsyncMock()
        repo.obtain_user_by_email.return_value = make_db_user(login_dto.password)
        service = AuthService(repo, jwt_settings)

        token = await service.login_user(login_dto)

        decoded = jwt.decode(
            token, JWT_TEST_PUBLIC_KEY, algorithms=["RS256"], audience="admin-panel"
        )
        assert decoded["iss"] == "auth-service"
        assert decoded["aud"] == "admin-panel"

    async def test_unknown_email_raises_invalid_credentials(
        self, login_dto, jwt_settings
    ):
        repo = AsyncMock()
        repo.obtain_user_by_email.return_value = None
        service = AuthService(repo, jwt_settings)

        with pytest.raises(InvalidCredentialsError):
            await service.login_user(login_dto)

    async def test_inactive_user_raises_invalid_credentials(
        self, login_dto, jwt_settings
    ):
        repo = AsyncMock()
        repo.obtain_user_by_email.return_value = make_db_user(
            login_dto.password, estado=False
        )
        service = AuthService(repo, jwt_settings)

        with pytest.raises(InvalidCredentialsError):
            await service.login_user(login_dto)

    async def test_wrong_password_raises_invalid_credentials(
        self, login_dto, jwt_settings
    ):
        repo = AsyncMock()
        repo.obtain_user_by_email.return_value = make_db_user("OtraClave1!")
        service = AuthService(repo, jwt_settings)

        with pytest.raises(InvalidCredentialsError):
            await service.login_user(login_dto)
