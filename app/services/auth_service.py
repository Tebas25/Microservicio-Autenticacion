import bcrypt
from fastapi.concurrency import run_in_threadpool
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_dto import CreateUserDTO


class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

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
