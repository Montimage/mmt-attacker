"""Credential Harvester attack implementation"""

import argparse
import sys
import os
from typing import Optional
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class CredentialHarvester(AttackBase):
    """Credential Harvester attack implementation"""
    
    name = "credential-harvester"
    description = "Perform credential harvesting attack"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--target', required=True, help='Target URL to clone')
        parser.add_argument('--port', type=int, default=80, help='Port to listen on')
        parser.add_argument('--interface', help='Network interface to listen on')
        parser.add_argument('--output', help='Output file to save harvested credentials')
        parser.add_argument('--ssl', action='store_true', help='Use HTTPS instead of HTTP')
        parser.add_argument('--cert', help='SSL certificate file (required if --ssl is used)')
        parser.add_argument('--key', help='SSL key file (required if --ssl is used)')
        
    def validate(self, args: argparse.Namespace) -> bool:
        if not self.validator.validate_port(args.port):
            logger.error(f"Invalid port number: {args.port}")
            return False
        if args.interface and not self.validator.validate_interface(args.interface):
            logger.error(f"Invalid interface: {args.interface}")
            return False
        if args.ssl:
            if not args.cert or not os.path.isfile(args.cert):
                logger.error("SSL certificate file is required when using HTTPS")
                return False
            if not args.key or not os.path.isfile(args.key):
                logger.error("SSL key file is required when using HTTPS")
                return False
        return True
        
    def run(self, args: argparse.Namespace) -> None:
        # Import the original attack script
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        attack_path = os.path.join(scripts_dir, 'credential_harvester')
        
        sys.path.insert(0, attack_path)
        try:
            import credential_harvester as attack_script
            
            # Create attack configuration
            config = {
                'target_url': args.target,
                'port': args.port,
                'interface': args.interface,
                'output_file': args.output,
                'use_ssl': args.ssl,
                'ssl_cert': args.cert,
                'ssl_key': args.key
            }
            
            # Run the attack
            logger.info(f"Running credential harvester attack cloning {args.target}")
            attack_script.run_attack(config)
            
        except ImportError:
            logger.error("Failed to import credential harvester attack script")
            raise
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
        finally:
            sys.path.remove(attack_path)
