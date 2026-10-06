import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.concurrency import run_in_threadpool
from app.core.db_exceptions import InvalidCredentialsError
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_dto import CreateUserDTO
from app.schemas.login_dto import LoginDTO
from app.core.config import Settings
from app.models.user_entity import UsuarioAdmin


class AuthService:
    def __init__(self, auth_repository: AuthRepository, settings: Settings):
        self.auth_repository = auth_repository
        self.settings = settings

    async def create_new_user(self, created_user: CreateUserDTO) -> CreateUserDTO:
        password = created_user.password
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(12)
        hashed = await run_in_threadpool(bcrypt.hashpw, password_bytes, salt)
        password_hash = hashed.decode("utf-8")
        return await self.auth_repository.create_new_user(
            email=created_user.email,
            password_hash=password_hash,
            complete_name=created_user.complete_name,
        )

    async def login_user(self, user: LoginDTO) -> str:
        db_user: UsuarioAdmin = await self.auth_repository.obtain_user_by_email(
            user.email
        )
        if db_user is None or not db_user.estado:
            raise InvalidCredentialsError()

        is_equal = await run_in_threadpool(
            bcrypt.checkpw,
            user.password.encode("utf-8"),
            db_user.password_hash.encode("utf-8"),
        )
        if not is_equal:
            raise InvalidCredentialsError()

        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(db_user.id_usuario),
            "iss": "auth-service",
            "aud": "admin-panel",
            "iat": now,
            "exp": now + timedelta(minutes=self.settings.JWT_EXPIRE_MINUTES),
        }
        return jwt.encode(
            payload, self.settings.private_key, algorithm=self.settings.JWT_ALGORITHM
        )
