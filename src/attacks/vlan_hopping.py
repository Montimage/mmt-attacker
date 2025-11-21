"""Perform VLAN hopping attack"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class VlanHopping(AttackBase):
    """Perform VLAN hopping attack"""

    name = "vlan-hopping"
    description = "Perform VLAN hopping attack"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--interface', required=True, help='Network interface')
        parser.add_argument('--outer-vlan', type=int, required=True, help='Outer VLAN ID')
        parser.add_argument('--inner-vlan', type=int, required=True, help='Inner VLAN ID')
        parser.add_argument('--target', required=True, help='Target IP')
        parser.add_argument('--count', type=int, , help='Number of packets (default: 10)')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Basic validation - extend as needed
        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'vlan_hopping')
        sys.path.insert(0, path)
        try:
            import vlan_hopping as attack_module
            logger.info(f"Running vlan-hopping attack")
            # Attack execution handled by module
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
