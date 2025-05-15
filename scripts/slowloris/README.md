# Slowloris Attack Simulation

## Overview

Slowloris is a type of Denial of Service (DoS) attack that targets web servers by opening multiple connections to the target server and keeping them open for as long as possible. Unlike traditional DoS attacks that flood servers with traffic, Slowloris uses minimal bandwidth by sending partial HTTP requests, making it difficult to detect and mitigate.

This script simulates a Slowloris attack for educational and authorized security testing purposes.

## Features

- Low-bandwidth DoS attack simulation
- Customizable connection count and timeout
- Detailed logging and statistics
- Performance monitoring
- Graceful shutdown and cleanup

## Requirements

- Python 3.6+
- Socket library (standard library)

## Installation

No additional libraries are required as the script uses Python's standard libraries.

## Usage

### Basic Attack

The simplest way to run a Slowloris attack is to specify a target host:

```bash
python slowloris.py example.com
```

This will:
- Target the specified host on port 80 (default)
- Use 150 connections (default)
- Use a socket timeout of 5 seconds (default)
- Run indefinitely until interrupted

### Customizing the Attack

#### Specify Port

To target a specific port:

```bash
# Target HTTPS (port 443)
python slowloris.py example.com -p 443

# Target a custom port
python slowloris.py example.com -p 8080
```

#### Adjust Connection Count

To control the number of connections:

```bash
# Use 300 connections (more aggressive)
python slowloris.py example.com -s 300

# Use 50 connections (less aggressive)
python slowloris.py example.com -s 50
```

#### Set Connection Timeout

To adjust how long to wait for each connection:

```bash
# Use a 10-second timeout
python slowloris.py example.com -t 10
```

#### Limit Attack Duration

To run the attack for a specific duration:

```bash
# Run for 60 seconds
python slowloris.py example.com -d 60
```

#### Enable Verbose Mode

For detailed output and debugging information:

```bash
python slowloris.py example.com -v
```

#### Use HTTPS

To target HTTPS servers:

```bash
python slowloris.py example.com -p 443 --https
```

## Advanced Usage

### Testing Server Limits

To find the connection limits of a server, you can gradually increase the connection count:

```bash
# Start with a low connection count
python slowloris.py example.com -s 50

# Increase if no effect is observed
python slowloris.py example.com -s 100
python slowloris.py example.com -s 200
python slowloris.py example.com -s 500
```

### Combining Parameters

For a more customized attack:

```bash
# HTTPS server with 200 connections, 8-second timeout, running for 2 minutes
python slowloris.py example.com -p 443 --https -s 200 -t 8 -d 120 -v
```

### Testing Different User Agents

Slowloris can be more effective with randomized user agents:

```bash
# Use random user agents
python slowloris.py example.com --randuseragent
```

## Monitoring the Attack

To observe the effect of the attack, you can use various tools:

```bash
# Check server response time
curl -o /dev/null -s -w "%{time_total}\n" http://example.com/

# Monitor server status (if available)
curl http://example.com/server-status

# Use tools like Apache Bench for benchmarking
ab -n 100 -c 10 http://example.com/
```

## Ethical Considerations

This tool should ONLY be used for:
- Educational purposes
- Authorized security testing
- Web server stress testing

Unauthorized use against systems without explicit permission is illegal and unethical.

## Defensive Measures

Common defenses against Slowloris attacks include:

1. Increasing the maximum number of clients the server can handle
2. Reducing connection timeout
3. Implementing rate limiting
4. Using reverse proxies (e.g., Nginx, HAProxy)
5. Deploying a Web Application Firewall (WAF)
6. Using load balancers
7. Implementing connection limits per IP

Understanding these attacks helps in implementing proper defenses.

## Command Line Options

```
positional arguments:
  host                  Host to perform stress test on

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port of webserver, usually 80
  -s SOCKETS, --sockets SOCKETS
                        Number of sockets to use in the test
  -v, --verbose         Increases logging
  -ua USERAGENT, --useragent USERAGENT
                        Specify a user-agent
  --randuseragent       Randomizes user-agents with each request
  --https               Use HTTPS for the requests
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for socket connection
  --proxy PROXY         SOCKS5 proxy to use
  -d DURATION, --duration DURATION
                        Duration of the attack in seconds (default: unlimited)
```

## License

Proprietary - Montimage
