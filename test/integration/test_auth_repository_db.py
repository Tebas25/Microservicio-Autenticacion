import uuid

import pytest
from sqlalchemy import text

from app.core.db_exceptions import EmailAlreadyExists
from app.repositories.auth_repository import AuthRepository


async def test_create_user_persists_with_server_defaults(db_session):
    repo = AuthRepository(db_session)

    user = await repo.create_new_user("a@b.com", "hash", "Nombre Completo")

    assert isinstance(user.id_usuario, uuid.UUID)
    assert user.estado is True
    assert user.creado_en is not None


async def test_duplicate_email_raises_and_session_stays_usable(db_session):
    repo = AuthRepository(db_session)
    await repo.create_new_user("a@b.com", "hash", "Nombre Completo")

    with pytest.raises(EmailAlreadyExists):
        await repo.create_new_user("a@b.com", "otro-hash", "Otro Nombre")

    # Tras el rollback la sesión debe seguir funcionando
    result = await db_session.execute(text("SELECT count(*) FROM usuarios_admin"))
    assert result.scalar() == 1
