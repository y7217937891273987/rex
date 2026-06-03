"""
Utilities module - Logging setup.
"""

import logging
import logging.handlers
import os
from config.settings import LOG_FILE, LOG_FORMAT


def setup_logging(name: str, level: str = "INFO") -> logging.Logger:
    """
    Setup logging for a module.
    
    Args:
        name: Module name
        level: Log level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # File handler with rotation
    log_path = f"logs/{LOG_FILE}"
    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=10485760,
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # Add handlers if not already present
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
