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
        parser.add_argument('--payloads', , help='Custom payloads file')
        parser.add_argument('--verbose', action='store_true', help='Verbose output')

    def validate(self, args: argparse.Namespace) -> bool:
        # Basic validation - extend as needed
        return True

    def run(self, args: argparse.Namespace) -> None:
        scripts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts')
        path = os.path.join(scripts_dir, 'directory_traversal')
        sys.path.insert(0, path)
        try:
            import directory_traversal as attack_module
            logger.info(f"Running directory-traversal attack")
            # Attack execution handled by module
        except Exception as e:
            logger.error(f"Attack failed: {e}")
            raise
        finally:
            sys.path.remove(path)
