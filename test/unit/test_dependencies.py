from unittest.mock import MagicMock

from app.api.dependencies import get_auth_service
from app.core.config import Settings
from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService


def test_get_auth_service_wires_repository_and_settings():
    db = MagicMock()
    settings = MagicMock(spec=Settings)

    service = get_auth_service(db=db, settings=settings)

    assert isinstance(service, AuthService)
    assert isinstance(service.auth_repository, AuthRepository)
    assert service.auth_repository.session is db
    assert service.settings is settings
