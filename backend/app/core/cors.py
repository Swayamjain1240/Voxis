"""Exact-origin CORS policy; credentials remain off in no-login Mode 1."""


ALLOWED_METHODS = {"GET", "POST", "OPTIONS"}
ALLOWED_HEADERS = {"content-type", "x-request-id"}


def cors_headers(origin, settings):
    if origin not in settings.cors_origins:
        return {}
    return {
        "access-control-allow-origin": origin,
        "vary": "Origin",
        "access-control-allow-methods": ", ".join(sorted(ALLOWED_METHODS)),
        "access-control-allow-headers": ", ".join(sorted(ALLOWED_HEADERS)),
        "access-control-expose-headers": "X-Request-ID, Retry-After",
    }
