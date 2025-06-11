import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FILE = os.path.join("logs", "lex.log")


def get_logger(name: str = "Lex") -> logging.Logger:
    """Return configured logger instance."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s:%(name)s:%(message)s")

    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def set_log_level(level: int) -> None:
    """Update the log level for the default logger and all handlers."""
    logger = logging.getLogger("Lex")
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)

