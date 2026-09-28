from unittest.mock import MagicMock

from app.api.dependencies import get_auth_service
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService


def test_get_auth_service_wires_repository_with_session():
    db = MagicMock()

    service = get_auth_service(db=db)

    assert isinstance(service, AuthService)
    assert isinstance(service.auth_repository, AuthRepository)
    assert service.auth_repository.session is db
