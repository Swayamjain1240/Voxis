import os
from dataclasses import dataclass


def read_bool(
    name: str,
    default: bool = False,
) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def read_int(
    name: str,
    default: int,
) -> int:
    value = os.getenv(name)

    if value is None:
        return default

    try:
        return int(value)
    except ValueError as error:
        raise ValueError(
            f"{name} must be an integer."
        ) from error


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv(
        "APP_NAME",
        "VOXIS",
    )

    environment: str = os.getenv(
        "ENVIRONMENT",
        "development",
    )

    host: str = os.getenv(
        "HOST",
        "127.0.0.1",
    )

    port: int = read_int(
        "PORT",
        8000,
    )

    max_audio_upload_mb: int = read_int(
        "MAX_AUDIO_UPLOAD_MB",
        25,
    )

    whisper_enabled: bool = read_bool(
        "WHISPER_ENABLED",
        False,
    )

    llm_enabled: bool = read_bool(
        "LLM_ENABLED",
        False,
    )

    sign_model_enabled: bool = read_bool(
        "SIGN_MODEL_ENABLED",
        False,
    )

    tts_enabled: bool = read_bool(
        "TTS_ENABLED",
        False,
    )

    whisper_model_size: str = os.getenv(
        "WHISPER_MODEL_SIZE",
        "small",
    )

    sign_model_path: str = os.getenv(
        "SIGN_MODEL_PATH",
        "",
    )

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
