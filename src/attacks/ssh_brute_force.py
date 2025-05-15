"""SSH Brute Force attack implementation"""

import argparse
import sys
import os
import netifaces
from typing import Optional, Dict, Any, List
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class SshBruteForce(AttackBase):
    """SSH Brute Force attack implementation"""
    
    name = "ssh-brute-force"
    description = "Perform SSH brute force attack"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        # Target configuration
        target_group = parser.add_argument_group('Target Configuration')
        target_group.add_argument('--target', required=True, help='Target IP address or hostname')
        target_group.add_argument('--port', type=int, default=22, help='SSH port')
        target_group.add_argument('--targets-file', help='File containing list of targets (one per line)')
        
        # Authentication configuration
        auth_group = parser.add_argument_group('Authentication Configuration')
        auth_group.add_argument('--username', help='Username to try')
        auth_group.add_argument('--usernames-file', help='File containing usernames (one per line)')
        auth_group.add_argument('--password', help='Single password to try')
        auth_group.add_argument('--passwords-file', help='File containing passwords (one per line)')
        auth_group.add_argument('--key-file', help='SSH private key file')
        auth_group.add_argument('--key-passphrase', help='Passphrase for SSH private key')
        
        # Dictionary configuration
        dict_group = parser.add_argument_group('Dictionary Configuration')
        dict_group.add_argument('--wordlist', help='Password wordlist file')
        dict_group.add_argument('--custom-wordlist', help='Additional custom wordlist to append')
        dict_group.add_argument('--min-length', type=int, help='Minimum password length')
        dict_group.add_argument('--max-length', type=int, help='Maximum password length')
        dict_group.add_argument('--charset', help='Custom character set for password generation')
        
        # Network configuration
        net_group = parser.add_argument_group('Network Configuration')
        net_group.add_argument('--interface', help='Network interface to use')
        net_group.add_argument('--source-ip', help='Source IP address (random if not specified)')
        net_group.add_argument('--proxy', help='SOCKS proxy URL (e.g., socks5://127.0.0.1:9050)')
        net_group.add_argument('--dns-resolver', help='Custom DNS resolver')
        
        # Attack behavior
        behavior_group = parser.add_argument_group('Attack Behavior')
        behavior_group.add_argument('--threads', type=int, default=4, help='Number of threads to use')
        behavior_group.add_argument('--timeout', type=float, default=5.0, help='Connection timeout (seconds)')
        behavior_group.add_argument('--delay', type=float, default=0.0, 
                                  help='Delay between attempts (seconds)')
        behavior_group.add_argument('--max-attempts', type=int, help='Maximum login attempts per target')
        behavior_group.add_argument('--stop-on-success', action='store_true', 
                                  help='Stop attacking after first success')
        behavior_group.add_argument('--shuffle', action='store_true', 
                                  help='Randomize credential order')
        
        # Monitoring and output
        monitor_group = parser.add_argument_group('Monitoring')
        monitor_group.add_argument('--log-file', help='Log file for attempts')
        monitor_group.add_argument('--output-format', choices=['text', 'json', 'csv'], 
                                 default='text', help='Output format')
        monitor_group.add_argument('--save-valid', help='Save valid credentials to file')
        monitor_group.add_argument('--stats-interval', type=float, default=1.0, 
                                 help='Interval for printing statistics')
        monitor_group.add_argument('--verify-access', action='store_true', 
                                 help='Verify successful logins with a test command')
        monitor_group.add_argument('--silent', action='store_true', help='Suppress non-error output')
        
    def validate(self, args: argparse.Namespace) -> bool:
        # Validate target configuration
        if not (args.target or args.targets_file):
            logger.error("Either --target or --targets-file must be specified")
            return False
            
        if args.target and not (self.validator.validate_ip(args.target) or 
                               self.validator.validate_domain(args.target)):
            logger.error(f"Invalid target: {args.target}")
            return False
            
        if args.targets_file and not self.validator.validate_file_path(
            args.targets_file, check_readable=True
        ):
            logger.error(f"Invalid targets file: {args.targets_file}")
            return False
            
        if not self.validator.validate_port(args.port):
            logger.error(f"Invalid port number: {args.port}")
            return False
            
        # Validate authentication configuration
        if not any([args.username, args.usernames_file, args.key_file]):
            logger.error("No authentication method specified")
            return False
            
        if not any([args.password, args.passwords_file, args.wordlist, 
                    args.key_file, args.custom_wordlist]):
            logger.error("No password source specified")
            return False
            
        # Validate input files
        if args.usernames_file and not self.validator.validate_file_path(
            args.usernames_file, check_readable=True
        ):
            logger.error(f"Invalid usernames file: {args.usernames_file}")
            return False
            
        if args.passwords_file and not self.validator.validate_file_path(
            args.passwords_file, check_readable=True
        ):
            logger.error(f"Invalid passwords file: {args.passwords_file}")
            return False
            
        if args.wordlist and not self.validator.validate_file_path(
            args.wordlist, check_readable=True
        ):
            logger.error(f"Invalid wordlist file: {args.wordlist}")
            return False
            
        if args.custom_wordlist and not self.validator.validate_file_path(
            args.custom_wordlist, check_readable=True
        ):
            logger.error(f"Invalid custom wordlist file: {args.custom_wordlist}")
            return False
            
        if args.key_file and not self.validator.validate_file_path(
            args.key_file, check_readable=True
        ):
            logger.error(f"Invalid SSH key file: {args.key_file}")
            return False
            
        # Validate password length constraints
        if args.min_length is not None and args.min_length < 1:
            logger.error(f"Invalid minimum password length: {args.min_length}")
            return False
            
        if args.max_length is not None:
            if args.max_length < 1:
                logger.error(f"Invalid maximum password length: {args.max_length}")
                return False
            if args.min_length and args.max_length < args.min_length:
                logger.error("Maximum length cannot be less than minimum length")
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
        if args.threads <= 0:
            logger.error(f"Invalid thread count: {args.threads}")
            return False
            
        if args.timeout <= 0:
            logger.error(f"Invalid timeout: {args.timeout}")
            return False
            
        if args.delay < 0:
            logger.error(f"Invalid delay: {args.delay}")
            return False
            
        if args.max_attempts is not None and args.max_attempts <= 0:
            logger.error(f"Invalid maximum attempts: {args.max_attempts}")
            return False
            
        if args.stats_interval <= 0:
            logger.error(f"Invalid statistics interval: {args.stats_interval}")
            return False
            
        # Validate output files
        if args.log_file and not self.validator.validate_file_path(
            args.log_file, check_exists=False, check_readable=False
        ):
            logger.error(f"Invalid log file path: {args.log_file}")
            return False
            
        if args.save_valid and not self.validator.validate_file_path(
            args.save_valid, check_exists=False, check_readable=False
        ):
            logger.error(f"Invalid save file path: {args.save_valid}")
            return False
            
        return True
        
    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        attack_path = os.path.join(scripts_dir, 'ssh_brute_force')
        
        sys.path.insert(0, attack_path)
        try:
            import ssh_brute_force as attack_script
            
            # Create attack configuration
            config = {
                'target_ip': args.target,
                'port': args.port,
                'username': args.username,
                'wordlist_path': args.wordlist,
                'thread_count': args.threads,
                'timeout': args.timeout
            }
            
            # Run the attack
            logger.info(f"Running SSH brute force attack against {args.target}:{args.port}")
            attack_script.run_attack(config)
            
        except ImportError:
            logger.error("Failed to import SSH brute force attack script")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(attack_path)
