# MMT-Attacker

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

MMT-Attacker is a powerful and flexible network attack simulation toolkit designed for security testing and network resilience assessment. It provides a comprehensive set of attack modules and PCAP replay capabilities to help security professionals evaluate network security measures in controlled environments.

## Features

- **Multiple Attack Vectors**: Support for various network and application-layer attacks
- **PCAP Replay**: Advanced packet replay functionality with customization options
- **Interactive Web Interface**: Modern React-based frontend for educational demonstrations
- **Modular Design**: Easy to extend with new attack types
- **Detailed Logging**: Comprehensive logging and monitoring capabilities
- **Validation**: Input validation and safety checks built-in
- **Configuration**: Flexible configuration options for each attack type

### Supported Attacks

- [ARP Spoofing](docs/PLAYBOOK.md#arp-spoofing-attack): Man-in-the-middle attack using ARP cache poisoning
- [SYN Flood](docs/PLAYBOOK.md#syn-flood-attack): TCP SYN flood DoS attack
- [DNS Amplification](docs/PLAYBOOK.md#dns-amplification-attack): DNS reflection and amplification attack
- [HTTP DoS](docs/PLAYBOOK.md#http-dos-attack): HTTP-based denial of service attack
- [Slowloris](docs/PLAYBOOK.md#slowloris-attack): Slow HTTP DoS attack
- [SSH Brute Force](docs/PLAYBOOK.md#ssh-brute-force-attack): SSH credential brute force attack
- [SQL Injection](docs/PLAYBOOK.md#sql-injection-attack): SQL injection testing and exploitation
- [PCAP Replay](docs/PLAYBOOK.md#pcap-replay-attacks): Network traffic capture replay
- [Ping of Death](docs/PLAYBOOK.md#ping-of-death-attack): ICMP-based DoS attack
- [Credential Harvester](docs/PLAYBOOK.md#credential-harvester-attack): Phishing and credential theft simulation

## Quick Start
Looking for the Playbook? Check out the [PLAYBOOK](docs/PLAYBOOK.md).

Want to explore the interactive demo? Visit the [Web Interface](frontend/README.md).

### Prerequisites

- Python 3.7 or higher
- Root/sudo privileges (for certain attacks)
- Network interface in promiscuous mode (for packet capture/injection)

### Installation

```bash
# Clone the repository
git clone https://github.com/montimage/mmt-attacker.git
cd mmt-attacker

# Install dependencies
pip install -r requirements.txt

# Verify installation
python src/cli.py --help
```

### Basic Usage

```bash
# List available attacks
python src/cli.py --list

# Get help for a specific attack
python src/cli.py <attack-type> --help

# Run an attack (example: HTTP DoS)
python src/cli.py http-dos --target http://example.com --threads 10
```

## Examples

### PCAP Replay
```bash
python src/cli.py pcap-replay \
    --input-file capture.pcap \
    --interface eth0 \
    --loop 3 \
    --speed 2.0
```

### ARP Spoofing
```bash
python src/cli.py arp-spoof \
    --target 192.168.1.100 \
    --gateway 192.168.1.1 \
    --interface eth0 \
    --bidirectional
```

### HTTP DoS
```bash
python src/cli.py http-dos \
    --target http://example.com \
    --method POST \
    --threads 10 \
    --verify-success
```

## Development

### Project Structure

```
mmt-attacker/
├── src/
│   ├── cli.py                     # Command-line interface
│   ├── attacks/                   # Attack implementations
│   │   ├── __init__.py           # Attack registry
│   │   ├── base.py               # Base attack class
│   │   ├── arp_spoof.py          # ARP spoofing attack
│   │   ├── syn_flood.py          # SYN flood attack
│   │   ├── dns_amplification.py   # DNS amplification attack
│   │   ├── http_dos.py           # HTTP DoS attack
│   │   ├── slowloris.py          # Slowloris attack
│   │   ├── ssh_brute_force.py    # SSH brute force attack
│   │   ├── sql_injection.py      # SQL injection attack
│   │   ├── pcap_replay.py        # PCAP replay functionality
│   │   ├── ping_of_death.py      # Ping of Death attack
│   │   └── credential_harvester.py # Credential harvesting
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       ├── validator.py          # Input validation
│       ├── network.py            # Network utilities
│       └── logger.py             # Logging utilities
├── frontend/                     # Web interface (React + Vite)
│   ├── src/                      # Frontend source code
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── data/                # Attack data and scenarios
│   │   └── utils/               # Utility functions
│   ├── package.json             # Node.js dependencies
│   └── vite.config.js           # Vite configuration
├── docs/                         # Documentation
│   ├── PLAYBOOK.md              # Detailed usage guide
│   └── images/                   # Documentation images
├── requirements.txt             # Python dependencies
└── README.md                    # Project overview
```

### Adding New Attacks

1. Create a new attack module in `src/attacks/`
2. Inherit from `AttackBase` class
3. Implement required methods:
   - `add_arguments()`
   - `validate()`
   - `run()`
4. Register the attack in `src/attacks/__init__.py`

Example:
```python
from argparse import ArgumentParser
from typing import Optional
import logging

from .base import AttackBase

logger = logging.getLogger(__name__)

class NewAttack(AttackBase):
    """Template for implementing a new attack module"""
    
    name = "new-attack"  # Used in CLI: python src/cli.py new-attack ...
    description = "Description of the new attack type"
    
    def add_arguments(self, parser: ArgumentParser) -> None:
        # Group related arguments
        target_group = parser.add_argument_group('Target Configuration')
        target_group.add_argument(
            '--target', 
            required=True,
            help='Target IP or hostname'
        )
        target_group.add_argument(
            '--port',
            type=int,
            default=80,
            help='Target port'
        )
        
        # Add attack-specific options
        attack_group = parser.add_argument_group('Attack Configuration')
        attack_group.add_argument(
            '--method',
            choices=['GET', 'POST'],
            default='GET',
            help='HTTP method to use'
        )
        
        # Add common options
        net_group = parser.add_argument_group('Network Configuration')
        net_group.add_argument(
            '--interface',
            help='Network interface to use'
        )
        net_group.add_argument(
            '--timeout',
            type=float,
            default=5.0,
            help='Operation timeout in seconds'
        )
    
    def validate(self, args: ArgumentParser) -> bool:
        # Validate target configuration
        if not self.validator.validate_ip(args.target):
            logger.error(f"Invalid target IP: {args.target}")
            return False
            
        if not self.validator.validate_port(args.port):
            logger.error(f"Invalid port: {args.port}")
            return False
            
        # Validate network configuration
        if args.interface and not self.validator.validate_interface(args.interface):
            logger.error(f"Invalid interface: {args.interface}")
            return False
            
        if args.timeout <= 0:
            logger.error(f"Invalid timeout: {args.timeout}")
            return False
            
        return True
    
    def run(self, args: ArgumentParser) -> None:
        try:
            logger.info(f"Starting {self.name} attack against {args.target}:{args.port}")
            
            # Implement attack logic here
            # Use self.validator for input validation
            # Use appropriate error handling
            # Log important events and progress
            
            logger.info(f"Attack completed successfully")
            
        except Exception as e:
            logger.error(f"Attack failed: {str(e)}")
            raise
```

Then register the attack in `src/attacks/__init__.py`:
```python
from .new_attack import NewAttack

# Register the attack
ATTACKS = {
    # ... existing attacks ...
    "new-attack": NewAttack,
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Please ensure your code:
- Follows PEP 8 style guide
- Includes appropriate tests
- Updates documentation as needed
- Maintains backward compatibility

## Security Considerations

⚠️ **WARNING**: This tool is for educational and testing purposes only.

- Always obtain proper authorization before testing
- Use in controlled environments only
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Montimage Research Team
- Open Source Community
- Security Research Community

## Support

For support, please:
1. Check the [documentation](docs/)
2. Search [existing issues](https://github.com/montimage/mmt-attacker/issues)
3. Create a new issue if needed

## Web Interface

The project includes an interactive web interface for educational demonstrations and attack scenario exploration. Built with React and Vite, it provides:

- Interactive attack scenarios with step-by-step walkthroughs
- Visual attack flow diagrams using Mermaid
- Command generation with parameter validation
- Educational content for each attack type
- Simulated attack execution and results

### Running the Web Interface

```bash
cd frontend
npm install
npm run dev
```

The interface will be available at `http://localhost:3000`.

For production deployment, see [frontend/README.md](frontend/README.md).

## Roadmap

- [x] GUI interface
- [ ] Additional attack vectors
- [ ] Enhanced reporting capabilities
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] API integration
- [x] Cloud deployment support (Netlify)
