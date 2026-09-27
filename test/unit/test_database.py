import pytest
from app.db.session import get_connection_args


class TestGetConnectionArgs:
    def test_unknown_mode_returns_empty_dict(self):
        assert get_connection_args("") == {}
        assert get_connection_args("algo_invalido") == {}

    @pytest.mark.parametrize(
        "ssl_mode",
        ["disable", "allow", "prefer", "require", "verify-ca", "verify-full"],
    )
    def test_valid_ssl_modes_are_passed_through(self, ssl_mode):
        assert get_connection_args(ssl_mode) == {"ssl": ssl_mode}
