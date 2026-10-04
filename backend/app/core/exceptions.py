from fastapi import HTTPException


class VOXISException(Exception):
    """Base exception for application-level errors."""


class FeatureNotEnabledError(
    HTTPException
):
    def __init__(
        self,
        feature: str,
        phase: str | None = None,
    ):
        detail = (
            f"{feature} is not enabled."
        )

        if phase:
            detail += (
                f" It is scheduled for {phase}."
            )

        super().__init__(
            status_code=501,
            detail=detail,
        )


class InvalidAudioError(
    HTTPException
):
    def __init__(
        self,
        message: str,
    ):
        super().__init__(
            status_code=400,
            detail=message,
        )


class PayloadTooLargeError(
    HTTPException
):
    def __init__(
        self,
        message: str,
    ):
        super().__init__(
            status_code=413,
            detail=message,
        )
