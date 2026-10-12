import logging

import pytest
from fastapi import Depends
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.core.security import Principal, require_owner, require_permission, require_principal
from app.main import create_app


@pytest.fixture
def client():
    with TestClient(create_app(Settings(environment="test")), base_url="http://localhost") as value:
        yield value


def assert_safe_error(response, status, code):
    assert response.status_code == status
    assert response.json()["success"] is False
    assert response.json()["error"]["code"] == code
    assert response.headers["x-request-id"] == response.json()["meta"]["request_id"]
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["cache-control"] == "no-store"


@pytest.mark.parametrize("host", ["untrusted.example", "localhost:invalid", "localhost:0", "localhost@evil.example", "localhost?", "localhost:"])
def test_host_is_checked_before_routes(client, host):
    assert_safe_error(client.get("/", headers={"host": host}), 400, "INVALID_HOST")


def test_cors_rejects_unknown_origin_and_credentials(client):
    denied = client.get("/", headers={"origin": "https://untrusted.example"})
    assert_safe_error(denied, 403, "ORIGIN_NOT_ALLOWED")
    assert "access-control-allow-origin" not in denied.headers
    allowed = client.get("/", headers={"origin": "http://localhost:5173"})
    assert allowed.status_code == 200
    assert allowed.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "access-control-allow-credentials" not in allowed.headers
    assert allowed.headers["x-frame-options"] == "DENY"
    assert "frame-ancestors 'none'" in allowed.headers["content-security-policy"]


def test_preflight_allows_only_declared_methods_and_headers(client):
    headers = {"origin": "http://localhost:5173", "access-control-request-method": "POST",
               "access-control-request-headers": "Content-Type"}
    assert client.options("/api/v1/conversation/message", headers=headers).status_code == 204
    headers["access-control-request-method"] = "DELETE"
    assert_safe_error(client.options("/", headers=headers), 400, "INVALID_PREFLIGHT")
    headers["access-control-request-method"] = "POST"
    headers["access-control-request-headers"] = "Authorization"
    assert_safe_error(client.options("/", headers=headers), 400, "INVALID_PREFLIGHT")


def test_rate_limit_cannot_be_bypassed_with_forwarded_header():
    app = create_app(Settings(environment="test", rate_limit_per_minute=2))
    with TestClient(app, base_url="http://localhost") as client:
        assert client.get("/").status_code == 200
        assert client.get("/").status_code == 200
        result = client.get("/", headers={"x-forwarded-for": "different-client"})
        assert_safe_error(result, 429, "RATE_LIMITED")
        assert result.headers["retry-after"] == "60"


def test_json_size_and_compression_limits(client):
    assert_safe_error(client.post("/api/v1/conversation/message", content=b"x" * (1024 * 1024 + 1)),
                      413, "PAYLOAD_TOO_LARGE")
    assert_safe_error(client.post("/", content=b"data", headers={"content-encoding": "gzip"}),
                      415, "UNSUPPORTED_ENCODING")


def test_production_requires_https_without_trusting_forwarded_headers():
    app = create_app(Settings(environment="production", debug=True, cors_origins=("https://voxis.example",)))
    with TestClient(app, base_url="http://localhost") as client:
        assert_safe_error(client.get("/", headers={"x-forwarded-proto": "https"}), 400, "HTTPS_REQUIRED")
    with TestClient(app, base_url="https://localhost") as client:
        result = client.get("/")
        assert result.status_code == 200
        assert result.headers["strict-transport-security"] == "max-age=31536000"
        assert client.get("/openapi.json").status_code == 404


def test_unexpected_errors_and_logs_do_not_expose_private_details(client, caplog):
    @client.app.get("/crash")
    def crash():
        raise RuntimeError("private-transcript-and-secret")

    with caplog.at_level(logging.INFO, logger="voxis.security"):
        response = client.get("/crash?text=private-transcript-and-secret")
    assert_safe_error(response, 500, "INTERNAL_ERROR")
    assert "private-transcript-and-secret" not in response.text
    security_logs = [record.message for record in caplog.records if record.name == "voxis.security"]
    assert security_logs and "private-transcript-and-secret" not in "".join(security_logs)


def test_private_route_dependencies_fail_closed(client):
    @client.app.get("/private/{owner}")
    def private(owner: str, principal=Depends(require_permission("read"))):
        require_owner(principal, owner)
        return {"ok": True}

    for headers in ({}, {"authorization": "Bearer invented", "x-user-id": "me"}):
        assert_safe_error(client.get("/private/me", headers=headers), 401, "UNAUTHORIZED")

    # A verifier is substituted only inside this test; no login exists in Mode 1.
    client.app.dependency_overrides[require_principal] = lambda: Principal("me", frozenset())
    assert_safe_error(client.get("/private/me"), 403, "FORBIDDEN")
    client.app.dependency_overrides[require_principal] = lambda: Principal("me", frozenset({"read"}))
    assert client.get("/private/me").status_code == 200
    assert_safe_error(client.get("/private/someone-else"), 403, "FORBIDDEN")
