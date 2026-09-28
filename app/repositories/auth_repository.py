# from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_entity import UsuarioAdmin
from sqlalchemy.exc import IntegrityError
from app.core.db_exceptions import EmailAlreadyExists


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_new_user(
        self, email: str, password_hash: str, complete_name: str
    ) -> UsuarioAdmin | None:
        new_user = UsuarioAdmin(
            email=email, password_hash=password_hash, nombre_completo=complete_name
        )
        self.session.add(new_user)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise EmailAlreadyExists(email)
        await self.session.refresh(new_user)
        return new_user
