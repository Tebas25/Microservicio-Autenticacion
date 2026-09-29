import pytest

from app.core.config import get_db_settings, get_jwt_setting
from app.db import session as session_module
from app.schemas import auth_dto, login_dto


@pytest.fixture(autouse=True)
def _isolate_global_state():
    def reset():
        get_db_settings.cache_clear()
        get_jwt_setting.cache_clear()
        session_module.engine = None
        session_module.AsyncSessionLocal = None

    reset()
    yield
    reset()


@pytest.fixture(autouse=True)
def _no_dns_email_validation(monkeypatch):
    """Sin esto, cada validación de email consulta DNS real."""
    for module in (auth_dto, login_dto):
        real_validate_email = module.validate_email

        def offline_validate_email(email, _real_fn=real_validate_email, **kwargs):
            kwargs["check_deliverability"] = False
            return _real_fn(email, **kwargs)

        monkeypatch.setattr(module, "validate_email", offline_validate_email)
