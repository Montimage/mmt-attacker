"""Perform MAC flooding attack"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class MacFlooding(AttackBase):
    """Perform MAC flooding attack"""

    name = "mac-flooding"
    description = "Perform MAC flooding attack"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--interface', required=True, help='Network interface')
        parser.add_argument('--count', type=int, default=1000, help='Number of frames (default: 1000)')
        parser.add_argument('--rate', type=int, default=100, help='Frames per second (default: 100)')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Basic validation - extend as needed
        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'mac_flooding')
        sys.path.insert(0, path)
        try:
            import mac_flooding as attack_module
            logger.info(f"Running mac-flooding attack")

            # Create and execute attack
            attack = attack_module.MACFloodingAttack(
                args.interface,
                args.count,
                args.rate,
                args.verbose
            )
            attack.execute()
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
