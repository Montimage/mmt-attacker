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
        parser.add_argument('--count', type=int, default=10, help='Number of packets (default: 10)')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Validate network interface
        if not self.validator.validate_interface(args.interface):
            logger.error(f"Invalid or unavailable network interface: {args.interface}")
            return False

        # Validate VLAN IDs (valid range is 1-4094)
        if not (1 <= args.outer_vlan <= 4094):
            logger.error(f"Invalid outer VLAN ID: {args.outer_vlan}. Must be between 1 and 4094")
            return False
        if not (1 <= args.inner_vlan <= 4094):
            logger.error(f"Invalid inner VLAN ID: {args.inner_vlan}. Must be between 1 and 4094")
            return False

        # Validate target IP
        if not self.validator.validate_ip(args.target, allow_private=True, allow_loopback=False):
            logger.error(f"Invalid target IP address: {args.target}")
            return False

        # Validate count
        if args.count <= 0:
            logger.error(f"Invalid packet count: {args.count}. Must be greater than 0")
            return False

        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'vlan_hopping')
        sys.path.insert(0, path)
        try:
            import vlan_hopping as attack_module
            logger.info(f"Running vlan-hopping attack")

            # Create and execute attack
            attack = attack_module.VLANHoppingAttack(
                args.interface,
                args.outer_vlan,
                args.inner_vlan,
                args.target,
                args.count,
                args.verbose
            )
            attack.execute()
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
