"""Perform directory traversal attack"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class DirectoryTraversal(AttackBase):
    """Perform directory traversal attack"""

    name = "directory-traversal"
    description = "Perform directory traversal attack"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--url', required=True, help='Target URL')
        parser.add_argument('--param', required=True, help='Parameter to test')
        parser.add_argument('--payloads', help='Custom payloads file')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Validate URL
        if not self.validator.validate_url(args.url):
            logger.error(f"Invalid URL: {args.url}")
            return False

        # Validate param is not empty
        if not args.param or not args.param.strip():
            logger.error("Parameter name cannot be empty")
            return False

        # Validate payloads file if provided
        if args.payloads:
            if not self.validator.validate_file_path(args.payloads, check_exists=True, check_readable=True):
                logger.error(f"Payloads file not found or not readable: {args.payloads}")
                return False

        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'directory_traversal')
        sys.path.insert(0, path)
        try:
            import directory_traversal as attack_module
            logger.info(f"Running directory-traversal attack")

            # Load payloads
            if args.payloads:
                with open(args.payloads, 'r') as f:
                    payloads = [line.strip() for line in f if line.strip()]
            else:
                payloads = attack_module.DEFAULT_PAYLOADS

            # Create and execute attack
            attack = attack_module.DirectoryTraversalAttack(
                args.url,
                args.param,
                payloads,
                args.verbose
            )
            attack.execute()
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
