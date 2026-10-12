import pytest

from app.core.config import Settings, read_bool, read_int


def test_read_int_enforces_safe_bounds(monkeypatch):
    monkeypatch.setenv("PORT", "0")
    with pytest.raises(ValueError, match="PORT"):
        Settings()

    monkeypatch.setenv("PORT", "65536")
    with pytest.raises(ValueError, match="PORT"):
        Settings()


def test_read_bool_rejects_ambiguous_values(monkeypatch):
    monkeypatch.setenv("DEBUG", "sometimes")
    with pytest.raises(ValueError, match="DEBUG"):
        read_bool("DEBUG")


def test_production_debug_is_always_disabled(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("DEBUG", "true")

    assert Settings().debug is False
