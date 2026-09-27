import pytest
from app.db.session import get_connection_args


class TestGetConnectionArgs:
    def test_ssl_disabled_by_default(self):
        assert get_connection_args("disable") == {}

    def test_unknown_mode_returns_empty_dict(self):
        assert get_connection_args("") == {}
        assert get_connection_args("algo_invalido") == {}

    @pytest.mark.parametrize(
        "ssl_mode",
        ["require", "prefer", "allow", "verify-ca", "verify-full"],
    )
    def test_valid_ssl_modes_are_passed_through(self, ssl_mode):
        result = get_connection_args(ssl_mode)
        assert result == {"ssl": ssl_mode}

    def test_ssl_required_mode(self):
        # Regresión: antes devolvía {"ssl": "requiere"} (typo en español)
        assert get_connection_args("require") == {"ssl": "require"}
