"""Perform FTP brute force attack"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class FtpBruteForce(AttackBase):
    """Perform FTP brute force attack"""

    name = "ftp-brute-force"
    description = "Perform FTP brute force attack"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--host', required=True, help='FTP server host')
        parser.add_argument('--port', type=int, , help='FTP port (default: 21)')
        parser.add_argument('--username', required=True, help='Username to test')
        parser.add_argument('--passwords', required=True, help='Password list file')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Basic validation - extend as needed
        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'ftp_brute_force')
        sys.path.insert(0, path)
        try:
            import ftp_brute_force as attack_module
            logger.info(f"Running ftp-brute-force attack")
            # Attack execution handled by module
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
