"""Perform XSS vulnerability testing"""

import argparse
import sys
import os
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class Xss(AttackBase):
    """Perform XSS vulnerability testing"""

    name = "xss"
    description = "Perform XSS vulnerability testing"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--url', required=True, help='Target URL')
        parser.add_argument('--param', required=True, help='Parameter to test')
        parser.add_argument('--payloads', help='Custom payloads file')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Basic validation - extend as needed
        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'xss')
        sys.path.insert(0, path)
        try:
            import xss as attack_module
            logger.info(f"Running xss attack")

            # Load payloads
            if args.payloads:
                with open(args.payloads, 'r') as f:
                    payloads = [line.strip() for line in f if line.strip()]
            else:
                payloads = attack_module.DEFAULT_PAYLOADS

            # Create and execute attack
            attack = attack_module.XSSAttack(
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
