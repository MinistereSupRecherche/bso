"""Logging module."""
import os
import logging
import sys
# import os


LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}




def create_logger(name=None):
    """Create a logger."""
    if not name:
        raise Exception("Logger should have a name")
    logger = logging.getLogger(name)
    logger = configure_logger(logger)
    return logger


def configure_logger(logger):
    """Configure a logger."""
    loglevel = LOG_LEVELS.get(os.getenv("LOG_LEVEL").lower()) or logging.INFO
    logger.setLevel(loglevel)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(loglevel)
    formatter = logging.Formatter(
        os.getenv("LOGGER_FORMAT"), os.getenv("LOGGER_DATE_FORMAT"))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(loglevel)
    return logger
