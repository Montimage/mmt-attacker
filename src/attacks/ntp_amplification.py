"""Perform NTP amplification attack"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class NtpAmplification(AttackBase):
    """Perform NTP amplification attack"""

    name = "ntp-amplification"
    description = "Perform NTP amplification attack"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--victim', required=True, help='Victim IP address')
        parser.add_argument('--ntp-servers', required=True, help='NTP server IPs (comma-separated)')
        parser.add_argument('--count', type=int, , help='Number of packets (default: 100)')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Basic validation - extend as needed
        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'ntp_amplification')
        sys.path.insert(0, path)
        try:
            import ntp_amplification as attack_module
            logger.info(f"Running ntp-amplification attack")
            # Attack execution handled by module
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
