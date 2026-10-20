import os
import re
from dataclasses import dataclass, field
from ipaddress import ip_address
from urllib.parse import urlsplit


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


def read_list(name: str, default: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in os.getenv(name, default).split(",") if item.strip())


def valid_hostname(value: str) -> bool:
    try:
        ip_address(value)
        return True
    except ValueError:
        return bool(re.fullmatch(
            r"(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)*"
            r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", value
        ))


@dataclass(frozen=True)
class Settings:
    cors_origins: tuple[str, ...] = field(default_factory=lambda: read_list(
        "CORS_ORIGINS", "http://127.0.0.1:5173,http://localhost:5173"
    ))
    allowed_hosts: tuple[str, ...] = field(default_factory=lambda: read_list(
        "ALLOWED_HOSTS", "127.0.0.1,localhost,::1"
    ))
    rate_limit_per_minute: int = field(default_factory=lambda: read_int(
        "RATE_LIMIT_PER_MINUTE", 120, minimum=1, maximum=1000
    ))
    request_timeout_seconds: int = field(default_factory=lambda: read_int(
        "REQUEST_TIMEOUT_SECONDS", 15, minimum=1, maximum=120
    ))
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
            maximum=50,
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

    whisper_model_path: str = field(
        default_factory=lambda: read_environment(
            "WHISPER_MODEL_PATH",
            "",
        )
    )

    whisper_device: str = field(
        default_factory=lambda: read_environment(
            "WHISPER_DEVICE",
            "cpu",
        )
    )

    whisper_compute_type: str = field(
        default_factory=lambda: read_environment(
            "WHISPER_COMPUTE_TYPE",
            "int8",
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
        if self.environment not in {"development", "test", "production", "prod"}:
            raise ValueError("ENVIRONMENT must be development, test, or production.")
        if not 1 <= self.port <= 65535:
            raise ValueError("PORT must be between 1 and 65535.")
        if not 1 <= self.max_audio_upload_mb <= 50:
            raise ValueError(
                "MAX_AUDIO_UPLOAD_MB must be between 1 and 50."
            )
        if not 1 <= self.rate_limit_per_minute <= 1000:
            raise ValueError("RATE_LIMIT_PER_MINUTE must be between 1 and 1000.")
        if not 1 <= self.request_timeout_seconds <= 120:
            raise ValueError("REQUEST_TIMEOUT_SECONDS must be between 1 and 120.")
        if not valid_hostname(self.host):
            raise ValueError("HOST must be an IP address or lowercase hostname.")
        if not self.allowed_hosts or not all(valid_hostname(host) for host in self.allowed_hosts):
            raise ValueError("ALLOWED_HOSTS must contain explicit hostnames, not wildcards or URLs.")
        if not self.cors_origins:
            raise ValueError("CORS_ORIGINS must contain explicit origins.")
        for origin in self.cors_origins:
            try:
                parsed = urlsplit(origin)
                port = parsed.port
            except ValueError as error:
                raise ValueError("CORS_ORIGINS contains an invalid origin.") from error
            if (parsed.scheme not in {"http", "https"} or not parsed.hostname or
                not valid_hostname(parsed.hostname) or port == 0 or
                any(char.isspace() for char in origin) or
                any(char in origin for char in "\\?#") or origin.endswith(":") or
                parsed.username is not None or parsed.password is not None or
                parsed.path or parsed.query or parsed.fragment or "*" in origin):
                raise ValueError("CORS_ORIGINS must contain exact HTTP(S) origins without paths.")
            if self.environment in PRODUCTION_ENVIRONMENTS and parsed.scheme != "https":
                raise ValueError("Production CORS_ORIGINS must use HTTPS.")
        if self.environment in PRODUCTION_ENVIRONMENTS and self.debug:
            object.__setattr__(self, "debug", False)


settings = Settings()
