"""Man-in-the-Middle (MITM) attack implementation"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class Mitm(AttackBase):
    """Man-in-the-Middle attack implementation"""

    name = "mitm"
    description = "Perform Man-in-the-Middle attack using ARP spoofing"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        target_group = parser.add_argument_group('Target Configuration')
        target_group.add_argument('--target', required=True, help='Target IP address')
        target_group.add_argument('--gateway', required=True, help='Gateway IP address')
        target_group.add_argument('--interface', required=True, help='Network interface')

        behavior_group = parser.add_argument_group('Attack Behavior')
        behavior_group.add_argument('--interval', type=float, default=1.0,
                                   help='ARP poison interval in seconds')
        behavior_group.add_argument('--capture', help='Save captured packets to file')

        monitor_group = parser.add_argument_group('Monitoring')
        monitor_group.add_argument('--verbose', action='store_true', help='Enable verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        if not self.validator.validate_ip(args.target, allow_private=True):
            logger.error(f"Invalid target IP: {args.target}")
            return False

        if not self.validator.validate_ip(args.gateway, allow_private=True):
            logger.error(f"Invalid gateway IP: {args.gateway}")
            return False

        if not self.validator.validate_interface(args.interface):
            logger.error(f"Invalid interface: {args.interface}")
            return False

        if args.interval <= 0:
            logger.error(f"Invalid interval: {args.interval}")
            return False

        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        mitm_path = os.path.join(scripts_dir, 'mitm')

        sys.path.insert(0, mitm_path)
        try:
            import mitm as attack_module

            attack = attack_module.MITMAttack(
                target_ip=args.target,
                gateway_ip=args.gateway,
                interface=args.interface,
                interval=args.interval,
                capture_file=args.capture,
                verbose=args.verbose
            )

            logger.info(f"Running MITM attack: {args.target} <-> {args.gateway}")
            attack.execute()

        except ImportError as e:
            logger.error(f"Failed to import MITM attack script: {e}")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(mitm_path)
