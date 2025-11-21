"""Perform BGP hijacking simulation"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class BgpHijacking(AttackBase):
    """Perform BGP hijacking simulation"""

    name = "bgp-hijacking"
    description = "Perform BGP hijacking simulation"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--prefix', required=True, help='Target IP prefix')
        parser.add_argument('--as-number', type=int, required=True, help='AS number')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Validate prefix (CIDR notation)
        if not self.validator.validate_network(args.prefix):
            logger.error(f"Invalid IP prefix/network: {args.prefix}. Must be in CIDR notation (e.g., 192.168.1.0/24)")
            return False

        # Validate AS number (valid range is 1-4294967295 for 32-bit ASN)
        if not (1 <= args.as_number <= 4294967295):
            logger.error(f"Invalid AS number: {args.as_number}. Must be between 1 and 4294967295")
            return False

        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'bgp_hijacking')
        sys.path.insert(0, path)
        try:
            import bgp_hijacking as attack_module
            logger.info(f"Running bgp-hijacking attack")

            # Create and execute attack
            attack = attack_module.BGPHijackingAttack(
                args.prefix,
                args.as_number,
                args.verbose
            )
            attack.execute()
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
