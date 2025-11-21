"""Perform Smurf amplification attack"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class SmurfAttack(AttackBase):
    """Perform Smurf amplification attack"""

    name = "smurf-attack"
    description = "Perform Smurf amplification attack"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--victim', required=True, help='Victim IP address')
        parser.add_argument('--broadcast', required=True, help='Broadcast IP address')
        parser.add_argument('--count', type=int, default=100, help='Number of packets (default: 100)')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Validate victim IP
        if not self.validator.validate_ip(args.victim, allow_private=True, allow_loopback=False):
            logger.error(f"Invalid victim IP address: {args.victim}")
            return False

        # Validate broadcast IP
        if not self.validator.validate_ip(args.broadcast, allow_private=True, allow_loopback=False):
            logger.error(f"Invalid broadcast IP address: {args.broadcast}")
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
        path = os.path.join(scripts_dir, 'smurf_attack')
        sys.path.insert(0, path)
        try:
            import smurf_attack as attack_module
            logger.info(f"Running smurf-attack attack")

            # Create and execute attack
            attack = attack_module.SmurfAttack(
                args.victim,
                args.broadcast,
                args.count,
                args.verbose
            )
            attack.execute()
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
