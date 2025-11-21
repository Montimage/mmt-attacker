# ICMP Flood Attack Simulation (Ping Flood)

## Overview

The ICMP Flood (also known as Ping Flood) is a Denial of Service (DoS) attack that overwhelms a target system by sending a massive number of ICMP Echo Request (ping) packets. The attack consumes both bandwidth and processing resources as the target must process each packet and generate ICMP Echo Reply responses.

This attack is particularly effective because:
- ICMP packets require minimal overhead to generate
- Target systems typically process ICMP packets at the kernel level
- Each packet requires a response, doubling the resource consumption
- Many systems don't rate-limit ICMP responses by default

## Features

- **High-Speed Flooding**: Send thousands of ICMP packets per second
- **Variable Packet Sizes**: Configure packet size from 8 to 65,500 bytes
- **IP Spoofing**: Randomize source IP addresses to evade filtering
- **Rate Control**: Precisely control packet transmission rate
- **Performance Metrics**: Real-time statistics on packet rate and bandwidth
- **Progress Tracking**: Visual progress indicators during execution
- **Detailed Logging**: Comprehensive logging with configurable verbosity

## Requirements

- Python 3.7 or higher
- Scapy library (2.4.5 or higher)
- Root/Administrator privileges (required for raw ICMP packets)
- Network interface with appropriate permissions

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Standard ICMP flood
sudo python3 icmp_flood.py -t 192.168.1.10

# Send 5000 packets
sudo python3 icmp_flood.py -t 192.168.1.10 -c 5000
```

### Advanced Usage

```bash
# High-intensity attack with large packets
sudo python3 icmp_flood.py -t 192.168.1.10 -c 10000 -r 1000 -s 1400

# Disable IP spoofing
sudo python3 icmp_flood.py -t 192.168.1.10 --no-spoof

# Verbose output
sudo python3 icmp_flood.py -t 192.168.1.10 -v
```

## Monitoring the Attack

### On Attacking Machine

```bash
# Monitor outgoing ICMP traffic
sudo tcpdump -i any 'icmp and dst host 192.168.1.10' -c 100
```

### On Target Machine

```bash
# Monitor incoming ICMP traffic
sudo tcpdump -i any 'icmp' -c 100

# Check system load
top
htop
```

## Ethical Considerations

### Legal Requirements

- **Authorization Required**: Only use on networks/systems you own or have explicit permission to test
- **Compliance**: Ensure compliance with all applicable laws and regulations
- **Professional Use**: Intended for security professionals and researchers only
- **Educational Purpose**: Use in controlled lab environments for learning

### Safety Guidelines

1. Never use against production systems without authorization
2. Obtain written permission before testing
3. Inform stakeholders about planned testing
4. Document all testing activities
5. Restore systems to normal operation after testing

## Defensive Measures

### Detection

```bash
# Monitor ICMP packet rates
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-request -j LOG --log-prefix "ICMP FLOOD: "
```

### Mitigation

```bash
# Rate-limit ICMP traffic
sudo iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 10/s -j ACCEPT
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j DROP

# Disable ICMP responses (extreme measure)
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
```

### Prevention Strategies

1. **Rate Limiting**: Implement ICMP rate limits at firewall/router level
2. **ICMP Filtering**: Filter or prioritize ICMP traffic
3. **Ingress Filtering**: Prevent IP spoofing (BCP 38/RFC 2827)
4. **DDoS Protection**: Use cloud-based DDoS mitigation services
5. **Network Monitoring**: Deploy IDS/IPS solutions to detect floods

## Command Line Options

```
Required:
  -t, --target TARGET     IP address of the target

Optional:
  -c, --count COUNT       Number of packets (default: 1000)
  -r, --rate RATE         Packets per second (default: 100)
  -s, --size SIZE         Packet size in bytes (default: 64)
  --spoof                 Use random source IPs (default: True)
  --no-spoof              Disable IP spoofing
  -v, --verbose           Enable verbose output
```

## License

Proprietary - Montimage

## Disclaimer

This tool is provided for educational and authorized security testing purposes only. The authors assume no liability for misuse or damage caused by this program.
