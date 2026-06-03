"""Logging configuration."""
import logging
import logging.config
from pathlib import Path
from config.settings import settings


def setup_logging() -> None:
    """Setup logging configuration."""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.REX_LOG_LEVEL,
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": settings.REX_LOG_LEVEL,
                "formatter": "detailed",
                "filename": "logs/rex.log",
                "maxBytes": 10485760,
                "backupCount": 5
            }
        },
        "root": {
            "level": settings.REX_LOG_LEVEL,
            "handlers": ["console", "file"]
        }
    }
    
    logging.config.dictConfig(logging_config)
