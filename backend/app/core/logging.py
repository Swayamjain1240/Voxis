import logging


LOGGER_NAME = "voxis"


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    return logging.getLogger(
        LOGGER_NAME
    )


logger = logging.getLogger(
    LOGGER_NAME
)
