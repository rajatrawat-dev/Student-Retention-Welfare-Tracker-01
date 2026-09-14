"""Logging configuration for StudentIQ."""

import logging
import sys
from pathlib import Path
from src.config.settings import settings

def get_logger(name: str = "StudentIQ") -> logging.Logger:
    """Configures and returns a standardized logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
        
        # Console handler with clean formatter
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logger.level)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Optional file logger
        try:
            settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(settings.LOGS_DIR / "student_iq.log", encoding="utf-8")
            file_handler.setLevel(logger.level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception:
            pass # Graceful degradation if filesystem is constrained
            
    return logger
