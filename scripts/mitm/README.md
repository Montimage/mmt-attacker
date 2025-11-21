# Man-in-the-Middle (MITM) Attack Simulation

## Overview

The Man-in-the-Middle (MITM) attack intercepts communication between two parties by positioning the attacker between them. This implementation uses ARP spoofing to poison the ARP caches of both the target and gateway, causing all traffic between them to flow through the attacker's machine.

## Features

- **ARP Cache Poisoning**: Bidirectional ARP spoofing
- **Traffic Interception**: Capture and inspect network traffic
- **Packet Capture**: Save intercepted packets to PCAP file
- **Automatic IP Forwarding**: Maintains connectivity while intercepting
- **Graceful Cleanup**: Restores ARP tables on exit
- **Configurable Update Intervals**: Control ARP poison frequency

## Requirements

- Python 3.7+
- Scapy 2.4.5+
- Root/Administrator privileges
- Network interface with appropriate permissions

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Basic MITM between target and gateway
sudo python3 mitm.py -t 192.168.1.10 -g 192.168.1.1 -i eth0
```

### Advanced Usage

```bash
# With packet capture
sudo python3 mitm.py -t 192.168.1.10 -g 192.168.1.1 -i eth0 --capture output.pcap

# Custom update interval
sudo python3 mitm.py -t 192.168.1.10 -g 192.168.1.1 -i eth0 --interval 2

# Verbose output
sudo python3 mitm.py -t 192.168.1.10 -g 192.168.1.1 -i eth0 -v
```

## Monitoring

```bash
# Monitor ARP table on target/gateway
arp -a

# Watch traffic flow
sudo tcpdump -i eth0 -n

# Verify IP forwarding (Linux)
cat /proc/sys/net/ipv4/ip_forward
```

## Ethical Considerations

- **Authorization Required**: Only use on networks you own or have permission to test
- **Legal Compliance**: Ensure compliance with all applicable laws
- **Professional Use**: For security testing and educational purposes only

## Defensive Measures

### Detection

```bash
# Static ARP entries (prevents ARP poisoning)
sudo arp -s 192.168.1.1 00:11:22:33:44:55

# Monitor for ARP anomalies
sudo arpwatch -i eth0
```

### Prevention

1. Use static ARP entries for critical hosts
2. Implement Dynamic ARP Inspection (DAI) on switches
3. Use encrypted protocols (HTTPS, SSH, VPN)
4. Deploy network monitoring tools
5. Enable port security on switches

## Command Line Options

```
Required:
  -t, --target TARGET      Target IP address
  -g, --gateway GATEWAY    Gateway IP address
  -i, --interface IFACE    Network interface

Optional:
  --interval SECONDS       ARP poison interval (default: 1.0)
  --capture FILE           Save packets to PCAP file
  -v, --verbose           Enable verbose output
```

## License

Proprietary - Montimage
