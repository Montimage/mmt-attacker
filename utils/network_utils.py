#!/usr/bin/env python3
"""
Network Utilities Module

This module provides utility functions for network interface and IP address operations,
including interface detection, IP address retrieval, and connectivity checking.

It simplifies common network-related tasks required by the MMT Attacker framework,
such as finding interfaces that can reach the internet and retrieving IP addresses.

Author: Montimage
License: Proprietary
"""

import socket
import ipaddress
from typing import List, Dict, Optional, Union, Tuple, Any

# Import centralized logger
from logger import get_logger

# Third-party imports
try:
    import netifaces as ni
except ImportError:
    raise ImportError(
        "The 'netifaces' module is required. "
        "Please install it using 'pip install netifaces'."
    )

# Get module logger
logger = get_logger(__name__)

def get_all_interfaces() -> List[str]:
    """Get all available network interfaces on the system.
    
    This function returns a list of all network interfaces available on the current system,
    regardless of their state (up/down) or configuration.
    
    Returns:
        List[str]: List of available network interface names
        
    Example:
        >>> get_all_interfaces()
        ['lo0', 'en0', 'en1', 'bridge0']
    """
    try:
        interfaces = ni.interfaces()
        logger.debug(f"Found {len(interfaces)} network interfaces: {interfaces}")
        return interfaces
    except Exception as e:
        logger.error(f"Error retrieving network interfaces: {str(e)}")
        return []

def check_if_interface_exist(iface: str) -> bool:
    """Check if a given network interface exists on the system.
    
    Args:
        iface (str): Name of the interface to check
        
    Returns:
        bool: True if the interface exists, False otherwise
        
    Example:
        >>> check_if_interface_exist('en0')
        True
        >>> check_if_interface_exist('nonexistent0')
        False
    """
    if not iface:
        logger.warning("Empty interface name provided")
        return False
        
    try:
        interfaces = ni.interfaces()
        exists = iface in interfaces
        if not exists:
            logger.debug(f"Interface '{iface}' not found. Available interfaces: {interfaces}")
        return exists
    except Exception as e:
        logger.error(f"Error checking interface '{iface}': {str(e)}")
        return False

def get_ip_address_by_machine_hostname() -> Optional[str]:
    """Get the primary IP address of the current machine using its hostname.
    
    This function retrieves the hostname of the current machine and resolves it
    to an IP address. Note that this may return a loopback address (127.0.0.1)
    depending on the system configuration.
    
    Returns:
        Optional[str]: The IP address of the machine, or None if resolution fails
        
    Example:
        >>> get_ip_address_by_machine_hostname()
        '192.168.1.100'
    """
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        logger.debug(f"Resolved hostname '{hostname}' to IP address '{ip_address}'")
        return ip_address
    except socket.gaierror as e:
        logger.error(f"Failed to resolve hostname to IP address: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error getting IP address by hostname: {str(e)}")
        return None

def is_valid_ip_address(ip_address: str) -> bool:
    """Validate if a string is a valid IPv4 or IPv6 address.
    
    Args:
        ip_address (str): IP address to validate
        
    Returns:
        bool: True if valid IP address, False otherwise
        
    Example:
        >>> is_valid_ip_address('192.168.1.1')
        True
        >>> is_valid_ip_address('not-an-ip')
        False
    """
    if not ip_address:
        return False
        
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False


def get_online_ip_address(online_server_ip: str = "8.8.8.8", port: int = 80, timeout: float = 2.0) -> Optional[str]:
    """Get the IP address of the current machine that can connect to a given server.
    
    This function attempts to establish a UDP socket connection to the specified server
    and retrieves the local IP address used for that connection. This is useful for
    determining which local IP address would be used for outbound internet traffic.
    
    Args:
        online_server_ip (str): The remote server to connect to. Defaults to "8.8.8.8" (Google DNS).
        port (int): The port to connect to. Defaults to 80.
        timeout (float): Socket timeout in seconds. Defaults to 2.0.
        
    Returns:
        Optional[str]: The local IP address used for the connection, or None if connection fails
        
    Example:
        >>> get_online_ip_address()
        '192.168.1.100'
    """
    # Validate input IP address
    if not is_valid_ip_address(online_server_ip):
        logger.error(f"Invalid IP address: {online_server_ip}")
        return None
        
    # Validate port number
    if not (0 < port < 65536):
        logger.error(f"Invalid port number: {port}")
        return None
        
    s = None
    try:
        # Create a UDP socket (SOCK_DGRAM)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        
        # Connect to the remote server
        s.connect((online_server_ip, port))
        
        # Get the local IP address used for this connection
        ip_address = s.getsockname()[0]
        logger.debug(f"Found online IP address: {ip_address} (via {online_server_ip})")
        return ip_address
        
    except socket.timeout:
        logger.error(f"Connection to {online_server_ip}:{port} timed out")
        return None
    except socket.error as e:
        logger.error(f"Socket error connecting to {online_server_ip}:{port}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error getting online IP address: {str(e)}")
        return None
    finally:
        # Always close the socket if it was created
        if s:
            s.close()

def get_online_interface(online_server_ip: str = "8.8.8.8", port: int = 80, timeout: float = 2.0) -> Optional[str]:
    """Get the network interface that can reach a given online server.
    
    This function identifies which network interface is used to connect to the specified
    server by matching the local IP address used for the connection with the IP addresses
    assigned to each interface.
    
    Args:
        online_server_ip (str): The remote server to connect to. Defaults to "8.8.8.8" (Google DNS).
        port (int): The port to connect to. Defaults to 80.
        timeout (float): Socket timeout in seconds. Defaults to 2.0.
        
    Returns:
        Optional[str]: The name of the interface that can reach the server, or None if no interface found
        
    Example:
        >>> get_online_interface()
        'en0'
    """
    # Get the IP address used to connect to the online server
    ip_address = get_online_ip_address(online_server_ip, port, timeout)
    if not ip_address:
        logger.error("Failed to determine online IP address")
        return None
    
    # Check each interface to find which one has this IP address
    for interface in get_all_interfaces():
        # Skip interfaces that are down
        if not is_interface_up(interface):
            continue
            
        # Get all IPv4 addresses for this interface
        addresses = get_interface_ipv4_addresses(interface)
        if ip_address in addresses:
            logger.debug(f"Found online interface: {interface} with IP {ip_address}")
            return interface
    
    logger.error(f"Could not find interface with IP address {ip_address}")
    return None

def get_interface_addresses(interface: str) -> Dict[int, List[Dict[str, str]]]:
    """Get all addresses (IPv4, IPv6, etc.) assigned to a specific interface.
    
    Args:
        interface (str): Name of the network interface
        
    Returns:
        Dict[int, List[Dict[str, str]]]: Dictionary mapping address families to address information
            - Keys are address family constants (e.g., socket.AF_INET for IPv4)
            - Values are lists of address dictionaries with keys like 'addr', 'netmask', etc.
        
    Example:
        >>> get_interface_addresses('en0')
        {2: [{'addr': '192.168.1.100', 'netmask': '255.255.255.0', 'broadcast': '192.168.1.255'}],
         30: [{'addr': 'fe80::1234:5678:9abc:def0%en0', 'netmask': 'ffff:ffff:ffff:ffff::', 'flags': 0}]}
    """
    if not check_if_interface_exist(interface):
        logger.error(f"Interface '{interface}' does not exist")
        return {}
        
    try:
        addresses = ni.ifaddresses(interface)
        logger.debug(f"Found addresses for interface '{interface}': {addresses}")
        return addresses
    except Exception as e:
        logger.error(f"Error getting addresses for interface '{interface}': {str(e)}")
        return {}

def get_interface_ipv4_addresses(interface: str) -> List[str]:
    """Get all IPv4 addresses assigned to a specific interface.
    
    Args:
        interface (str): Name of the network interface
        
    Returns:
        List[str]: List of IPv4 addresses assigned to the interface
        
    Example:
        >>> get_interface_ipv4_addresses('en0')
        ['192.168.1.100']
    """
    addresses = []
    
    # Get all addresses for the interface
    all_addresses = get_interface_addresses(interface)
    
    # Extract IPv4 addresses (family AF_INET = 2)
    if socket.AF_INET in all_addresses:
        for addr_info in all_addresses[socket.AF_INET]:
            if 'addr' in addr_info:
                addresses.append(addr_info['addr'])
                
    return addresses

def is_interface_up(interface: str) -> bool:
    """Check if a network interface is up and running.
    
    Args:
        interface (str): Name of the network interface
        
    Returns:
        bool: True if the interface is up, False otherwise
        
    Example:
        >>> is_interface_up('en0')
        True
    """
    if not check_if_interface_exist(interface):
        logger.error(f"Interface '{interface}' does not exist")
        return False
        
    try:
        # Check if the interface has any addresses assigned
        addresses = ni.ifaddresses(interface)
        
        # If the interface has any addresses (IPv4, IPv6, etc.), it's likely up
        # Different platforms may have different ways to determine if an interface is up
        # This is a simple heuristic that works on most systems
        return bool(addresses)
    except Exception as e:
        logger.error(f"Error checking if interface '{interface}' is up: {str(e)}")
        return False

def get_default_gateway() -> Optional[str]:
    """Get the default gateway IP address.
    
    Returns:
        Optional[str]: The IP address of the default gateway, or None if not found
        
    Example:
        >>> get_default_gateway()
        '192.168.1.1'
    """
    try:
        gateways = ni.gateways()
        if 'default' in gateways and socket.AF_INET in gateways['default']:
            gateway_ip = gateways['default'][socket.AF_INET][0]
            logger.debug(f"Found default gateway: {gateway_ip}")
            return gateway_ip
        else:
            logger.warning("No default gateway found")
            return None
    except Exception as e:
        logger.error(f"Error getting default gateway: {str(e)}")
        return None

def get_all_active_interfaces() -> List[str]:
    """Get all active network interfaces (interfaces that are up).
    
    Returns:
        List[str]: List of active interface names
        
    Example:
        >>> get_all_active_interfaces()
        ['lo0', 'en0']
    """
    active_interfaces = []
    for interface in get_all_interfaces():
        if is_interface_up(interface):
            active_interfaces.append(interface)
    return active_interfaces

def print_network_info() -> None:
    """Print comprehensive network information for all interfaces."""
    print("\n" + "=" * 60)
    print("NETWORK INTERFACES INFORMATION")
    print("=" * 60)
    
    # Get all interfaces
    interfaces = get_all_interfaces()
    print(f"Found {len(interfaces)} network interfaces:")
    
    # Get online interface
    online_iface = get_online_interface()
    if online_iface:
        print(f"Online interface: {online_iface}")
        online_ip = get_online_ip_address()
        if online_ip:
            print(f"Online IP address: {online_ip}")
    else:
        print("No online interface detected")
    
    # Get default gateway
    gateway = get_default_gateway()
    if gateway:
        print(f"Default gateway: {gateway}")
    else:
        print("No default gateway detected")
    
    # Print detailed information for each interface
    for iface in interfaces:
        print("\n" + "-" * 60)
        print(f"Interface: {iface}")
        print(f"Status: {'UP' if is_interface_up(iface) else 'DOWN'}")
        
        # Get IPv4 addresses
        ipv4_addresses = get_interface_ipv4_addresses(iface)
        if ipv4_addresses:
            print(f"IPv4 addresses: {', '.join(ipv4_addresses)}")
        else:
            print("No IPv4 addresses assigned")
        
        # Get all addresses (including IPv6, etc.)
        all_addresses = get_interface_addresses(iface)
        if all_addresses:
            for family, addresses in all_addresses.items():
                if family == socket.AF_INET:
                    family_name = "IPv4"
                elif family == socket.AF_INET6:
                    family_name = "IPv6"
                else:
                    family_name = f"Family {family}"
                
                for addr_info in addresses:
                    addr_str = addr_info.get('addr', 'N/A')
                    netmask = addr_info.get('netmask', 'N/A')
                    broadcast = addr_info.get('broadcast', 'N/A')
                    print(f"  {family_name}: {addr_str}")
                    print(f"    Netmask: {netmask}")
                    if broadcast != 'N/A':
                        print(f"    Broadcast: {broadcast}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Network Utilities Command Line Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python network_utils.py --all
  python network_utils.py --interfaces
  python network_utils.py --online-ip
  python network_utils.py --interface eth0
"""
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Display all network information"
    )
    
    parser.add_argument(
        "--interfaces",
        action="store_true",
        help="List all network interfaces"
    )
    
    parser.add_argument(
        "--active-interfaces",
        action="store_true",
        help="List all active network interfaces"
    )
    
    parser.add_argument(
        "--online-ip",
        action="store_true",
        help="Display the online IP address"
    )
    
    parser.add_argument(
        "--online-interface",
        action="store_true",
        help="Display the online interface"
    )
    
    parser.add_argument(
        "--gateway",
        action="store_true",
        help="Display the default gateway"
    )
    
    parser.add_argument(
        "--interface",
        metavar="IFACE",
        help="Display information for a specific interface"
    )
    
    parser.add_argument(
        "--check-interface",
        metavar="IFACE",
        help="Check if a specific interface exists"
    )
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        exit(0)
    
    # Process arguments
    if args.all:
        print_network_info()
    
    if args.interfaces:
        interfaces = get_all_interfaces()
        print(f"Available network interfaces ({len(interfaces)}):\n")
        for iface in interfaces:
            print(f"  - {iface}")
    
    if args.active_interfaces:
        active_interfaces = get_all_active_interfaces()
        print(f"Active network interfaces ({len(active_interfaces)}):\n")
        for iface in active_interfaces:
            print(f"  - {iface}")
    
    if args.online_ip:
        ip = get_online_ip_address()
        if ip:
            print(f"Online IP address: {ip}")
        else:
            print("Failed to determine online IP address")
    
    if args.online_interface:
        iface = get_online_interface()
        if iface:
            print(f"Online interface: {iface}")
        else:
            print("Failed to determine online interface")
    
    if args.gateway:
        gateway = get_default_gateway()
        if gateway:
            print(f"Default gateway: {gateway}")
        else:
            print("Failed to determine default gateway")
    
    if args.interface:
        iface = args.interface
        print(f"Information for interface '{iface}':")
        
        if not check_if_interface_exist(iface):
            print(f"  Interface '{iface}' does not exist")
            exit(1)
        
        print(f"  Status: {'UP' if is_interface_up(iface) else 'DOWN'}")
        
        ipv4_addresses = get_interface_ipv4_addresses(iface)
        if ipv4_addresses:
            print(f"  IPv4 addresses: {', '.join(ipv4_addresses)}")
        else:
            print("  No IPv4 addresses assigned")
        
        all_addresses = get_interface_addresses(iface)
        if all_addresses:
            for family, addresses in all_addresses.items():
                if family == socket.AF_INET:
                    family_name = "IPv4"
                elif family == socket.AF_INET6:
                    family_name = "IPv6"
                else:
                    family_name = f"Family {family}"
                
                for addr_info in addresses:
                    addr_str = addr_info.get('addr', 'N/A')
                    netmask = addr_info.get('netmask', 'N/A')
                    broadcast = addr_info.get('broadcast', 'N/A')
                    print(f"  {family_name}: {addr_str}")
                    print(f"    Netmask: {netmask}")
                    if broadcast != 'N/A':
                        print(f"    Broadcast: {broadcast}")
    
    if args.check_interface:
        iface = args.check_interface
        exists = check_if_interface_exist(iface)
        print(f"Interface '{iface}': {'EXISTS' if exists else 'DOES NOT EXIST'}")
