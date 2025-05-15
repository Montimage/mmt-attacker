"""SQL Injection attack implementation"""

import argparse
import sys
import os
import netifaces
from typing import Optional, Dict, Any, List
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class SqlInjection(AttackBase):
    """SQL Injection attack implementation"""
    
    name = "sql-injection"
    description = "Perform SQL injection attack"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        # Target configuration
        target_group = parser.add_argument_group('Target Configuration')
        target_group.add_argument('--target', required=True, help='Target URL')
        target_group.add_argument('--parameter', required=True, help='Parameter to inject')
        target_group.add_argument('--parameters-file', help='File containing parameters to test')
        target_group.add_argument('--method', default='GET', 
                                help='HTTP method (GET, POST, PUT, etc)')
        target_group.add_argument('--path', help='Target path (if not in URL)')
        
        # Injection configuration
        inject_group = parser.add_argument_group('Injection Configuration')
        inject_group.add_argument('--payload', help='SQL injection payload')
        inject_group.add_argument('--payloads-file', help='File containing payloads')
        inject_group.add_argument('--dbms', choices=['mysql', 'mssql', 'oracle', 'postgresql'], 
                                help='Target DBMS type')
        inject_group.add_argument('--prefix', help='Payload prefix')
        inject_group.add_argument('--suffix', help='Payload suffix')
        inject_group.add_argument('--encoding', help='Payload encoding (e.g., base64)')
        
        # Request configuration
        req_group = parser.add_argument_group('Request Configuration')
        req_group.add_argument('--headers', help='Additional headers in JSON format')
        req_group.add_argument('--cookies', help='Cookies in JSON format')
        req_group.add_argument('--data', help='POST data template')
        req_group.add_argument('--user-agent', help='Custom User-Agent string')
        req_group.add_argument('--referer', help='Custom Referer header')
        req_group.add_argument('--content-type', help='Content-Type header')
        
        # Detection configuration
        detect_group = parser.add_argument_group('Detection Configuration')
        detect_group.add_argument('--string', help='String to match in response')
        detect_group.add_argument('--regex', help='Regex pattern to match in response')
        detect_group.add_argument('--code', type=int, help='Expected HTTP response code')
        detect_group.add_argument('--time-based', action='store_true', 
                                help='Use time-based detection')
        detect_group.add_argument('--time-sec', type=float, default=5.0, 
                                help='Time-based detection threshold (seconds)')
        
        # Network configuration
        net_group = parser.add_argument_group('Network Configuration')
        net_group.add_argument('--interface', help='Network interface to use')
        net_group.add_argument('--source-ip', help='Source IP address (random if not specified)')
        net_group.add_argument('--proxy', help='Proxy URL (e.g., http://127.0.0.1:8080)')
        net_group.add_argument('--timeout', type=float, default=30.0, 
                             help='Request timeout (seconds)')
        net_group.add_argument('--delay', type=float, default=0.0, 
                             help='Delay between requests (seconds)')
        net_group.add_argument('--retries', type=int, default=3, 
                             help='Number of retries for failed requests')
        
        # Attack behavior
        behavior_group = parser.add_argument_group('Attack Behavior')
        behavior_group.add_argument('--threads', type=int, default=1, 
                                  help='Number of threads to use')
        behavior_group.add_argument('--batch', action='store_true', 
                                  help='Run in non-interactive mode')
        behavior_group.add_argument('--risk', type=int, choices=[1,2,3], default=1, 
                                  help='Risk level (1-3)')
        behavior_group.add_argument('--level', type=int, choices=[1,2,3,4,5], default=1, 
                                  help='Test level (1-5)')
        behavior_group.add_argument('--test-forms', action='store_true', 
                                  help='Test form parameters')
        behavior_group.add_argument('--test-cookies', action='store_true', 
                                  help='Test cookie values')
        
        # Monitoring and output
        monitor_group = parser.add_argument_group('Monitoring')
        monitor_group.add_argument('--log-file', help='Log file for requests/responses')
        monitor_group.add_argument('--output-dir', help='Directory to save output files')
        monitor_group.add_argument('--save-responses', action='store_true', 
                                 help='Save all HTTP responses')
        monitor_group.add_argument('--report-format', 
                                 choices=['text', 'json', 'html', 'xml'], 
                                 default='text', help='Report format')
        monitor_group.add_argument('--verbose', action='count', default=0, 
                                 help='Verbosity level (-v, -vv, -vvv)')
        monitor_group.add_argument('--silent', action='store_true', 
                                 help='Suppress non-error output')
        
    def validate(self, args: argparse.Namespace) -> bool:
        # Validate target configuration
        if not self.validator.validate_url(args.target):
            logger.error(f"Invalid target URL: {args.target}")
            return False
            
        if args.parameters_file and not self.validator.validate_file_path(
            args.parameters_file, check_readable=True
        ):
            logger.error(f"Invalid parameters file: {args.parameters_file}")
            return False
            
        # Validate injection configuration
        if not any([args.payload, args.payloads_file]):
            logger.error("Either --payload or --payloads-file must be specified")
            return False
            
        if args.payloads_file and not self.validator.validate_file_path(
            args.payloads_file, check_readable=True
        ):
            logger.error(f"Invalid payloads file: {args.payloads_file}")
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
                
        # Validate detection configuration
        if args.time_based and args.time_sec <= 0:
            logger.error(f"Invalid time-based threshold: {args.time_sec}")
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
            
        if args.timeout <= 0:
            logger.error(f"Invalid timeout: {args.timeout}")
            return False
            
        if args.delay < 0:
            logger.error(f"Invalid delay: {args.delay}")
            return False
            
        if args.retries < 0:
            logger.error(f"Invalid retry count: {args.retries}")
            return False
            
        # Validate attack behavior
        if args.threads <= 0:
            logger.error(f"Invalid thread count: {args.threads}")
            return False
            
        # Validate output configuration
        if args.log_file and not self.validator.validate_file_path(
            args.log_file, check_exists=False, check_readable=False
        ):
            logger.error(f"Invalid log file path: {args.log_file}")
            return False
            
        if args.output_dir and not self.validator.validate_file_path(
            args.output_dir, check_exists=False, check_readable=False
        ):
            logger.error(f"Invalid output directory: {args.output_dir}")
            return False
            
        return True
        
    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        attack_path = os.path.join(scripts_dir, 'sql_injection')
        
        sys.path.insert(0, attack_path)
        try:
            import sql_injection as attack_script
            
            # Create attack configuration
            config = {
                'target_url': args.target,
                'parameter': args.parameter,
                'method': args.method,
                'payload_file': args.payload_file,
                'cookies': args.cookies,
                'timeout': args.timeout
            }
            
            # Run the attack
            logger.info(f"Running SQL injection attack against {args.target}")
            attack_script.run_attack(config)
            
        except ImportError:
            logger.error("Failed to import SQL injection attack script")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(attack_path)
