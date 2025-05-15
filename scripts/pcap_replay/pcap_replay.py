#!/usr/bin/env python3
"""
PCAP Replay Attack Simulation

This module provides a class-based implementation for simulating network attacks by
replaying captured network traffic (PCAP files) with customizable parameters. It allows
for modifying destination IP addresses and ports to target specific systems.

The module supports various features:
- Customizable packet replay rate
- IP and port translation
- Interface selection
- Packet filtering
- Detailed logging and statistics
- Loop mode for continuous replay

IMPORTANT ETHICAL AND LEGAL NOTICE:
This tool should ONLY be used for legitimate security testing with proper authorization.
Unauthorized use against systems without explicit permission is illegal and unethical.
The authors assume no liability for misuse of this software.

Usage Examples:
    # Basic usage with command line arguments
    python pcap_replay.py -f /path/to/attack.pcap -t 192.168.1.10 -i eth0
    
    # Modify both IP and port
    python pcap_replay.py -f /path/to/attack.pcap -t 192.168.1.10 -p 8080 -i eth0
    
    # Replay with custom rate
    python pcap_replay.py -f /path/to/attack.pcap -t 192.168.1.10 -i eth0 -r 10

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os
import sys
import time
import argparse
import ipaddress
import subprocess
from typing import List, Dict, Optional, Any, Tuple, Union
from pathlib import Path

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

class PCAPReplayAttack:
    """
    A class to perform network attack simulations by replaying PCAP files.
    
    This class provides methods to replay captured network traffic with
    customizable parameters such as target IP, port, and interface.
    
    Attributes:
        pcap_file (str): Path to the PCAP file to replay
        target_ip (str): Target IP address to send traffic to
        target_port (Optional[int]): Target port to send traffic to
        interface (str): Network interface to use for sending packets
        original_ip (Optional[str]): Original destination IP in the PCAP file
        original_port (Optional[int]): Original destination port in the PCAP file
        rate (float): Packet replay rate multiplier
        loop_count (int): Number of times to replay the PCAP file
        verbose (bool): Whether to enable verbose output
    """
    
    def __init__(self, 
                 pcap_file: str, 
                 target_ip: str,
                 interface: str,
                 target_port: Optional[int] = None,
                 original_ip: Optional[str] = None,
                 original_port: Optional[int] = None,
                 rate: float = 1.0,
                 loop_count: int = 1,
                 verbose: bool = False):
        """
        Initialize the PCAP replay attack simulator.
        
        Args:
            pcap_file (str): Path to the PCAP file to replay
            target_ip (str): Target IP address to send traffic to
            interface (str): Network interface to use for sending packets
            target_port (Optional[int]): Target port to send traffic to
            original_ip (Optional[str]): Original destination IP in the PCAP file
            original_port (Optional[int]): Original destination port in the PCAP file
            rate (float): Packet replay rate multiplier
            loop_count (int): Number of times to replay the PCAP file
            verbose (bool): Whether to enable verbose output
            
        Raises:
            ValueError: If pcap_file does not exist
            ValueError: If target_ip is not a valid IP address
            ValueError: If target_port is not a valid port number
        """
        # Validate PCAP file
        if not os.path.exists(pcap_file):
            raise ValueError(f"PCAP file not found: {pcap_file}")
        self.pcap_file = pcap_file
        
        # Validate target IP
        try:
            ipaddress.ip_address(target_ip)
            self.target_ip = target_ip
        except ValueError:
            raise ValueError(f"Invalid target IP address: {target_ip}")
        
        # Validate target port if provided
        if target_port is not None:
            if not (0 < target_port < 65536):
                raise ValueError(f"Invalid target port: {target_port}. Must be between 1-65535.")
        self.target_port = target_port
        
        # Set other parameters
        self.interface = interface
        self.original_ip = original_ip
        self.original_port = original_port
        self.rate = max(0.1, rate)  # Ensure reasonable rate
        self.loop_count = max(1, loop_count)  # Ensure at least 1 loop
        self.verbose = verbose
        
        # Initialize state variables
        self.start_time = None
        self.end_time = None
        self.packets_sent = 0
        
        logger.info(f"Initialized PCAP replay attack simulation")
        logger.info(f"PCAP file: {pcap_file}")
        logger.info(f"Target: {target_ip}{f':{target_port}' if target_port else ''}")
        logger.info(f"Interface: {interface}")
        if self.verbose:
            logger.info(f"Rate: {rate}x, Loop count: {loop_count}")
            if original_ip:
                logger.info(f"Original IP: {original_ip}")
            if original_port:
                logger.info(f"Original port: {original_port}")
    
    def _check_tcpreplay_installed(self) -> bool:
        """
        Check if tcpreplay is installed on the system.
        
        Returns:
            bool: True if tcpreplay is installed, False otherwise
        """
        try:
            result = subprocess.run(
                ["which", "tcpreplay-edit"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error checking for tcpreplay-edit: {str(e)}")
            return False
    
    def _build_command(self) -> List[str]:
        """
        Build the tcpreplay command with appropriate options.
        
        Returns:
            List[str]: Command and arguments as a list
        """
        cmd = ["tcpreplay-edit"]
        
        # Add interface
        cmd.extend(["-i", self.interface])
        
        # Add rate
        if self.rate != 1.0:
            cmd.extend(["-x", str(self.rate)])
        
        # Add loop count
        if self.loop_count > 1:
            cmd.extend(["--loop", str(self.loop_count)])
        
        # Add IP rewriting if original IP is specified
        if self.original_ip:
            cmd.extend(["-D", f"{self.original_ip}:{self.target_ip}"])
            # Also rewrite source IP to maintain consistency
            cmd.extend(["-S", f"{self.original_ip}:{self.target_ip}"])
        
        # Add port rewriting if both original and target ports are specified
        if self.original_port and self.target_port:
            cmd.extend(["-r", f"{self.original_port}:{self.target_port}"])
        
        # Add statistics options
        cmd.extend(["-tK"])  # Print stats, send at layer 3
        
        # Add PCAP file
        cmd.append(self.pcap_file)
        
        return cmd
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the PCAP replay attack.
        
        Returns:
            Dict[str, Any]: Statistics about the attack execution
        """
        # Check if tcpreplay-edit is installed
        if not self._check_tcpreplay_installed():
            logger.error("tcpreplay-edit is not installed. Please install it to use this script.")
            return {"success": False, "error": "tcpreplay-edit not installed"}
        
        # Build the command
        cmd = self._build_command()
        cmd_str = " ".join(cmd)
        
        logger.info(f"Executing command: {cmd_str}")
        
        # Record start time
        self.start_time = time.time()
        
        try:
            # Execute the command
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True
            )
            
            # Process output in real-time
            stdout_lines = []
            for line in process.stdout:
                line = line.strip()
                if line:
                    logger.info(line)
                    stdout_lines.append(line)
                    # Try to extract packet count from output
                    if "packets" in line and "sent" in line:
                        try:
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if part == "packets" and i > 0:
                                    self.packets_sent = int(parts[i-1])
                                    break
                        except (ValueError, IndexError):
                            pass
            
            # Wait for process to complete
            process.wait()
            
            # Record end time
            self.end_time = time.time()
            
            # Check if process was successful
            if process.returncode != 0:
                stderr = process.stderr.read()
                logger.error(f"Command failed with return code {process.returncode}: {stderr}")
                return {
                    "success": False,
                    "error": f"Command failed with return code {process.returncode}",
                    "stderr": stderr
                }
            
            # Get statistics
            stats = self._get_statistics()
            self._print_summary(stats)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error executing PCAP replay: {str(e)}")
            self.end_time = time.time()
            return {"success": False, "error": str(e)}
    
    def _get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the attack execution.
        
        Returns:
            Dict[str, Any]: Statistics including packets sent, duration, etc.
        """
        duration = (self.end_time - self.start_time) if self.end_time else 0
        
        return {
            "success": True,
            "pcap_file": self.pcap_file,
            "target_ip": self.target_ip,
            "target_port": self.target_port,
            "interface": self.interface,
            "packets_sent": self.packets_sent,
            "duration": duration,
            "packets_per_second": self.packets_sent / duration if duration > 0 else 0,
            "loop_count": self.loop_count,
            "rate": self.rate
        }
    
    def _print_summary(self, stats: Dict[str, Any]) -> None:
        """
        Print a summary of the attack execution.
        
        Args:
            stats (Dict[str, Any]): Statistics from _get_statistics()
        """
        logger.info("=" * 60)
        logger.info("PCAP Replay Attack Summary")
        logger.info("=" * 60)
        logger.info(f"PCAP File:          {stats['pcap_file']}")
        logger.info(f"Target:             {stats['target_ip']}{f':{stats["target_port"]}' if stats['target_port'] else ''}")
        logger.info(f"Interface:          {stats['interface']}")
        logger.info(f"Packets Sent:       {stats['packets_sent']}")
        logger.info(f"Duration:           {stats['duration']:.2f} seconds")
        logger.info(f"Rate:               {stats['packets_per_second']:.2f} packets/second")
        logger.info("=" * 60)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the PCAP replay attack.
    
    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="PCAP Replay Attack Simulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pcap_replay.py -f attack.pcap -t 192.168.1.10 -i eth0
  python pcap_replay.py -f attack.pcap -t 192.168.1.10 -p 8080 -i eth0 -o 192.168.0.1 -g 80
  python pcap_replay.py -f attack.pcap -t 192.168.1.10 -i eth0 -r 10 -l 5
"""
    )
    
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Path to the PCAP file to replay"
    )
    
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target IP address to send traffic to"
    )
    
    parser.add_argument(
        "-i", "--interface",
        required=True,
        help="Network interface to use for sending packets"
    )
    
    parser.add_argument(
        "-p", "--port",
        type=int,
        help="Target port to send traffic to"
    )
    
    parser.add_argument(
        "-o", "--original-ip",
        help="Original destination IP in the PCAP file"
    )
    
    parser.add_argument(
        "-g", "--original-port",
        type=int,
        help="Original destination port in the PCAP file"
    )
    
    parser.add_argument(
        "-r", "--rate",
        type=float,
        default=1.0,
        help="Packet replay rate multiplier (default: 1.0)"
    )
    
    parser.add_argument(
        "-l", "--loop",
        type=int,
        default=1,
        help="Number of times to replay the PCAP file (default: 1)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the PCAP replay attack simulation.
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    try:
        # Create the attack simulator
        attack = PCAPReplayAttack(
            pcap_file=args.file,
            target_ip=args.target,
            interface=args.interface,
            target_port=args.port,
            original_ip=args.original_ip,
            original_port=args.original_port,
            rate=args.rate,
            loop_count=args.loop,
            verbose=args.verbose
        )
        
        # Execute the attack
        attack.execute()
        
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # Display ethical notice
    print("=" * 80)
    print("IMPORTANT ETHICAL AND LEGAL NOTICE:")
    print("This tool should ONLY be used for legitimate security testing with proper authorization.")
    print("Unauthorized use against systems without explicit permission is illegal and unethical.")
    print("=" * 80)
    print()
    
    main()
