import pytest

from app.core.config import get_db_settings
from app.db import session as session_module
from app.schemas import auth_dto


@pytest.fixture(autouse=True)
def _isolate_global_state():
    def reset():
        get_db_settings.cache_clear()
        session_module.engine = None
        session_module.AsyncSessionLocal = None

    reset()
    yield
    reset()


@pytest.fixture(autouse=True)
def _no_dns_email_validation(monkeypatch):
    """Los tests no deben depender de DNS ni de la red: se mantiene la
    validación de sintaxis pero se desactiva la verificación de entregabilidad."""
    real_validate_email = auth_dto.validate_email

    def offline_validate_email(email, **kwargs):
        kwargs["check_deliverability"] = False
        return real_validate_email(email, **kwargs)

    monkeypatch.setattr(auth_dto, "validate_email", offline_validate_email)
