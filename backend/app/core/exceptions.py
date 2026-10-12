from typing import Any

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request

from app.schemas.response import request_meta


class VOXISException(Exception):
    """Base exception for application-level errors."""


class VOXISHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        *,
        details: Any | None = None,
    ):
        self.code = code
        self.message = message
        self.details = details if details is not None else {}
        super().__init__(
            status_code=status_code,
            detail=message,
        )


class FeatureNotEnabledError(VOXISHTTPException):
    def __init__(
        self,
        feature: str,
        phase: str | None = None,
    ):
        message = (
            f"{feature} is not enabled."
        )

        if phase:
            message += (
                f" It is scheduled for {phase}."
            )

        super().__init__(
            status_code=501,
            code="FEATURE_DISABLED",
            message=message,
            details={"feature": feature},
        )


class FeatureUnavailableError(VOXISHTTPException):
    def __init__(
        self,
        feature: str,
        code: str,
        reason: str = "The feature is enabled but not implemented.",
    ):
        super().__init__(
            status_code=503,
            code=code,
            message=f"{feature} is unavailable. {reason}",
            details={
                "feature": feature,
                "reason": reason,
            },
        )


class InvalidAudioError(VOXISHTTPException):
    def __init__(
        self,
        message: str,
    ):
        super().__init__(
            status_code=400,
            code="INVALID_AUDIO",
            message=message,
        )


class UnsupportedMediaTypeError(VOXISHTTPException):
    def __init__(
        self,
        message: str,
    ):
        super().__init__(
            status_code=415,
            code="UNSUPPORTED_MEDIA_TYPE",
            message=message,
        )


class PayloadTooLargeError(VOXISHTTPException):
    def __init__(
        self,
        message: str,
    ):
        super().__init__(
            status_code=413,
            code="PAYLOAD_TOO_LARGE",
            message=message,
        )


def _status_code_to_error_code(status_code: int) -> str:
    return {
        400: "INVALID_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        408: "REQUEST_TIMEOUT",
        413: "PAYLOAD_TOO_LARGE",
        415: "UNSUPPORTED_MEDIA_TYPE",
        422: "VALIDATION_ERROR",
        429: "RATE_LIMITED",
        501: "NOT_IMPLEMENTED",
        503: "SERVICE_UNAVAILABLE",
    }.get(status_code, "INTERNAL_ERROR" if status_code >= 500 else "REQUEST_ERROR")


def http_exception_handler(
    _request: Request,
    exc: HTTPException,
) -> JSONResponse:
    message = getattr(exc, "message", None)
    if message is None:
        message = exc.detail if isinstance(exc.detail, str) else "The request could not be processed."
    details = getattr(exc, "details", None)
    if details is None:
        details = exc.detail if isinstance(exc.detail, dict) else {}

    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content={
            "success": False,
            "error": {
                "code": getattr(exc, "code", None) or _status_code_to_error_code(exc.status_code),
                "message": message,
                "details": details,
            },
            "meta": request_meta(_request),
            # Keep the old field for the current Mode 1 frontend/client boundary.
            "detail": exc.detail,
        },
    )


def validation_exception_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    details = [
        {
            "loc": [str(part) for part in error.get("loc", ())],
            "message": error.get("msg", "Invalid value."),
            "type": error.get("type", "value_error"),
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The request could not be validated.",
                "details": details,
            },
            "meta": request_meta(_request),
            "detail": details,
        },
    )


def unhandled_exception_handler(
    _request: Request,
    _exc: Exception,
) -> JSONResponse:
    """Return a safe response without exposing exception details or paths."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "The service could not process the request.",
                "details": {},
            },
            "meta": request_meta(_request),
            "detail": "The service could not process the request.",
        },
    )
