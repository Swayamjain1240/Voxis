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
    monkeypatch.setenv("CORS_ORIGINS", "https://voxis.example")

    assert Settings().debug is False


@pytest.mark.parametrize("name,value", [
    ("ENVIRONMENT", "prodution"), ("ALLOWED_HOSTS", "*"),
    ("ALLOWED_HOSTS", "https://localhost"), ("ALLOWED_HOSTS", "localhost:8000"),
    ("HOST", "http://localhost"), ("CORS_ORIGINS", "*"),
    ("CORS_ORIGINS", "http://localhost:abc"), ("CORS_ORIGINS", "http://localhost/path"),
    ("CORS_ORIGINS", "http://user@localhost"), ("CORS_ORIGINS", "null"),
    ("RATE_LIMIT_PER_MINUTE", "0"), ("REQUEST_TIMEOUT_SECONDS", "0"),
    ("MAX_AUDIO_UPLOAD_MB", "51"),
])
def test_invalid_security_configuration_fails_closed(monkeypatch, name, value):
    monkeypatch.setenv(name, value)
    with pytest.raises(ValueError):
        Settings()


def test_production_requires_explicit_https_origins():
    with pytest.raises(ValueError, match="HTTPS"):
        Settings(environment="production", cors_origins=("http://localhost:5173",))
