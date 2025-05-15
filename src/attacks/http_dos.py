"""HTTP DoS attack implementation"""

import argparse
import sys
import os
import netifaces
from typing import Optional, Dict, Any, List
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class HttpDos(AttackBase):
    """HTTP DoS attack implementation"""
    
    name = "http-dos"
    description = "Perform HTTP DoS attack"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        # Target configuration
        target_group = parser.add_argument_group('Target Configuration')
        target_group.add_argument('--target', required=True, help='Target URL')
        target_group.add_argument('--method', default='GET', 
                                help='HTTP method (GET, POST, HEAD, PUT, DELETE, OPTIONS)')
        target_group.add_argument('--path', default='/', help='Target path (default: /)')
        target_group.add_argument('--port', type=int, help='Target port (default: 80/443 based on scheme)')
        
        # Request configuration
        req_group = parser.add_argument_group('Request Configuration')
        req_group.add_argument('--user-agent', help='Custom User-Agent string')
        req_group.add_argument('--headers', help='Additional headers in JSON format')
        req_group.add_argument('--cookies', help='Cookies in JSON format')
        req_group.add_argument('--data', help='POST/PUT data')
        req_group.add_argument('--data-file', help='File containing POST/PUT data')
        req_group.add_argument('--content-type', help='Content-Type header for requests')
        req_group.add_argument('--follow-redirects', action='store_true', help='Follow redirects')
        
        # Network configuration
        net_group = parser.add_argument_group('Network Configuration')
        net_group.add_argument('--interface', help='Network interface to use')
        net_group.add_argument('--source-ip', help='Source IP address (random if not specified)')
        net_group.add_argument('--proxy', help='Proxy URL (e.g., socks5://127.0.0.1:9050)')
        net_group.add_argument('--dns-resolver', help='Custom DNS resolver')
        net_group.add_argument('--timeout', type=float, default=30.0, help='Request timeout in seconds')
        net_group.add_argument('--ssl-verify', action='store_true', help='Verify SSL certificates')
        
        # Attack behavior
        behavior_group = parser.add_argument_group('Attack Behavior')
        behavior_group.add_argument('--threads', type=int, default=10, help='Number of threads to use')
        behavior_group.add_argument('--count', type=int, default=1000, help='Number of requests to send')
        behavior_group.add_argument('--interval', type=float, default=0.1, 
                                  help='Time interval between requests (seconds)')
        behavior_group.add_argument('--ramp-up', type=int, help='Gradually increase request rate over seconds')
        behavior_group.add_argument('--random-path', action='store_true', 
                                  help='Randomize path for each request')
        behavior_group.add_argument('--random-query', action='store_true', 
                                  help='Add random query parameters')
        
        # Monitoring and output
        monitor_group = parser.add_argument_group('Monitoring')
        monitor_group.add_argument('--log-file', help='Log file for requests and responses')
        monitor_group.add_argument('--stats-interval', type=float, default=1.0, 
                                 help='Interval for printing statistics')
        monitor_group.add_argument('--success-codes', help='HTTP codes to consider success (default: 200-299)')
        monitor_group.add_argument('--verify-success', action='store_true', 
                                 help='Verify successful requests before attack')
        monitor_group.add_argument('--silent', action='store_true', help='Suppress non-error output')
        
    def validate(self, args: argparse.Namespace) -> bool:
        # Validate target URL and configuration
        if not self.validator.validate_url(args.target):
            logger.error(f"Invalid target URL: {args.target}")
            return False
            
        if args.port is not None and not self.validator.validate_port(args.port):
            logger.error(f"Invalid port: {args.port}")
            return False
            
        # Validate HTTP method
        valid_methods = {'GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS'}
        if args.method.upper() not in valid_methods:
            logger.error(f"Invalid HTTP method: {args.method}. Must be one of {valid_methods}")
            return False
            
        # Validate request configuration
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
                
        if args.data_file and not self.validator.validate_file_path(args.data_file, check_readable=True):
            logger.error(f"Invalid data file: {args.data_file}")
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
            
        # Validate numeric parameters
        if args.timeout <= 0:
            logger.error(f"Invalid timeout: {args.timeout}")
            return False
            
        if args.threads <= 0:
            logger.error(f"Invalid thread count: {args.threads}")
            return False
            
        if args.count <= 0:
            logger.error(f"Invalid request count: {args.count}")
            return False
            
        if args.interval <= 0:
            logger.error(f"Invalid interval: {args.interval}")
            return False
            
        if args.ramp_up is not None and args.ramp_up <= 0:
            logger.error(f"Invalid ramp-up time: {args.ramp_up}")
            return False
            
        if args.stats_interval <= 0:
            logger.error(f"Invalid statistics interval: {args.stats_interval}")
            return False
            
        # Validate success codes if provided
        if args.success_codes:
            try:
                codes = [int(x.strip()) for x in args.success_codes.split('-')]
                if len(codes) not in (1, 2) or not all(100 <= x <= 599 for x in codes):
                    raise ValueError
            except ValueError:
                logger.error(f"Invalid success codes: {args.success_codes}. Use format: 200 or 200-299")
                return False
                
        return True
        
    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        attack_path = os.path.join(scripts_dir, 'http_dos')
        
        sys.path.insert(0, attack_path)
        try:
            import http_dos as attack_script
            
            # Create attack configuration
            config = {
                'target_url': args.target,
                'method': args.method,
                'thread_count': args.threads,
                'request_count': args.requests,
                'interval': args.interval,
                'timeout': args.timeout
            }
            
            # Run the attack
            logger.info(f"Running HTTP DoS attack against {args.target}")
            attack_script.run_attack(config)
            
        except ImportError:
            logger.error("Failed to import HTTP DoS attack script")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(attack_path)
