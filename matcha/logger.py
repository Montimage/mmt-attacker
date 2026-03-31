#!/usr/bin/env python3
"""
Centralized Logging Module for MMT Attacker

This module provides a centralized logging configuration for all components
of the MMT Attacker framework. It ensures consistent log formatting,
levels, and handling across the entire application.

Usage:
    from logger import get_logger

    # Get a logger for a specific module
    logger = get_logger(__name__)

    # Use the logger
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

Author: Montimage
License: Proprietary
"""

import logging
import logging.handlers
import os
import sys

# ---------------------------------------------------------------------------
# ANSI colour codes (terminal only)
# ---------------------------------------------------------------------------

_RESET = "\033[0m"
_BOLD = "\033[1m"
_DIM = "\033[2m"

# Palette: charcoal/slate + electric cyan + amber + red
_CYAN = "\033[38;5;51m"
_AMBER = "\033[38;5;214m"
_RED = "\033[38;5;196m"
_GREEN = "\033[38;5;82m"
_GREY = "\033[38;5;245m"
_WHITE = "\033[38;5;252m"

_LEVEL_COLORS = {
    "DEBUG": _GREY,
    "INFO": _CYAN,
    "WARNING": _AMBER,
    "ERROR": _RED,
    "CRITICAL": f"{_BOLD}{_RED}",
}

_LEVEL_LABELS = {
    "DEBUG": "DBG",
    "INFO": "INF",
    "WARNING": "WRN",
    "ERROR": "ERR",
    "CRITICAL": "CRT",
}


# ---------------------------------------------------------------------------
# Custom formatters
# ---------------------------------------------------------------------------


class _ColourFormatter(logging.Formatter):
    """ANSI-coloured formatter for terminal output."""

    def format(self, record: logging.LogRecord) -> str:  # noqa: A003
        level = record.levelname
        colour = _LEVEL_COLORS.get(level, _WHITE)
        label = _LEVEL_LABELS.get(level, level[:3])

        # Short module name (last two segments)
        module = record.name
        parts = module.rsplit(".", 2)
        short_module = ".".join(parts[-2:]) if len(parts) >= 2 else module
        short_module = short_module[:28].ljust(28)

        ts = self.formatTime(record, "%H:%M:%S")

        prefix = (
            f"{_DIM}{_WHITE}{ts}{_RESET} "
            f"{colour}{_BOLD}[{label}]{_RESET} "
            f"{_DIM}{short_module}{_RESET}  "
        )
        msg = record.getMessage()

        if record.exc_info:
            msg += "\n" + self.formatException(record.exc_info)

        return prefix + msg


class _PlainFormatter(logging.Formatter):
    """Plain formatter for file output (no ANSI codes)."""

    FMT = "%(asctime)s  %(levelname)-8s  %(name)-40s  %(message)s"
    DATE = "%Y-%m-%d %H:%M:%S"

    def __init__(self) -> None:
        super().__init__(fmt=self.FMT, datefmt=self.DATE)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "mmt-attacker.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "mmt-attacker-error.log")

# ---------------------------------------------------------------------------
# Global state
# ---------------------------------------------------------------------------

_log_level = DEFAULT_LOG_LEVEL
_log_format = DEFAULT_LOG_FORMAT
_date_format = DEFAULT_DATE_FORMAT
_log_to_file = True
_log_to_console = True

_loggers: dict[str, logging.Logger] = {}

# Detect whether stdout/stderr support colour
_USE_COLOR = sys.stderr.isatty() and os.environ.get("NO_COLOR", "") == ""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def configure_logging(
    level: int | None = None,
    log_format: str | None = None,
    date_format: str | None = None,
    log_to_file: bool | None = None,
    log_to_console: bool | None = None,
    log_file: str | None = None,
    error_log_file: str | None = None,
) -> None:
    """Configure the global logging settings."""
    global _log_level, _log_format, _date_format, _log_to_file, _log_to_console
    global LOG_FILE, ERROR_LOG_FILE

    if level is not None:
        _log_level = level
    if log_format is not None:
        _log_format = log_format
    if date_format is not None:
        _date_format = date_format
    if log_to_file is not None:
        _log_to_file = log_to_file
    if log_to_console is not None:
        _log_to_console = log_to_console
    if log_file is not None:
        LOG_FILE = log_file
    if error_log_file is not None:
        ERROR_LOG_FILE = error_log_file

    for logger_name, logger in _loggers.items():
        _configure_logger(logger, logger_name)


def get_logger(name: str) -> logging.Logger:
    """Return a logger configured according to global settings."""
    if name in _loggers:
        return _loggers[name]
    logger = logging.getLogger(name)
    _configure_logger(logger, name)
    _loggers[name] = logger
    return logger


def set_log_level(level: int) -> None:
    configure_logging(level=level)


def get_log_level() -> int:
    return _log_level


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _configure_logger(logger: logging.Logger, name: str) -> None:
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.setLevel(_log_level)
    logger.propagate = False

    if _log_to_console:
        console = logging.StreamHandler(sys.stderr)
        console.setFormatter(_ColourFormatter() if _USE_COLOR else _PlainFormatter())
        logger.addHandler(console)

    if _log_to_file:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

        main_fh = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5
        )
        main_fh.setFormatter(_PlainFormatter())
        logger.addHandler(main_fh)

        err_fh = logging.handlers.RotatingFileHandler(
            ERROR_LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5
        )
        err_fh.setLevel(logging.ERROR)
        err_fh.setFormatter(_PlainFormatter())
        logger.addHandler(err_fh)


# Boot with defaults
configure_logging()
