import asyncio
import json
import logging
from time import monotonic
from urllib.parse import urlsplit

from starlette.datastructures import Headers, MutableHeaders
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import PRODUCTION_ENVIRONMENTS
from app.core.cors import ALLOWED_HEADERS, ALLOWED_METHODS, cors_headers
from app.core.exceptions import VOXISHTTPException, http_exception_handler, unhandled_exception_handler
from app.core.limits import WindowRateLimiter


logger = logging.getLogger("voxis.security")
JSON_LIMIT = 1024 * 1024
MAX_INFLIGHT = 8


def valid_host(headers, settings):
    host = headers.get("host", "")
    if (len(headers.getlist("host")) != 1 or any(char.isspace() for char in host) or
            any(char in host for char in "\\/@?#") or host.endswith(":")):
        return False
    try:
        parsed = urlsplit("http://" + host)
        return (parsed.hostname in settings.allowed_hosts and parsed.port != 0 and not parsed.username and
                not parsed.password and not parsed.path and not parsed.query and
                not parsed.fragment)
    except ValueError:
        return False


class TransportMiddleware:
    def __init__(self, app, settings):
        self.app = app
        self.settings = settings
        self.limiter = WindowRateLimiter(settings.rate_limit_per_minute)
        self.inflight = 0

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = Headers(scope=scope)
        origin = headers.get("origin")
        request = Request(scope)
        status = 500
        started = False
        began = monotonic()
        production = self.settings.environment in PRODUCTION_ENVIRONMENTS

        async def secure_send(message):
            nonlocal status, started
            if message["type"] == "http.response.start":
                started = True
                status = message["status"]
                response_headers = MutableHeaders(scope=message)
                response_headers.update({
                    "x-content-type-options": "nosniff",
                    "x-frame-options": "DENY",
                    "referrer-policy": "no-referrer",
                    "cache-control": "no-store",
                    "content-security-policy": "default-src 'none'; frame-ancestors 'none'; base-uri 'none'",
                    "permissions-policy": "camera=(), microphone=(), geolocation=()",
                    **cors_headers(origin, self.settings),
                })
                if production and scope["scheme"] == "https":
                    response_headers["strict-transport-security"] = "max-age=31536000"
            await send(message)

        async def fail(code, message, status_code, retry=False):
            response = http_exception_handler(request, VOXISHTTPException(status_code, code, message))
            if retry:
                response.headers["retry-after"] = "60"
            await response(scope, receive, secure_send)

        try:
            if not valid_host(headers, self.settings):
                return await fail("INVALID_HOST", "Host is not allowed.", 400)
            if production and scope["scheme"] != "https":
                return await fail("HTTPS_REQUIRED", "HTTPS is required.", 400)
            if len(headers.getlist("origin")) > 1 or (origin is not None and origin not in self.settings.cors_origins):
                return await fail("ORIGIN_NOT_ALLOWED", "Origin is not allowed.", 403)
            peer = scope.get("client")
            if not self.limiter.allow(peer[0] if peer else "local"):
                return await fail("RATE_LIMITED", "Request quota exceeded.", 429, retry=True)
            if scope["method"] == "OPTIONS":
                requested_method = headers.get("access-control-request-method", "")
                requested_headers = {value.strip().lower() for value in headers.get("access-control-request-headers", "").split(",") if value.strip()}
                if origin is None or requested_method not in ALLOWED_METHODS or not requested_headers <= ALLOWED_HEADERS:
                    return await fail("INVALID_PREFLIGHT", "CORS preflight is not allowed.", 400)
                return await Response(status_code=204)(scope, receive, secure_send)
            if self.inflight >= MAX_INFLIGHT:
                return await fail("SERVICE_BUSY", "The service is busy.", 503)

            upload = scope["path"] in {"/api/v1/speech/upload", "/api/v1/speech/transcribe"}
            limit = self.settings.max_audio_upload_mb * 1024 * 1024 + 65536 if upload else JSON_LIMIT
            length = headers.get("content-length")
            if length is not None:
                if len(headers.getlist("content-length")) != 1 or not length.isascii() or not length.isdigit():
                    return await fail("INVALID_REQUEST", "Invalid Content-Length.", 400)
                if len(length) > 10 or int(length) > limit:
                    return await fail("PAYLOAD_TOO_LARGE", "Request body exceeds the limit.", 413)
            encoding = headers.get("content-encoding", "identity").lower()
            if encoding != "identity":
                return await fail("UNSUPPORTED_ENCODING", "Compressed request bodies are not supported.", 415)

            self.inflight += 1
            try:
                async def process():
                    body = bytearray()
                    while True:
                        message = await receive()
                        if message["type"] == "http.disconnect":
                            return
                        chunk = message.get("body", b"")
                        if len(body) + len(chunk) > limit:
                            return await fail("PAYLOAD_TOO_LARGE", "Request body exceeds the limit.", 413)
                        body.extend(chunk)
                        if not message.get("more_body", False):
                            break
                    supplied = False
                    if length is not None and int(length) != len(body):
                        return await fail("INVALID_REQUEST", "Content-Length does not match the body.", 400)

                    async def bounded_receive():
                        nonlocal supplied
                        if supplied:
                            return await receive()
                        supplied = True
                        return {"type": "http.request", "body": bytes(body), "more_body": False}

                    await self.app(scope, bounded_receive, secure_send)

                await asyncio.wait_for(process(), timeout=self.settings.request_timeout_seconds)
            finally:
                self.inflight -= 1
        except asyncio.TimeoutError:
            if not started:
                await fail("REQUEST_TIMEOUT", "Request exceeded the time limit.", 408)
        except Exception:
            if started:
                raise
            await unhandled_exception_handler(request, None)(scope, receive, secure_send)
        finally:
            # No URLs, query strings, payloads, IP addresses, credentials or tracebacks.
            logger.info(json.dumps({
                "event": "http_request", "request_id": scope.get("state", {}).get("request_id"),
                "method": scope["method"], "status": status,
                "duration_ms": round((monotonic() - began) * 1000),
            }))
