# HTTP DoS Attack Simulation

## Overview

HTTP DoS (Denial of Service) attacks target web servers by overwhelming them with HTTP requests or by exploiting vulnerabilities in the HTTP protocol. This script simulates various HTTP-based DoS attacks including HTTP flooding, Slowloris (slow headers), and Slow POST (slow body) attacks.

This tool is designed for educational purposes and authorized security testing to help understand and defend against these attack vectors.

## Features

- Multiple attack methods:
  - HTTP GET flood
  - HTTP POST flood
  - Slowloris (slow HTTP headers)
  - Slow POST (slow HTTP body)
- Concurrent connections using threading
- Customizable request headers and payloads
- Connection keep-alive and timeout configuration
- Detailed logging and statistics
- Performance monitoring

## Requirements

- Python 3.6+
- Requests library

## Installation

```bash
# Install required dependencies
pip install requests
```

## Usage

### Basic Attack

The simplest way to run an HTTP DoS attack is to specify a target URL and attack method:

```bash
# HTTP GET flood (default method)
python http_dos.py -t http://example.com -m get

# HTTP POST flood
python http_dos.py -t http://example.com -m post
```

By default, the script will:
- Use 100 concurrent connections
- Run for 60 seconds
- Use a connection timeout of 10 seconds

### Attack Methods

The script supports four different attack methods:

```bash
# HTTP GET flood - sends numerous GET requests
python http_dos.py -t http://example.com -m get

# HTTP POST flood - sends numerous POST requests with data
python http_dos.py -t http://example.com -m post

# Slowloris - keeps connections open by sending partial headers
python http_dos.py -t http://example.com -m slowloris

# Slow POST - keeps connections open by sending the POST body slowly
python http_dos.py -t http://example.com -m slowpost
```

### Customizing the Attack

#### Adjust Connection Count

To control the number of concurrent connections:

```bash
# Use 200 concurrent connections
python http_dos.py -t http://example.com -m get -c 200

# Use fewer connections for a less intensive attack
python http_dos.py -t http://example.com -m get -c 50
```

#### Set Attack Duration

To control how long the attack runs:

```bash
# Run for 2 minutes (120 seconds)
python http_dos.py -t http://example.com -m get -d 120

# Run for a shorter duration (30 seconds)
python http_dos.py -t http://example.com -m get -d 30
```

#### Configure Connection Timeout

To adjust the connection timeout:

```bash
# Use a longer timeout (30 seconds)
python http_dos.py -t http://example.com -m slowloris -o 30

# Use a shorter timeout (5 seconds)
python http_dos.py -t http://example.com -m get -o 5
```

#### Enable Verbose Mode

For detailed output and debugging information:

```bash
python http_dos.py -t http://example.com -m get -v
```

## Advanced Usage

### Comparing Attack Methods

To evaluate which attack method is most effective against a specific target:

```bash
# Test GET flood
python http_dos.py -t http://example.com -m get -c 100 -d 60

# Test Slowloris
python http_dos.py -t http://example.com -m slowloris -c 100 -d 60

# Test Slow POST
python http_dos.py -t http://example.com -m slowpost -c 100 -d 60
```

### Slowloris Attack

Slowloris is particularly effective against servers with limited connection pools:

```bash
# Basic Slowloris attack
python http_dos.py -t http://example.com -m slowloris -c 200

# More aggressive Slowloris with more connections
python http_dos.py -t http://example.com -m slowloris -c 500 -d 120
```

### Slow POST Attack

Slow POST works well against application servers that wait for the complete request body:

```bash
# Basic Slow POST attack
python http_dos.py -t http://example.com -m slowpost -c 100

# More aggressive Slow POST with longer timeout
python http_dos.py -t http://example.com -m slowpost -c 200 -o 30 -d 180
```

## Monitoring the Attack

To observe the effect of the attack, you can use various tools:

```bash
# Monitor server response time
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
- Web application stress testing

Unauthorized use against systems without explicit permission is illegal and unethical.

## Defensive Measures

Common defenses against HTTP DoS attacks include:

1. Rate limiting
2. Connection timeouts
3. Load balancing
4. Web Application Firewalls (WAF)
5. Content Delivery Networks (CDN)
6. Request filtering

Understanding these attacks helps in implementing proper defenses.

## Command Line Options

```
-t, --target       URL of the target web server (required)
-m, --method       Attack method: get, post, slowloris, slowpost (default: get)
-c, --connections  Number of concurrent connections (default: 100)
-d, --duration     Duration of the attack in seconds (default: 60)
-o, --timeout      Connection timeout in seconds (default: 10)
-v, --verbose      Enable verbose output
```

## License

Proprietary - Montimage
