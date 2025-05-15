"""Base class for all MMT-Attacker attacks"""

import argparse
import ipaddress
import logging
import os
import re
import socket
import netifaces
from typing import Optional, List, Dict, Union
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class AttackValidator:
    """Enhanced validator class for attack parameters"""
    
    @staticmethod
    def validate_ip(ip: str, allow_private: bool = True, allow_loopback: bool = True) -> bool:
        """Validate IP address format with additional checks"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            if not allow_private and ip_obj.is_private:
                logger.error(f"Private IP addresses not allowed: {ip}")
                return False
            if not allow_loopback and ip_obj.is_loopback:
                logger.error(f"Loopback addresses not allowed: {ip}")
                return False
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_port(port: int, restricted: bool = True) -> bool:
        """Validate port number with additional checks"""
        if not (0 <= port <= 65535):
            return False
        if restricted and port < 1024:
            logger.warning(f"Port {port} requires root/admin privileges")
        return True
    
    @staticmethod
    def validate_interface(interface: str) -> bool:
        """Validate network interface existence and status"""
        try:
            if interface not in netifaces.interfaces():
                logger.error(f"Interface not found: {interface}")
                return False
            # Check if interface has an IP address assigned
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET not in addrs:
                logger.warning(f"Interface {interface} has no IPv4 address")
            return True
        except Exception as e:
            logger.error(f"Interface validation error: {str(e)}")
            return False
    
    @staticmethod
    def validate_url(url: str, allowed_schemes: List[str] = ['http', 'https']) -> bool:
        """Validate URL format and accessibility"""
        try:
            parsed = urlparse(url)
            if parsed.scheme not in allowed_schemes:
                logger.error(f"Invalid URL scheme: {parsed.scheme}")
                return False
            if not parsed.netloc:
                logger.error("Missing hostname in URL")
                return False
            return True
        except Exception:
            return False
    
    @staticmethod
    def validate_file_path(path: str, check_exists: bool = True, 
                          check_readable: bool = True, 
                          allowed_extensions: List[str] = None) -> bool:
        """Validate file path with comprehensive checks"""
        if check_exists and not os.path.exists(path):
            logger.error(f"File not found: {path}")
            return False
        if check_readable and not os.access(path, os.R_OK):
            logger.error(f"File not readable: {path}")
            return False
        if allowed_extensions:
            ext = os.path.splitext(path)[1].lower()
            if ext not in allowed_extensions:
                logger.error(f"Invalid file extension: {ext}")
                return False
        return True
    
    @staticmethod
    def validate_domain(domain: str) -> bool:
        """Validate domain name format and resolution"""
        if not domain or len(domain) > 255:
            return False
        pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'
            r'[a-zA-Z]{2,}$'
        )
        if not pattern.match(domain):
            return False
        try:
            socket.gethostbyname(domain)
            return True
        except socket.error:
            logger.warning(f"Could not resolve domain: {domain}")
            return False
    
    @staticmethod
    def validate_mac_address(mac: str) -> bool:
        """Validate MAC address format"""
        pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        return bool(pattern.match(mac))
    
    @staticmethod
    def validate_network(network: str) -> bool:
        """Validate network CIDR format"""
        try:
            ipaddress.ip_network(network, strict=False)
            return True
        except ValueError:
            return False

class AttackBase:
    """Base class for all attacks"""
    
    name: str = "base"
    description: str = "Base attack class"
    
    def __init__(self):
        self.validator = AttackValidator()
        
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add attack-specific arguments to parser"""
        raise NotImplementedError
        
    def validate(self, args: argparse.Namespace) -> bool:
        """Validate attack-specific arguments"""
        raise NotImplementedError
        
    def run(self, args: argparse.Namespace) -> None:
        """Run the attack"""
        raise NotImplementedError
