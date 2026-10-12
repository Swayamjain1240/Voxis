import os
from dataclasses import dataclass, field


PRODUCTION_ENVIRONMENTS = {"production", "prod"}


def read_bool(
    name: str,
    default: bool = False,
) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return True
    if normalized in {
        "0",
        "false",
        "no",
        "off",
    }:
        return False
    raise ValueError(
        f"{name} must be a boolean (true/false)."
    )


def read_int(
    name: str,
    default: int,
    *,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    value = os.getenv(name)

    if value is None:
        result = default
    else:
        try:
            result = int(value.strip())
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"{name} must be an integer."
            ) from error

    if minimum is not None and result < minimum:
        raise ValueError(
            f"{name} must be at least {minimum}."
        )
    if maximum is not None and result > maximum:
        raise ValueError(
            f"{name} must be at most {maximum}."
        )

    return result


def read_environment(
    name: str,
    default: str,
) -> str:
    return os.getenv(name, default).strip()


def read_debug() -> bool:
    environment = read_environment(
        "ENVIRONMENT",
        "development",
    ).lower()
    requested = read_bool("DEBUG", False)
    return requested and environment not in PRODUCTION_ENVIRONMENTS


@dataclass(frozen=True)
class Settings:
    app_name: str = field(
        default_factory=lambda: read_environment(
            "APP_NAME",
            "VOXIS",
        )
    )

    environment: str = field(
        default_factory=lambda: read_environment(
            "ENVIRONMENT",
            "development",
        ).lower()
    )

    host: str = field(
        default_factory=lambda: read_environment(
            "HOST",
            "127.0.0.1",
        )
    )

    port: int = field(
        default_factory=lambda: read_int(
            "PORT",
            8000,
            minimum=1,
            maximum=65535,
        )
    )

    max_audio_upload_mb: int = field(
        default_factory=lambda: read_int(
            "MAX_AUDIO_UPLOAD_MB",
            25,
            minimum=1,
            maximum=1024,
        )
    )

    debug: bool = field(
        default_factory=read_debug,
    )

    whisper_enabled: bool = field(
        default_factory=lambda: read_bool(
            "WHISPER_ENABLED",
            False,
        )
    )

    llm_enabled: bool = field(
        default_factory=lambda: read_bool(
            "LLM_ENABLED",
            False,
        )
    )

    sign_model_enabled: bool = field(
        default_factory=lambda: read_bool(
            "SIGN_MODEL_ENABLED",
            False,
        )
    )

    tts_enabled: bool = field(
        default_factory=lambda: read_bool(
            "TTS_ENABLED",
            False,
        )
    )

    whisper_model_size: str = field(
        default_factory=lambda: read_environment(
            "WHISPER_MODEL_SIZE",
            "small",
        )
    )

    sign_model_path: str = field(
        default_factory=lambda: read_environment(
            "SIGN_MODEL_PATH",
            "",
        )
    )

    def __post_init__(self):
        normalized_environment = self.environment.strip().lower()
        if normalized_environment != self.environment:
            object.__setattr__(
                self,
                "environment",
                normalized_environment,
            )
        if not self.app_name:
            raise ValueError("APP_NAME must not be empty.")
        if not self.environment:
            raise ValueError("ENVIRONMENT must not be empty.")
        if not 1 <= self.port <= 65535:
            raise ValueError("PORT must be between 1 and 65535.")
        if not 1 <= self.max_audio_upload_mb <= 1024:
            raise ValueError(
                "MAX_AUDIO_UPLOAD_MB must be between 1 and 1024."
            )
        if self.environment in PRODUCTION_ENVIRONMENTS and self.debug:
            object.__setattr__(self, "debug", False)

    @property
    def cors_origins(self) -> list[str]:
        raw = os.getenv(
            "CORS_ORIGINS",
            "http://127.0.0.1:5173,http://localhost:5173",
        )

        return [
            item.strip()
            for item in raw.split(",")
            if item.strip()
        ]


settings = Settings()
