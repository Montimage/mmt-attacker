"""Perform HTTP flood attack"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class HttpFlood(AttackBase):
    """Perform HTTP flood attack"""

    name = "http-flood"
    description = "Perform HTTP flood attack"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--url', required=True, help='Target URL')
        parser.add_argument('--count', type=int, default=100, help='Number of requests (default: 100)')
        parser.add_argument('--threads', type=int, default=10, help='Number of threads (default: 10)')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Validate URL
        if not self.validator.validate_url(args.url):
            logger.error(f"Invalid URL: {args.url}")
            return False

        # Validate count
        if args.count <= 0:
            logger.error(f"Invalid count: {args.count}. Must be greater than 0")
            return False

        # Validate threads
        if args.threads <= 0:
            logger.error(f"Invalid thread count: {args.threads}. Must be greater than 0")
            return False
        if args.threads > 100:
            logger.warning(f"Large thread count ({args.threads}) may overwhelm the system")

        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'http_flood')
        sys.path.insert(0, path)
        try:
            import http_flood as attack_module
            logger.info(f"Running http-flood attack")

            # Create and execute attack
            attack = attack_module.HTTPFloodAttack(
                args.url,
                args.count,
                args.threads,
                args.verbose
            )
            attack.execute()
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
