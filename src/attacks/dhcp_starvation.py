"""DHCP Starvation attack implementation"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class DhcpStarvation(AttackBase):
    """DHCP Starvation attack implementation"""

    name = "dhcp-starvation"
    description = "Perform DHCP starvation attack"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--interface', required=True, help='Network interface')
        parser.add_argument('--count', type=int, default=100, help='Number of requests')
        parser.add_argument('--rate', type=int, default=10, help='Requests per second')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        if not self.validator.validate_interface(args.interface):
            logger.error(f"Invalid interface: {args.interface}")
            return False
        if args.count <= 0 or args.rate <= 0:
            logger.error("Count and rate must be positive")
            return False
        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'dhcp_starvation')
        sys.path.insert(0, path)
        try:
            import dhcp_starvation as attack_module
            attack = attack_module.DHCPStarvationAttack(
                interface=args.interface,
                count=args.count,
                rate=args.rate,
                verbose=args.verbose
            )
            logger.info(f"Running DHCP starvation attack")
            attack.execute()
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
