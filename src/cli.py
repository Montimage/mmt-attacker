#!/usr/bin/env python3

import argparse
import sys
import os
from typing import List, Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import all attack modules
from attacks import (
    ArpSpoofing,
    SynFlood,
    UdpFlood,
    IcmpFlood,
    Mitm,
    DhcpStarvation,
    MacFlooding,
    VlanHopping,
    BgpHijacking,
    DnsAmplification,
    HttpDos,
    HttpFlood,
    Slowloris,
    Xss,
    DirectoryTraversal,
    Xxe,
    SslStrip,
    SmurfAttack,
    NtpAmplification,
    SshBruteForce,
    FtpBruteForce,
    RdpBruteForce,
    SqlInjection,
    CredentialHarvester,
    PingOfDeath,
    PcapReplay
)

def get_available_attacks() -> Dict[str, Any]:
    """Return dictionary of available attacks"""
    attack_classes = [
        ArpSpoofing,
        SynFlood,
        UdpFlood,
        IcmpFlood,
        Mitm,
        DhcpStarvation,
        MacFlooding,
        VlanHopping,
        BgpHijacking,
        DnsAmplification,
        HttpDos,
        HttpFlood,
        Slowloris,
        Xss,
        DirectoryTraversal,
        Xxe,
        SslStrip,
        SmurfAttack,
        NtpAmplification,
        SshBruteForce,
        FtpBruteForce,
        RdpBruteForce,
        SqlInjection,
        CredentialHarvester,
        PingOfDeath,
        PcapReplay
    ]
    attacks = [attack() for attack in attack_classes]
    return {attack.name: attack for attack in attacks}

def main():
    # Create main parser
    parser = argparse.ArgumentParser(
        description='MMT-Attacker - Network Attack Simulation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add global arguments
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    # Create subparsers for different attacks
    subparsers = parser.add_subparsers(dest='attack', help='Available attacks')
    
    # Register available attacks
    attacks = get_available_attacks()
    for name, attack in attacks.items():
        attack_parser = subparsers.add_parser(name, help=attack.description)
        attack.add_arguments(attack_parser)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # If no attack specified, show help and exit
    if not args.attack:
        parser.print_help()
        sys.exit(1)
    
    # Get selected attack
    attack = attacks[args.attack]
    
    # Validate attack arguments
    if not attack.validate(args):
        logger.error("Attack validation failed. Please check your arguments.")
        sys.exit(1)
    
    try:
        # Run the attack
        attack.run(args)
    except KeyboardInterrupt:
        logger.info("\nAttack interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Attack failed: {str(e)}")
        if args.verbose:
            logger.exception("Detailed error information:")
        sys.exit(1)

if __name__ == '__main__':
    main()
