# PCAP Replay Attack Simulation

This tool provides a class-based implementation for simulating network attacks by replaying captured network traffic (PCAP files) with customizable parameters. It allows for modifying destination IP addresses and ports to target specific systems.

## Overview

The PCAP Replay tool leverages `tcpreplay-edit` to replay captured network traffic with customizable parameters. This allows security professionals to simulate various network attacks in controlled environments for educational and testing purposes.

## Features

- **Customizable Packet Replay**: Adjust replay speed with rate multiplier
- **IP and Port Translation**: Rewrite destination IPs and ports to target specific systems
- **Interface Selection**: Choose the network interface for sending packets
- **Loop Mode**: Replay PCAP files multiple times for sustained testing
- **Detailed Statistics**: Get comprehensive information about the attack execution
- **Verbose Logging**: Enable detailed output for debugging and analysis

## Requirements

- Python 3.6 or higher
- `tcpreplay-edit` installed on the system
- Network interface with appropriate permissions
- PCAP files containing the attack traffic

To install the required Python dependencies:

```bash
pip install -r requirements.txt
```

To install tcpreplay-edit:
- On Ubuntu/Debian: `sudo apt-get install tcpreplay`
- On macOS: `brew install tcpreplay`
- On CentOS/RHEL: `sudo yum install tcpreplay`

## Usage

### Basic Usage

```bash
python pcap_replay.py -f /path/to/attack.pcap -t 192.168.1.10 -i eth0
```

### Command-Line Options

- `-f, --file`: Path to the PCAP file to replay (required)
- `-t, --target`: Target IP address to send traffic to (required)
- `-i, --interface`: Network interface to use for sending packets (required)
- `-p, --port`: Target port to send traffic to
- `-o, --original-ip`: Original destination IP in the PCAP file
- `-g, --original-port`: Original destination port in the PCAP file
- `-r, --rate`: Packet replay rate multiplier (default: 1.0)
- `-l, --loop`: Number of times to replay the PCAP file (default: 1)
- `-v, --verbose`: Enable verbose output

### Examples

#### Basic Replay

Replay a PCAP file to a target IP using a specific interface:

```bash
python pcap_replay.py -f attacks/ddos.pcap -t 192.168.1.10 -i eth0
```

#### IP and Port Translation

Replay a PCAP file with IP and port translation:

```bash
python pcap_replay.py -f attacks/sql_injection.pcap -t 192.168.1.10 -p 8080 -i eth0 -o 192.168.0.1 -g 80
```

#### Accelerated Replay with Looping

Replay a PCAP file at 10x speed, looping 5 times:

```bash
python pcap_replay.py -f attacks/worm.pcap -t 192.168.1.10 -i eth0 -r 10 -l 5
```

## Advanced Usage

### Replaying Multiple PCAP Files

To replay multiple PCAP files in sequence:

```bash
for pcap in /path/to/pcaps/*.pcap; do
    python pcap_replay.py -f "$pcap" -t 192.168.1.10 -i eth0
done
```

### Creating Custom Attack Scenarios

You can create custom attack scenarios by combining multiple PCAP files and adjusting replay parameters:

1. Start with reconnaissance PCAP at normal speed
2. Follow with exploitation PCAP at slower speed
3. Finish with payload delivery PCAP

## Ethical Considerations

This tool should ONLY be used for legitimate security testing with proper authorization. Unauthorized use against systems without explicit permission is illegal and unethical.

Always ensure you have:
- Written permission from the system owner
- Proper scope definition for testing
- Controlled environment to prevent collateral damage
- Compliance with local laws and regulations

## Defensive Measures

To protect against replay attacks:

- Implement strong packet filtering at network boundaries
- Use stateful inspection firewalls
- Deploy intrusion detection/prevention systems
- Implement rate limiting for network traffic
- Use encrypted protocols with strong authentication

## Troubleshooting

### Common Issues

1. **Permission Denied**: Run the script with appropriate privileges to access network interfaces
2. **Interface Not Found**: Verify the interface name with `ifconfig` or `ip addr`
3. **tcpreplay-edit Not Found**: Ensure tcpreplay is installed and in your PATH
4. **PCAP File Not Found**: Check the file path and permissions

### Debugging

Enable verbose mode with `-v` to get detailed output about the execution process.
