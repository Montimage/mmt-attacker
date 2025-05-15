#!/usr/bin/env python3
"""
Utility Functions Module

This module provides common utility functions used throughout the MMT Attacker framework,
including command execution, file operations, and application path resolution.

The functions in this module are designed to be reusable across different components
of the MMT Attacker framework and provide consistent error handling and logging.

Author: Montimage
License: Proprietary
"""

import os
import sys
import json
import shlex
import subprocess
from typing import Dict, List, Optional, Union, Any

# Import centralized logger
from logger import get_logger

# Get module logger
logger = get_logger(__name__)

def exec_command(cmd: str, cwd: Optional[str] = None, timeout: Optional[int] = None, 
shell: bool = True) -> Optional[str]:
    """Execute a command and return the output.
    
    This function executes a shell command and returns its output. It handles errors
    and provides detailed logging of command execution.
    
    Args:
        cmd (str): The command to be executed
        cwd (Optional[str]): The working directory in which to execute the command
        timeout (Optional[int]): Maximum time in seconds to wait for command completion
        shell (bool): Whether to use shell execution (default: True)
        
    Returns:
        Optional[str]: The command output as a string, or None if execution failed
        
    Example:
        >>> exec_command('echo "Hello World"')
        'Hello World'
    """
    try:
        # Log the command being executed
        logger.debug(f"Executing command: {cmd}")
        
        # Execute the command with appropriate parameters
        output = subprocess.check_output(
            cmd,
            shell=shell,
            stderr=subprocess.STDOUT,
            cwd=cwd,
            timeout=timeout,
            universal_newlines=False  # Return bytes for proper encoding handling
        )
        
        # Decode the output with error handling
        decoded_output = output.decode('utf-8', errors='replace').strip()
        return decoded_output
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Command '{e.cmd}' failed with error code {e.returncode}: {e.output.decode('utf-8', errors='replace')}")
        return None
    except subprocess.TimeoutExpired:
        logger.error(f"Command '{cmd}' timed out after {timeout} seconds")
        return None
    except Exception as e:
        logger.error(f"Error executing command '{cmd}': {str(e)}")
        return None


def exec_command_safe(cmd_args: List[str], cwd: Optional[str] = None, timeout: Optional[int] = None) -> Optional[str]:
    """Execute a command safely without shell injection risks.
    
    This function executes a command using a list of arguments, which is safer than
    passing a shell string as it prevents shell injection attacks.
    
    Args:
        cmd_args (List[str]): The command and its arguments as a list
        cwd (Optional[str]): The working directory in which to execute the command
        timeout (Optional[int]): Maximum time in seconds to wait for command completion
        
    Returns:
        Optional[str]: The command output as a string, or None if execution failed
        
    Example:
        >>> exec_command_safe(['echo', 'Hello World'])
        'Hello World'
    """
    try:
        # Log the command being executed
        logger.debug(f"Executing command: {' '.join(cmd_args)}")
        
        # Execute the command with appropriate parameters
        output = subprocess.check_output(
            cmd_args,
            shell=False,  # Safer execution without shell
            stderr=subprocess.STDOUT,
            cwd=cwd,
            timeout=timeout,
            universal_newlines=False  # Return bytes for proper encoding handling
        )
        
        # Decode the output with error handling
        decoded_output = output.decode('utf-8', errors='replace').strip()
        return decoded_output
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Command '{' '.join(cmd_args)}' failed with error code {e.returncode}: {e.output.decode('utf-8', errors='replace')}")
        return None
    except subprocess.TimeoutExpired:
        logger.error(f"Command '{' '.join(cmd_args)}' timed out after {timeout} seconds")
        return None
    except Exception as e:
        logger.error(f"Error executing command '{' '.join(cmd_args)}': {str(e)}")
        return None

def get_application_path(app_name: str) -> Optional[str]:
    """Get the absolute path of a given application.
    
    This function uses the 'which' command to find the full path of an executable.
    It only works on systems with the 'which' command (Unix/Linux/macOS).
    
    Args:
        app_name (str): Name of the application to locate
        
    Returns:
        Optional[str]: Absolute path to the application, or None if not found
        
    Example:
        >>> get_application_path('python')
        '/usr/bin/python'
    """
    if not app_name or not app_name.strip():
        logger.error("Empty application name provided")
        return None
        
    # Sanitize the application name to prevent command injection
    sanitized_app_name = shlex.quote(app_name.strip())
    
    # Use the safer exec_command_safe to avoid shell injection
    path = exec_command_safe(['which', sanitized_app_name])
    
    if not path:
        logger.warning(f"Application '{app_name}' not found in PATH")
        
    return path

def read_json_file(file_path: str) -> Optional[Union[Dict, List]]:
    """Read a JSON file and return its contents as a Python object.
    
    This function reads a JSON file and parses it into a Python dictionary or list.
    It handles various error conditions and provides detailed error logging.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        Optional[Union[Dict, List]]: The parsed JSON data as a Python object, or None if reading failed
        
    Example:
        >>> data = read_json_file('config.json')
        >>> if data:
        ...     print(data['version'])
    """
    if not file_path or not isinstance(file_path, str):
        logger.error("Invalid file path provided")
        return None
        
    # Normalize and validate the file path
    normalized_path = os.path.normpath(file_path)
    
    if not os.path.exists(normalized_path):
        logger.error(f"File not found: {normalized_path}")
        return None
        
    if not os.path.isfile(normalized_path):
        logger.error(f"Path is not a file: {normalized_path}")
        return None
        
    try:
        # Open the JSON file for reading
        with open(normalized_path, 'r', encoding='utf-8') as f:
            # Load the contents of the file into a Python object
            json_data = json.load(f)
            return json_data
            
    except FileNotFoundError:
        logger.error(f"File not found: {normalized_path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in {normalized_path}: {str(e)}")
        return None
    except PermissionError:
        logger.error(f"Permission denied when reading {normalized_path}")
        return None
    except Exception as e:
        logger.error(f"Error reading JSON file {normalized_path}: {str(e)}")
        return None


def write_json_file(file_path: str, data: Union[Dict, List], indent: int = 4) -> bool:
    """Write data to a JSON file.
    
    This function serializes a Python object to JSON and writes it to a file.
    It handles various error conditions and provides detailed error logging.
    
    Args:
        file_path (str): Path to the JSON file to write
        data (Union[Dict, List]): The data to serialize to JSON
        indent (int): Number of spaces for indentation in the JSON file
        
    Returns:
        bool: True if the write was successful, False otherwise
        
    Example:
        >>> config = {'version': '1.0', 'debug': True}
        >>> write_json_file('config.json', config)
        True
    """
    if not file_path or not isinstance(file_path, str):
        logger.error("Invalid file path provided")
        return False
        
    # Create directory if it doesn't exist
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create directory {directory}: {str(e)}")
            return False
    
    try:
        # Write the data to the JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
        
    except TypeError as e:
        logger.error(f"Data is not JSON serializable: {str(e)}")
        return False
    except PermissionError:
        logger.error(f"Permission denied when writing to {file_path}")
        return False
    except Exception as e:
        logger.error(f"Error writing JSON file {file_path}: {str(e)}")
        return False


def is_tool_available(name: str) -> bool:
    """Check if a command-line tool is available in the system PATH.
    
    Args:
        name (str): Name of the tool to check
        
    Returns:
        bool: True if the tool is available, False otherwise
        
    Example:
        >>> is_tool_available('python')
        True
        >>> is_tool_available('nonexistent-tool')
        False
    """
    return get_application_path(name) is not None


def get_file_size(file_path: str) -> Optional[int]:
    """Get the size of a file in bytes.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        Optional[int]: Size of the file in bytes, or None if the file doesn't exist
        
    Example:
        >>> size = get_file_size('example.txt')
        >>> if size:
        ...     print(f"File size: {size} bytes")
    """
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        logger.error(f"File not found: {file_path}")
        return None
        
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        logger.error(f"Error getting file size for {file_path}: {str(e)}")
        return None


def ensure_dir_exists(directory: str) -> bool:
    """Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory (str): Path to the directory
        
    Returns:
        bool: True if the directory exists or was created, False otherwise
        
    Example:
        >>> ensure_dir_exists('/tmp/my_directory')
        True
    """
    if not directory:
        logger.error("Empty directory path provided")
        return False
        
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {str(e)}")
        return False
