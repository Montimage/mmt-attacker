# MMT-Attacker

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

MMT-Attacker is a powerful and flexible network attack simulation toolkit designed for security testing and network resilience assessment. It provides a comprehensive set of attack modules and PCAP replay capabilities to help security professionals evaluate network security measures in controlled environments.

## Features

- **Multiple Attack Vectors**: Support for various network and application-layer attacks
- **PCAP Replay**: Advanced packet replay functionality with customization options
- **Modular Design**: Easy to extend with new attack types
- **Detailed Logging**: Comprehensive logging and monitoring capabilities
- **Validation**: Input validation and safety checks built-in
- **Configuration**: Flexible configuration options for each attack type

### Supported Attacks

- ARP Spoofing
- SYN Flood
- DNS Amplification
- HTTP DoS
- Slowloris
- SSH Brute Force
- SQL Injection
- PCAP Replay
- Ping of Death
- Credential Harvesting

## Quick Start

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

## Documentation

- [Detailed Playbook](docs/PLAYBOOK.md): Comprehensive guide with examples
- [Attack Modules](docs/): Documentation for each attack type
- [Configuration Guide](docs/): Detailed configuration options
- [API Reference](docs/): API documentation for developers

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
│   ├── cli.py              # Command-line interface
│   ├── attacks/            # Attack implementations
│   │   ├── __init__.py
│   │   ├── base.py        # Base attack class
│   │   ├── arp_spoof.py
│   │   ├── syn_flood.py
│   │   └── ...
│   └── utils/             # Utility functions
├── docs/                  # Documentation
├── tests/                # Unit tests
├── examples/             # Example scripts
├── requirements.txt      # Python dependencies
└── README.md            # This file
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
from .base import AttackBase

class NewAttack(AttackBase):
    name = "new-attack"
    description = "Description of the new attack"

    def add_arguments(self, parser):
        parser.add_argument('--target', required=True, help='Target')
        # Add more arguments

    def validate(self, args):
        # Implement validation
        return True

    def run(self, args):
        # Implement attack logic
        pass
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

## Roadmap

- [ ] Additional attack vectors
- [ ] Enhanced reporting capabilities
- [ ] GUI interface
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] API integration
- [ ] Cloud deployment support
