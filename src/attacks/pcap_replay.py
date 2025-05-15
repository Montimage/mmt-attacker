"""PCAP Replay attack implementation"""

import argparse
import sys
import os
from typing import Optional
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class PcapReplay(AttackBase):
    """PCAP Replay attack implementation"""
    
    name = "pcap-replay"
    description = "Replay captured network traffic from PCAP files"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--file', required=True, help='PCAP file to replay')
        parser.add_argument('--interface', required=True, help='Network interface to use')
        parser.add_argument('--loop', action='store_true', help='Loop the replay continuously')
        parser.add_argument('--count', type=int, help='Number of times to replay (ignored if --loop is set)')
        parser.add_argument('--speed', type=float, default=1.0, help='Replay speed multiplier')
        parser.add_argument('--src-ip', help='Replace source IP address')
        parser.add_argument('--dst-ip', help='Replace destination IP address')
        parser.add_argument('--src-port', type=int, help='Replace source port')
        parser.add_argument('--dst-port', type=int, help='Replace destination port')
        
    def validate(self, args: argparse.Namespace) -> bool:
        if not os.path.isfile(args.file):
            logger.error(f"PCAP file not found: {args.file}")
            return False
        if not self.validator.validate_interface(args.interface):
            logger.error(f"Invalid interface: {args.interface}")
            return False
        if args.src_ip and not self.validator.validate_ip(args.src_ip):
            logger.error(f"Invalid source IP address: {args.src_ip}")
            return False
        if args.dst_ip and not self.validator.validate_ip(args.dst_ip):
            logger.error(f"Invalid destination IP address: {args.dst_ip}")
            return False
        if args.src_port and not self.validator.validate_port(args.src_port):
            logger.error(f"Invalid source port: {args.src_port}")
            return False
        if args.dst_port and not self.validator.validate_port(args.dst_port):
            logger.error(f"Invalid destination port: {args.dst_port}")
            return False
        if args.speed <= 0:
            logger.error(f"Invalid speed multiplier: {args.speed}")
            return False
        if args.count is not None and args.count <= 0:
            logger.error(f"Invalid replay count: {args.count}")
            return False
        return True
        
    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        attack_path = os.path.join(scripts_dir, 'pcap_replay')
        
        sys.path.insert(0, attack_path)
        try:
            import pcap_replay as attack_script
            
            # Create attack configuration
            config = {
                'pcap_file': args.file,
                'interface': args.interface,
                'loop': args.loop,
                'count': args.count,
                'speed': args.speed,
                'src_ip': args.src_ip,
                'dst_ip': args.dst_ip,
                'src_port': args.src_port,
                'dst_port': args.dst_port
            }
            
            # Run the attack
            logger.info(f"Running PCAP replay attack using {args.file}")
            attack_script.run_attack(config)
            
        except ImportError:
            logger.error("Failed to import PCAP replay script")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(attack_path)
