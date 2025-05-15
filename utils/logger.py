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

import os
import sys
import logging
import logging.handlers
from typing import Optional, Dict, Any

# Constants
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Directory for log files
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Log file paths
LOG_FILE = os.path.join(LOG_DIR, 'mmt-attacker.log')
ERROR_LOG_FILE = os.path.join(LOG_DIR, 'mmt-attacker-error.log')

# Global configuration
_log_level = DEFAULT_LOG_LEVEL
_log_format = DEFAULT_LOG_FORMAT
_date_format = DEFAULT_DATE_FORMAT
_log_to_file = True
_log_to_console = True

# Cache for loggers to avoid creating multiple loggers for the same name
_loggers: Dict[str, logging.Logger] = {}


def configure_logging(
    level: Optional[int] = None,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
    log_to_file: Optional[bool] = None,
    log_to_console: Optional[bool] = None,
    log_file: Optional[str] = None,
    error_log_file: Optional[str] = None
) -> None:
    """
    Configure the global logging settings.
    
    Args:
        level: Logging level (e.g., logging.DEBUG, logging.INFO)
        log_format: Format string for log messages
        date_format: Format string for timestamps
        log_to_file: Whether to log to files
        log_to_console: Whether to log to console
        log_file: Path to the main log file
        error_log_file: Path to the error log file
    """
    global _log_level, _log_format, _date_format, _log_to_file, _log_to_console
    
    # Update global settings if provided
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
        
    # Update log file paths if provided
    global LOG_FILE, ERROR_LOG_FILE
    if log_file is not None:
        LOG_FILE = log_file
    if error_log_file is not None:
        ERROR_LOG_FILE = error_log_file
        
    # Reconfigure existing loggers
    for logger_name, logger in _loggers.items():
        _configure_logger(logger, logger_name)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    This function returns a logger configured according to the global settings.
    If a logger with the given name already exists, it returns the existing logger.
    
    Args:
        name: Name of the logger, typically __name__ of the module
        
    Returns:
        A configured logger instance
    """
    # Check if logger already exists
    if name in _loggers:
        return _loggers[name]
    
    # Create a new logger
    logger = logging.getLogger(name)
    
    # Configure the logger
    _configure_logger(logger, name)
    
    # Cache the logger
    _loggers[name] = logger
    
    return logger


def _configure_logger(logger: logging.Logger, name: str) -> None:
    """
    Configure a logger with handlers and formatters.
    
    Args:
        logger: The logger to configure
        name: Name of the logger
    """
    # Reset existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Set the log level
    logger.setLevel(_log_level)
    
    # Create formatter
    formatter = logging.Formatter(_log_format, _date_format)
    
    # Add console handler if enabled
    if _log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Add file handlers if enabled
    if _log_to_file:
        # Ensure log directory exists
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        
        # Main log file - rotates when file reaches 5MB, keeps 5 backups
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=5*1024*1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Error log file - only logs ERROR and above
        error_file_handler = logging.handlers.RotatingFileHandler(
            ERROR_LOG_FILE, maxBytes=5*1024*1024, backupCount=5
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)
        logger.addHandler(error_file_handler)


def set_log_level(level: int) -> None:
    """
    Set the global logging level.
    
    Args:
        level: Logging level (e.g., logging.DEBUG, logging.INFO)
    """
    configure_logging(level=level)


def get_log_level() -> int:
    """
    Get the current global logging level.
    
    Returns:
        The current logging level
    """
    return _log_level


# Initialize logging with default settings
configure_logging()
