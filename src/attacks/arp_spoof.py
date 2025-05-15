"""ARP Spoofing attack implementation"""

import argparse
import sys
import os
import netifaces
from typing import Optional, Dict, Any
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class ArpSpoofing(AttackBase):
    """ARP Spoofing attack implementation"""
    
    name = "arp-spoof"
    description = "Perform ARP spoofing attack"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        # Target configuration
        target_group = parser.add_argument_group('Target Configuration')
        target_group.add_argument('--target', required=True, help='Target IP address')
        target_group.add_argument('--target-mac', help='Target MAC address (will be auto-discovered if not specified)')
        target_group.add_argument('--gateway', required=True, help='Gateway IP address')
        target_group.add_argument('--gateway-mac', help='Gateway MAC address (will be auto-discovered if not specified)')
        
        # Network configuration
        net_group = parser.add_argument_group('Network Configuration')
        net_group.add_argument('--interface', required=True, help='Network interface to use')
        net_group.add_argument('--source-ip', help='Source IP address for spoofed packets (default: interface IP)')
        net_group.add_argument('--source-mac', help='Source MAC address for spoofed packets (default: interface MAC)')
        
        # Attack behavior
        behavior_group = parser.add_argument_group('Attack Behavior')
        behavior_group.add_argument('--interval', type=float, default=1.0, help='Time interval between packets (seconds)')
        behavior_group.add_argument('--count', type=int, default=0, help='Number of packets to send (0 for infinite)')
        behavior_group.add_argument('--aggressive', action='store_true', help='Send packets more frequently when target is active')
        behavior_group.add_argument('--bidirectional', action='store_true', help='Spoof both target->gateway and gateway->target')
        behavior_group.add_argument('--restore-on-exit', action='store_true', help='Restore ARP tables when attack ends')
        
        # Monitoring and output
        monitor_group = parser.add_argument_group('Monitoring')
        monitor_group.add_argument('--packet-log', help='Log file for captured packets')
        monitor_group.add_argument('--verify', action='store_true', help='Verify ARP tables are poisoned')
        monitor_group.add_argument('--silent', action='store_true', help='Suppress non-error output')
        
    def validate(self, args: argparse.Namespace) -> bool:
        # Validate IP addresses
        if not self.validator.validate_ip(args.target, allow_private=True, allow_loopback=False):
            logger.error(f"Invalid target IP address: {args.target}")
            return False
        if not self.validator.validate_ip(args.gateway, allow_private=True, allow_loopback=False):
            logger.error(f"Invalid gateway IP address: {args.gateway}")
            return False
        if args.source_ip and not self.validator.validate_ip(args.source_ip, allow_private=True):
            logger.error(f"Invalid source IP address: {args.source_ip}")
            return False
            
        # Validate MAC addresses if provided
        if args.target_mac and not self.validator.validate_mac_address(args.target_mac):
            logger.error(f"Invalid target MAC address: {args.target_mac}")
            return False
        if args.gateway_mac and not self.validator.validate_mac_address(args.gateway_mac):
            logger.error(f"Invalid gateway MAC address: {args.gateway_mac}")
            return False
        if args.source_mac and not self.validator.validate_mac_address(args.source_mac):
            logger.error(f"Invalid source MAC address: {args.source_mac}")
            return False
            
        # Validate interface
        if not self.validator.validate_interface(args.interface):
            logger.error(f"Invalid interface: {args.interface}")
            return False
            
        # Validate interface has required IP address
        try:
            addrs = netifaces.ifaddresses(args.interface)
            if netifaces.AF_INET not in addrs:
                logger.error(f"Interface {args.interface} has no IPv4 address")
                return False
        except Exception as e:
            logger.error(f"Failed to get interface addresses: {str(e)}")
            return False
            
        # Validate packet log file if specified
        if args.packet_log and not self.validator.validate_file_path(
            args.packet_log, 
            check_exists=False, 
            check_readable=False
        ):
            logger.error(f"Invalid packet log file path: {args.packet_log}")
            return False
            
        # Validate timing parameters
        if args.interval <= 0:
            logger.error(f"Invalid interval: {args.interval}")
            return False
        if args.count < 0:
            logger.error(f"Invalid packet count: {args.count}")
            return False
            
        # Additional checks
        if args.target == args.gateway:
            logger.error("Target and gateway IP addresses cannot be the same")
            return False
            
        return True
        return True
        
    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        arp_spoof_path = os.path.join(scripts_dir, 'arp_spoofing')
        
        sys.path.insert(0, arp_spoof_path)
        try:
            import arp_spoof as attack_script
            
            # Set up logging configuration
            if args.silent:
                logger.setLevel(logging.WARNING)
            
            # Create attack configuration
            config = {
                # Target configuration
                'target_ip': args.target,
                'target_mac': args.target_mac,  # Will be auto-discovered if None
                'gateway_ip': args.gateway,
                'gateway_mac': args.gateway_mac,  # Will be auto-discovered if None
                
                # Network configuration
                'interface': args.interface,
                'source_ip': args.source_ip,  # Will use interface IP if None
                'source_mac': args.source_mac,  # Will use interface MAC if None
                
                # Attack behavior
                'interval': args.interval,
                'count': args.count,
                'aggressive': args.aggressive,
                'bidirectional': args.bidirectional,
                'restore_on_exit': args.restore_on_exit,
                
                # Monitoring
                'packet_log': args.packet_log,
                'verify': args.verify
            }
            
            # Run the attack
            logger.info(f"Running ARP spoofing attack against {args.target} via {args.interface}")
            if args.bidirectional:
                logger.info("Running in bidirectional mode - spoofing both target and gateway")
            if args.aggressive:
                logger.info("Running in aggressive mode - increased packet frequency when target is active")
            if args.restore_on_exit:
                logger.info("ARP tables will be restored on exit")
            
            attack_script.run_attack(config)
            
        except ImportError:
            logger.error("Failed to import ARP spoofing attack script")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(arp_spoof_path)
